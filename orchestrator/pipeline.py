import os
import re
import json
import time
import uuid
import asyncio
import logging
from typing import List
from pathlib import Path

from models.schemas import (
    ScanRequest, PipelineResult, AuditReport, CodeFinding,
    PatchSuggestion, FindingType, Severity, AgentSource
)
from mcp_servers.fs_server import list_directory, read_file
from skills.secret_redactor import redact_secrets_with_report
from skills.diff_formatter import format_unified_diff

from agents import code_reviewer, secops_agent, patch_agent

logger = logging.getLogger(__name__)

def clean_prompt_injection(code: str) -> str:
    """
    Strips adversarial prompt injection comment patterns.
    Replaces matched comment lines with a sanitized placeholder.
    """
    patterns = [
        r"ignore\s+all\s+previous\s+instructions",
        r"ignore\s+previous\s+instructions",
        r"ignore\s+previous",
        r"system:",
        r"forget\s+everything",
        r"jailbreak",
        r"new\s+instructions",
    ]
    cleaned = code
    for p in patterns:
        # Matches comment characters followed by optional spaces and pattern
        regex = re.compile(rf"(?:#|//|--|/\*)\s*{p}.*", re.IGNORECASE)
        cleaned = regex.sub("# [SANITIZED-COMMENT]", cleaned)
    return cleaned

def _find_all_files(relative_dir: str, file_extensions: List[str]) -> List[str]:
    """Recursively lists all files in relative_dir with allowed extensions."""
    files = []
    try:
        res = json.loads(list_directory(relative_dir))
        for entry in res.get("entries", []):
            rel_path = entry.get("relative_path")
            if entry.get("type") == "file":
                # Check extension
                _, ext = os.path.splitext(rel_path)
                if ext.lower() in file_extensions:
                    files.append(rel_path)
            elif entry.get("type") == "directory":
                files.extend(_find_all_files(rel_path, file_extensions))
    except Exception as e:
        logger.error(f"Error traversing directory {relative_dir}: {e}")
    return files

from agents.code_reviewer import rotate_runner as rotate_reviewer
from agents.secops_agent import rotate_runner as rotate_secops
from agents.patch_agent import rotate_runner as rotate_patch
from agents.utils import get_all_keys

def rotate_all_runners():
    rotate_reviewer()
    rotate_secops()
    rotate_patch()

async def retry_with_backoff(coro_func, *args, delay=10, **kwargs):
    """Wraps an async function call with key rotation and retry backoff for rate limits."""
    keys = get_all_keys()
    num_keys = len(keys)
    
    for rotation_attempt in range(num_keys):
        try:
            return await coro_func(*args, **kwargs)
        except Exception as e:
            err_msg = str(e)
            # Check for 429 or RESOURCE_EXHAUSTED
            if "429" in err_msg or "RESOURCE_EXHAUSTED" in err_msg:
                # Rotate key immediately without sleeping if there are remaining keys to try
                if rotation_attempt < num_keys - 1:
                    rotate_all_runners()
                    logger.warning(
                        f"Rate limit 429 hit. Rotated to next API key in pool "
                        f"(Rotation {rotation_attempt + 1}/{num_keys}). Retrying immediately..."
                    )
                    continue
                else:
                    # All keys exhausted, perform a dynamic sleep backoff
                    match = re.search(r"Please retry in ([\d\.]+)s", err_msg, re.IGNORECASE)
                    if match:
                        wait_time = float(match.group(1)) + 1.5
                    else:
                        wait_time = delay
                    
                    logger.warning(
                        f"All keys in the pool hit 429. Sleeping for {wait_time:.1f} seconds "
                        f"before retrying..."
                    )
                    await asyncio.sleep(wait_time)
                    # Rotate back to make one final attempt
                    rotate_all_runners()
                    try:
                        return await coro_func(*args, **kwargs)
                    except Exception as final_err:
                        raise final_err
            raise e

def run_pipeline(request: ScanRequest) -> PipelineResult:
    """
    Synchronous entry point that runs the async pipeline.
    Safely executes in both standard and active-event-loop (Streamlit) environments.
    """
    try:
        # Check if there is an active running event loop
        asyncio.get_running_loop()
        # If yes, execute in a separate thread to avoid loop collision
        import concurrent.futures
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(asyncio.run, run_pipeline_async(request))
            return future.result()
    except RuntimeError:
        # No running event loop, safe to run directly
        return asyncio.run(run_pipeline_async(request))

