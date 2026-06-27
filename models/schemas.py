"""
models/schemas.py
─────────────────
All shared data models for the Smart DevOps & Code Auditor pipeline.
Passed between Agent A → Agent B → Agent C via the orchestrator.

Design: Python stdlib dataclasses (no Pydantic dependency — see ADR-005).
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict
from enum import Enum
from datetime import datetime
import uuid


# ──────────────────────────────────────────────────────────────────────────────
# ENUMS
# ──────────────────────────────────────────────────────────────────────────────

class Severity(str, Enum):
    """
    Issue severity levels with corresponding security score deductions.
    Score starts at 100, deducted per finding:
      CRITICAL → -30 | HIGH → -15 | MEDIUM → -7 | LOW → -3 | INFO → -1
    """
    CRITICAL = "CRITICAL"
    HIGH     = "HIGH"
    MEDIUM   = "MEDIUM"
    LOW      = "LOW"
    INFO     = "INFO"


class FindingType(str, Enum):
    """
    Classification of detected issues.
    Security types map to CWE identifiers (see CodeFinding.cwe_id).
    """
    HARDCODED_SECRET      = "HARDCODED_SECRET"       # CWE-798
    SQL_INJECTION         = "SQL_INJECTION"           # CWE-89
    COMMAND_INJECTION     = "COMMAND_INJECTION"       # CWE-78
    PATH_TRAVERSAL        = "PATH_TRAVERSAL"          # CWE-22
    WEAK_CRYPTO           = "WEAK_CRYPTO"             # CWE-327
    INSECURE_CONFIG       = "INSECURE_CONFIG"         # CWE-16
    LOGIC_BUG             = "LOGIC_BUG"              # General — Agent A
    CODE_SMELL            = "CODE_SMELL"             # General — Agent A
    PERFORMANCE_ISSUE     = "PERFORMANCE_ISSUE"      # General — Agent A
    PROMPT_INJECTION_RISK = "PROMPT_INJECTION_RISK"  # Novel AI-era finding


class AgentSource(str, Enum):
    """Which agent produced a finding."""
    CODE_REVIEWER = "code_reviewer"
    SECOPS        = "secops"


class PatchStatus(str, Enum):
    """User review status of a patch suggestion."""
    PENDING  = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


# ──────────────────────────────────────────────────────────────────────────────
# SEVERITY SCORE DEDUCTIONS
# ──────────────────────────────────────────────────────────────────────────────

SEVERITY_DEDUCTIONS: Dict[Severity, int] = {
    Severity.CRITICAL: 30,
    Severity.HIGH:     15,
    Severity.MEDIUM:    7,
    Severity.LOW:       3,
    Severity.INFO:      1,
}

SEVERITY_EMOJI: Dict[str, str] = {
    "CRITICAL": "🔴",
    "HIGH":     "🟠",
    "MEDIUM":   "🟡",
    "LOW":      "🟢",
    "INFO":     "ℹ️",
}


# ──────────────────────────────────────────────────────────────────────────────
# CORE DATA MODELS
# ──────────────────────────────────────────────────────────────────────────────

@dataclass
class CodeFinding:
    """
    A single issue detected by Agent A (Code Reviewer) or Agent B (SecOps).
    Produced AFTER code has been redacted — code_snippet contains [REDACTED-X] tokens
    if secrets were present in the original.
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    file_path: str = ""
    line_number: int = 0
    line_end: int = 0                    # last line of the affected block (0 = same as line_number)
    code_snippet: str = ""              # the offending code (post-redaction)
    finding_type: FindingType = FindingType.CODE_SMELL
    severity: Severity = Severity.LOW
    description: str = ""              # human-readable explanation for the developer
    cwe_id: Optional[str] = None       # e.g., "CWE-89" — only set by Agent B (SecOps)
    cwe_name: Optional[str] = None     # e.g., "Improper Neutralization of SQL Commands"
    agent_source: AgentSource = AgentSource.CODE_REVIEWER
    confidence: float = 0.0            # 0.0–1.0, agent's self-assessed confidence


