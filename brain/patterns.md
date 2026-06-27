# 🔁 Patterns & Conventions

## Naming Conventions
- Files:       snake_case              (code_reviewer.py, diff_formatter.py)
- Classes:     PascalCase              (CodeFinding, PatchSuggestion, AuditReport)
- Functions:   snake_case, verb-first  (run_scan, format_diff, redact_secrets, validate_path)
- Constants:   UPPER_SNAKE_CASE        (SANDBOX_ROOT, INJECTION_PATTERNS, SEVERITY_DEDUCTIONS)
- Enum values: UPPER_CASE              (Severity.CRITICAL, FindingType.SQL_INJECTION)
- Agent names: lowercase underscore    ("code_reviewer", "secops_engineer", "patch_artisan")
- Prompt files: {agent_name}_prompt.txt

## Code Patterns

### Pattern 1 — LlmAgent Definition (ADK)
```python
# agents/code_reviewer.py
import os
from google.adk.agents import LlmAgent

def _load_prompt(filename: str) -> str:
    prompt_path = os.path.join(os.path.dirname(__file__), "prompts", filename)
    with open(prompt_path, "r") as f:
        return f.read()

code_reviewer = LlmAgent(
    name="code_reviewer",
    model="gemini-2.0-flash",
    instruction=_load_prompt("code_reviewer_prompt.txt"),
)
```

### Pattern 2 — FastMCP Skill Tool
```python
# skills/secret_redactor.py
from fastmcp import FastMCP

mcp = FastMCP("secret-redactor-skill")

@mcp.tool()
def redact_secrets(code: str) -> str:
    """
    Mask sensitive strings before passing code to any LLM.
    Called BEFORE every agent invocation — never skip this.
    """
    import re
    patterns = [
        (r'(API_KEY\s*=\s*["\'])([^"\']{8,})(["\'])', r'\1[REDACTED-API-KEY]\3'),
        (r'(password\s*=\s*["\'])([^"\']+)(["\'])', r'\1[REDACTED-PASSWORD]\3'),
        (r'(token\s*=\s*["\'])([^"\']+)(["\'])', r'\1[REDACTED-TOKEN]\3'),
        (r'(secret\s*=\s*["\'])([^"\']+)(["\'])', r'\1[REDACTED-SECRET]\3'),
        (r'(private_key\s*=\s*["\'])([^"\']+)(["\'])', r'\1[REDACTED-KEY]\3'),
    ]
    result = code
    for pattern, replacement in patterns:
        result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
    return result
```

### Pattern 3 — MCP Path Validation (ALWAYS use this in fs_server.py)
```python
# mcp_servers/fs_server.py
import os
from pathlib import Path

SANDBOX_ROOT = Path(os.getenv("SANDBOX_ROOT", "./sandbox-repo")).resolve()

def _validate_path(requested: str) -> Path:
    """
    Validates that requested path is within sandbox.
    Raises PermissionError if outside. Always call this before any file op.
    """
    target = Path(requested).resolve()
    if not str(target).startswith(str(SANDBOX_ROOT)):
        raise PermissionError(
            f"Security violation: '{requested}' is outside sandbox '{SANDBOX_ROOT}'. "
            f"Agents may only access files within {SANDBOX_ROOT}."
        )
    if not target.exists():
        raise FileNotFoundError(f"File not found within sandbox: {requested}")
    return target
```

### Pattern 4 — Pre-LLM Guard (orchestrator/pipeline.py) — NEVER SKIP
```python
# In orchestrator/pipeline.py — applied BEFORE every single agent call
from skills.secret_redactor import redact_secrets
import re

INJECTION_PATTERNS = [
    r'#\s*ignore\s+(all\s+)?(previous|prior)\s+instructions',
    r'#\s*system\s*:',
    r'#\s*forget\s+everything',
    r'#\s*jailbreak',
    r'#\s*new\s+instructions',
]

def _sanitize_code(code: str) -> str:
    """Strip adversarial comment injection patterns before LLM sees code."""
    result = code
    for pattern in INJECTION_PATTERNS:
        result = re.sub(pattern, '# [SANITIZED-COMMENT]', result, flags=re.IGNORECASE)
    return result

def prepare_code_for_llm(raw_code: str) -> str:
    """Full pre-processing chain — call this every time before an agent."""
    redacted = redact_secrets(raw_code)       # Skill 1 — mask secrets
    clean = _sanitize_code(redacted)          # Guard — strip injections
    return clean
```

### Pattern 5 — Agent Response JSON Validation
```python
# In orchestrator/pipeline.py — parse agent output defensively
import json
from models.schemas import CodeFinding

def _parse_findings(raw_response: str, agent_source: str, error_log: list) -> list:
    """
    Parse agent JSON output into CodeFinding objects.
    Never crashes — errors go to error_log, returns [] on failure.
    """
    try:
        # Strip markdown fences if LLM wraps in ```json ... ```
        text = raw_response.strip()
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        data = json.loads(text.strip())
        findings_raw = data if isinstance(data, list) else data.get("findings", [])
        return [CodeFinding(**f, agent_source=agent_source) for f in findings_raw]
    except (json.JSONDecodeError, KeyError, TypeError, Exception) as e:
        error_log.append(f"[{agent_source}] Parse error: {e}")
        return []   # graceful degradation — never crash the pipeline
```

### Pattern 6 — Streamlit Session State for Scan Results
```python
# ui/app.py — initialize once, read in all tabs
import streamlit as st

def init_session_state():
    if "pipeline_result" not in st.session_state:
        st.session_state.pipeline_result = None
    if "approved_patches" not in st.session_state:
        st.session_state.approved_patches = []
    if "scan_running" not in st.session_state:
        st.session_state.scan_running = False

# Persist result across tabs:
# st.session_state.pipeline_result = run_pipeline(scan_request)
```

## Anti-Patterns — NEVER DO THESE
- ❌ Never pass raw code (unsanitized) to any LlmAgent
- ❌ Never trust file paths returned by LLM — validate every path against SANDBOX_ROOT
- ❌ Never `except: pass` or `except Exception: pass` — always log to error_log
- ❌ Never hardcode GEMINI_API_KEY or any credential in any .py file
- ❌ Never import brain/ files from agent code — brain is IDE context only
- ❌ Never skip JSON validation when parsing agent output
- ❌ Never create MCP write tools (write_file, delete_file) — read-only only
- ❌ Never let the Streamlit UI call agents directly — always go through orchestrator

## Changelog
---
### [2026-06-26 | SESSION-1 | OPERATION: Create]

**File(s) Affected:** brain/patterns.md
**Status:** ✅ Done

#### BEFORE
> NEW FILE

#### AFTER
> 6 canonical code patterns documented with working code snippets.
> 8 anti-patterns listed.

#### REASON
> Establish conventions before building any agent or skill code.

#### REMAINING
> Update as new patterns emerge during implementation.
---