async def run_pipeline_async(request: ScanRequest) -> PipelineResult:
    """
    Asynchronously runs the sequential analysis pipeline on a target directory.
    """
    start_time = time.time()
    pipeline_id = str(uuid.uuid4())[:12]
    
    result = PipelineResult(
        pipeline_id=pipeline_id,
        scan_request=request,
        audit_report=AuditReport(
            target_directory=request.target_dir
        )
    )
    
    # 1. Resolve relative directory to query the local MCP tools
    target_abs = Path(request.target_dir).resolve()
    sandbox_abs = Path(os.getenv("SANDBOX_ROOT", "./sandbox-repo")).resolve()
    
    if target_abs == sandbox_abs:
        start_rel = "."
    else:
        try:
            start_rel = str(target_abs.relative_to(sandbox_abs))
        except ValueError:
            # Reverts to absolute path string, which will cause fs_server validation to fail
            start_rel = str(target_abs)
            
    # 2. File discovery via MCP
    try:
        files_to_scan = _find_all_files(start_rel, request.file_extensions)
    except Exception as e:
        result.error_log.append(f"Directory lock security block / listing error: {e}")
        result.total_runtime_seconds = time.time() - start_time
        return result
        
    result.audit_report.files_scanned = len(files_to_scan)
    
    all_findings = []
    all_patches = []
    
    for file_path in files_to_scan:
        try:
            # 3. Read raw content
            raw_content = read_file(file_path)
            lines_in_file = len(raw_content.splitlines())
            result.audit_report.total_lines_scanned += lines_in_file
            
            # Apply Pre-processing Guards
            # A. Secret Redactor Skill
            redacted_code, redaction_log = redact_secrets_with_report(raw_content)
            for log_entry in redaction_log:
                logger.info(f"[{file_path}] {log_entry}")
                
            # B. Prompt Injection Sanitizer
            clean_code = clean_prompt_injection(redacted_code)
            
            # 4. Sequential Agent Calls with rate limit retries
            # Agent A: Code Reviewer
            reviewer_findings = await retry_with_backoff(
                code_reviewer.analyze_code, clean_code, file_path
            )
            
            # Agent B: SecOps Engineer
            secops_findings = await retry_with_backoff(
                secops_agent.analyze_code, clean_code, file_path, reviewer_findings
            )
            
            file_findings = reviewer_findings + secops_findings
            all_findings.extend(file_findings)
            
            # Agent C: Patch Artisan
            file_patches = await retry_with_backoff(
                patch_agent.generate_patches, clean_code, file_path, file_findings
            )
            
            # 5. Diff Formatting Skill
            for patch in file_patches:
                patch.unified_diff = format_unified_diff(
                    patch.original_code, patch.patched_code, file_path
                )
                all_patches.append(patch)
                
        except Exception as e:
            result.error_log.append(f"Failed to scan file '{file_path}': {e}")
            logger.error(f"Error scanning {file_path}: {e}", exc_info=True)
            
    # 6. Aggregate results
    result.audit_report.findings = all_findings
    result.patches = all_patches
    
    # Programmatic prose summaries
    result.audit_report.reviewer_summary = _generate_reviewer_summary(all_findings)
    result.audit_report.secops_summary = _generate_secops_summary(all_findings)
    
    # Compute security score & metrics
    result.audit_report.compute_score()
    result.audit_report.severity_summary()
    
    result.total_runtime_seconds = time.time() - start_time
    return result

def _generate_reviewer_summary(findings: List[CodeFinding]) -> str:
    reviewer_findings = [f for f in findings if f.agent_source == AgentSource.CODE_REVIEWER]
    if not reviewer_findings:
        return "No logic bugs, dead code, or performance bottlenecks were detected."
    num_bugs = len([f for f in reviewer_findings if f.finding_type == FindingType.LOGIC_BUG])
    num_smells = len([f for f in reviewer_findings if f.finding_type == FindingType.CODE_SMELL])
    num_perf = len([f for f in reviewer_findings if f.finding_type == FindingType.PERFORMANCE_ISSUE])
    return (
        f"Logic review identified {len(reviewer_findings)} code quality issue(s): "
        f"{num_bugs} logic bug(s), {num_smells} code smell(s), and {num_perf} performance issue(s)."
    )

def _generate_secops_summary(findings: List[CodeFinding]) -> str:
    secops_findings = [f for f in findings if f.agent_source == AgentSource.SECOPS]
    if not secops_findings:
        return "No security vulnerabilities (CWE) were detected."
    criticals = len([f for f in secops_findings if f.severity == Severity.CRITICAL])
    highs = len([f for f in secops_findings if f.severity == Severity.HIGH])
    mediums = len([f for f in secops_findings if f.severity == Severity.MEDIUM])
    return (
        f"Security scan identified {len(secops_findings)} vulnerability(ies): "
        f"{criticals} CRITICAL, {highs} HIGH, and {mediums} MEDIUM. CWE mapping applied successfully."
    )

