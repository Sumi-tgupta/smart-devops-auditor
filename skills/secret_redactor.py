"""
skills/secret_redactor.py
─────────────────────────
Skill 1 of 2: Secret Redactor

Masks sensitive strings in source code BEFORE any LLM sees it.
This is a pre-processing guard — called in orchestrator/pipeline.py
before every single agent invocation.

Pattern: FastMCP @tool decorator (see patterns.md — Pattern 2)
"""

import re
from fastmcp import FastMCP

mcp = FastMCP("secret-redactor-skill")


# ── Redaction Rules ────────────────────────────────────────────────────────────
# Format: (compiled_regex, replacement_string)
# Order matters — more specific patterns first.

REDACTION_RULES = [
    # AWS-style access keys (AKIA...)
    (re.compile(r'(AKIA[A-Z0-9]{16})', re.IGNORECASE),
     '[REDACTED-AWS-ACCESS-KEY]'),

    # Generic API keys assigned to common variable names
    (re.compile(r'((?:api[_-]?key|apikey)\s*=\s*["\'])([^"\']{8,})(["\'])', re.IGNORECASE),
     r'\1[REDACTED-API-KEY]\3'),

    # OpenAI / Anthropic style keys (sk-...)
    (re.compile(r'(["\'])(sk-[a-zA-Z0-9\-_]{20,})(["\'])'),
     r'\1[REDACTED-API-KEY]\3'),

    # Passwords
    (re.compile(r'((?:password|passwd|pwd)\s*=\s*["\'])([^"\']+)(["\'])', re.IGNORECASE),
     r'\1[REDACTED-PASSWORD]\3'),

    # Tokens
    (re.compile(r'((?:token|access_token|auth_token|bearer_token)\s*=\s*["\'])([^"\']+)(["\'])', re.IGNORECASE),
     r'\1[REDACTED-TOKEN]\3'),

    # Secrets
    (re.compile(r'((?:secret|secret_key|client_secret)\s*=\s*["\'])([^"\']+)(["\'])', re.IGNORECASE),
     r'\1[REDACTED-SECRET]\3'),

    # Private keys / certificates (multi-line block openers)
    (re.compile(r'(-----BEGIN (?:RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----)', re.IGNORECASE),
     '[REDACTED-PRIVATE-KEY-BLOCK]'),

    # Database connection strings with credentials
    (re.compile(r'((?:db|database|postgres|mysql|mongodb)://[^:]+:)([^@]+)(@)', re.IGNORECASE),
     r'\1[REDACTED-DB-PASSWORD]\3'),

    # Generic "connection_string" or "conn_str" variables
    (re.compile(r'((?:connection_string|conn_str|dsn)\s*=\s*["\'])([^"\']+)(["\'])', re.IGNORECASE),
     r'\1[REDACTED-CONNECTION-STRING]\3'),
]


@mcp.tool()
def redact_secrets(code: str) -> str:
    """
    Mask API keys, passwords, tokens, and other credentials in source code.

    Called BEFORE every agent invocation. Never skip this in the pipeline.
    Replaces real credential values with [REDACTED-X] placeholder tokens.

    Args:
        code: Raw source code string (may contain secrets)

    Returns:
        Code string with secrets replaced by redaction tokens.
        The code structure and logic is preserved exactly.
        Only the secret VALUES are replaced, not the variable names.

    Example:
        Input:  API_KEY = "sk-1234abcd5678efgh"
        Output: API_KEY = [REDACTED-API-KEY]
    """
    result = code
    redaction_count = 0

    for pattern, replacement in REDACTION_RULES:
        new_result, count = pattern.subn(replacement, result)
        result = new_result
        redaction_count += count

    return result


def redact_secrets_with_report(code: str) -> tuple[str, list[str]]:
    """
    Same as redact_secrets but also returns a list of what was redacted.
    Used for logging in orchestrator — not exposed as MCP tool.

    Returns:
        (redacted_code: str, redaction_log: list[str])
    """
    result = code
    redaction_log = []

    for pattern, replacement in REDACTION_RULES:
        matches = pattern.findall(result)
        if matches:
            label = replacement.strip("[]").replace("[REDACTED-", "").rstrip("]")
            redaction_log.append(f"Redacted {len(matches)} {label} pattern(s)")
        result = pattern.sub(replacement, result)

    return result, redaction_log


if __name__ == "__main__":
    # Quick test
    test_code = '''
import os

API_KEY = "sk-1234abcd5678efgh"
DB_PASSWORD = "super_secret_123"
token = "bearer_abc123xyz"
secret_key = "my-app-secret"

conn = "postgres://user:mypassword@localhost/db"

def connect():
    return conn
'''
    print("=== ORIGINAL ===")
    print(test_code)

    redacted, log = redact_secrets_with_report(test_code)
    print("=== REDACTED ===")
    print(redacted)
    print("=== LOG ===")
    for entry in log:
        print(f"  • {entry}")