@dataclass
class AuditReport:
    """
    Aggregated output from Agent A + Agent B for a full scan run.
    security_score is computed lazily via compute_score().
    """
    scan_id: str = field(default_factory=lambda: str(uuid.uuid4())[:12])
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    target_directory: str = "./sandbox-repo"
    files_scanned: int = 0
    total_lines_scanned: int = 0
    findings: List[CodeFinding] = field(default_factory=list)
    security_score: int = 100           # recomputed by compute_score() — don't set manually
    summary_by_severity: Dict[str, int] = field(default_factory=dict)
    reviewer_summary: str = ""          # Agent A's free-text summary of what it found
    secops_summary: str = ""            # Agent B's free-text summary

    def compute_score(self) -> int:
        """
        Compute security score: start at 100, deduct per finding severity.
        Floors at 0. Call this after all findings are populated.
        """
        score = 100
        for finding in self.findings:
            score -= SEVERITY_DEDUCTIONS.get(finding.severity, 0)
        self.security_score = max(0, score)
        return self.security_score

    def severity_summary(self) -> Dict[str, int]:
        """Count findings per severity. Populates summary_by_severity in-place."""
        counts = {s.value: 0 for s in Severity}
        for finding in self.findings:
            counts[finding.severity.value] += 1
        self.summary_by_severity = counts
        return counts

    def findings_by_severity(self, severity: Severity) -> List[CodeFinding]:
        """Filter findings by a specific severity level."""
        return [f for f in self.findings if f.severity == severity]

    def critical_count(self) -> int:
        return len(self.findings_by_severity(Severity.CRITICAL))

    def score_label(self) -> str:
        """Human-readable score label for UI display."""
        s = self.compute_score()
        if s >= 80:
            return f"✅ {s}/100 — Good"
        elif s >= 50:
            return f"⚠️ {s}/100 — Needs Attention"
        else:
            return f"🚨 {s}/100 — Critical Issues"


@dataclass
class PatchSuggestion:
    """
    A fix proposed by Agent C (Patch Artisan) for a single CodeFinding.
    unified_diff is populated AFTER Agent C runs, by the DiffFormatter skill.
    """
    patch_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    finding: CodeFinding = field(default_factory=CodeFinding)
    original_code: str = ""            # the problematic code block (pre-fix)
    patched_code: str = ""             # the fixed code block
    unified_diff: str = ""             # git unified diff — set by DiffFormatter skill
    explanation: str = ""              # why this patch fixes the finding
    confidence_score: float = 0.0     # 0.0–1.0, Agent C's confidence
    status: PatchStatus = PatchStatus.PENDING

    def is_auto_approvable(self, threshold: float = 0.95) -> bool:
        """Returns True if confidence meets auto-approve threshold."""
        return self.confidence_score >= threshold


@dataclass
class ScanRequest:
    """
    User-supplied scan configuration. Created by UI or CLI and passed to orchestrator.
    """
    target_dir: str = "./sandbox-repo"
    scan_depth: int = 3
    file_extensions: List[str] = field(
        default_factory=lambda: [".py", ".js", ".ts", ".env", ".yaml", ".yml"]
    )
    enable_secret_redaction: bool = True       # always True in production; locked in UI
    enable_prompt_sanitization: bool = True    # always True in production; locked in UI
    auto_approve_threshold: float = 0.95       # auto-approve patches above this confidence


@dataclass
class PipelineResult:
    """
    Final output of the orchestrator pipeline.
    Returned to Streamlit UI or CLI for display.
    """
    pipeline_id: str = field(default_factory=lambda: str(uuid.uuid4())[:12])
    scan_request: ScanRequest = field(default_factory=ScanRequest)
    audit_report: AuditReport = field(default_factory=AuditReport)
    patches: List[PatchSuggestion] = field(default_factory=list)
    approved_patches: List[str] = field(default_factory=list)   # patch_ids approved by user
    total_runtime_seconds: float = 0.0
    error_log: List[str] = field(default_factory=list)

    def summary(self) -> str:
        """One-liner for CLI / logging output."""
        r = self.audit_report
        return (
            f"[{r.scan_id[:8]}]  "
            f"{r.files_scanned} files  |  "
            f"{len(r.findings)} findings  |  "
            f"Score: {r.compute_score()}/100  |  "
            f"{len(self.patches)} patches  |  "
            f"{self.total_runtime_seconds:.1f}s"
        )

    def has_errors(self) -> bool:
        return len(self.error_log) > 0

    def approved_patch_objects(self) -> List[PatchSuggestion]:
        """Return only the patches the user has approved."""
        return [p for p in self.patches if p.patch_id in self.approved_patches]
