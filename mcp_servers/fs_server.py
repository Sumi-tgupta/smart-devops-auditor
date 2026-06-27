"""
mcp_servers/fs_server.py
────────────────────────
Local filesystem MCP server for Smart DevOps & Code Auditor.

SECURITY: All paths are validated against SANDBOX_ROOT before any file operation.
          Path traversal (../), symlink attacks, and absolute paths outside sandbox are blocked.
          Only READ tools are exposed — no write, delete, or execute.

Usage (called by orchestrator via ADK McpToolset):
  server = create_fs_server()
  # ADK will call tools like: list_directory, read_file, get_file_stats
"""

import os
import json
from pathlib import Path
from datetime import datetime
from fastmcp import FastMCP

# ── Security Boundary ──────────────────────────────────────────────────────────
SANDBOX_ROOT = Path(os.getenv("SANDBOX_ROOT", "./sandbox-repo")).resolve()
MAX_FILE_SIZE_KB = 512
ALLOWED_EXTENSIONS = {
    ".py", ".js", ".ts", ".env", ".yaml", ".yml", ".json", ".txt", ".md", ".cfg", ".ini"
}

# ── MCP Server Instance ────────────────────────────────────────────────────────
mcp = FastMCP("smart-devops-fs-server")


def _validate_path(requested: str) -> Path:
    """
    Canonicalize and validate that the requested path is inside SANDBOX_ROOT.
    Raises PermissionError if outside sandbox.
    Raises FileNotFoundError if file doesn't exist.
    Call this at the top of EVERY tool function.
    """
    # Resolve to absolute path — this defeats ../../../ traversal and symlinks
    target = (SANDBOX_ROOT / requested).resolve()

    # Check 1: Must be inside sandbox (string prefix check on resolved paths)
    if not str(target).startswith(str(SANDBOX_ROOT)):
        raise PermissionError(
            f"SECURITY VIOLATION: Access denied.\n"
            f"Requested: '{requested}'\n"
            f"Resolved:  '{target}'\n"
            f"Sandbox:   '{SANDBOX_ROOT}'\n"
            f"Agents may only access files within the sandbox directory."
        )

    # Check 2: Must exist
    if not target.exists():
        raise FileNotFoundError(
            f"File or directory not found within sandbox: '{requested}'\n"
            f"Sandbox root: '{SANDBOX_ROOT}'"
        )

    return target


def _check_extension(path: Path) -> None:
    """Raise ValueError if file extension is not in allowed list."""
    if path.suffix.lower() not in ALLOWED_EXTENSIONS:
        raise ValueError(
            f"File type '{path.suffix}' is not allowed for scanning.\n"
            f"Allowed: {', '.join(sorted(ALLOWED_EXTENSIONS))}"
        )


def _check_size(path: Path) -> None:
    """Raise ValueError if file exceeds max size."""
    size_kb = path.stat().st_size / 1024
    if size_kb > MAX_FILE_SIZE_KB:
        raise ValueError(
            f"File '{path.name}' is too large ({size_kb:.1f} KB > {MAX_FILE_SIZE_KB} KB limit)."
        )


# ── MCP TOOLS ─────────────────────────────────────────────────────────────────

@mcp.tool()
def list_directory(path: str = ".") -> str:
    """
    List files and subdirectories within the sandbox.

    Args:
        path: Relative path within sandbox. Use "." for sandbox root.

    Returns:
        JSON string with list of entries and their types.

    Security: Path is validated against SANDBOX_ROOT before any filesystem access.
    """
    target = _validate_path(path)

    if not target.is_dir():
        raise NotADirectoryError(f"'{path}' is not a directory.")

    entries = []
    for item in sorted(target.iterdir()):
        entries.append({
            "name": item.name,
            "type": "directory" if item.is_dir() else "file",
            "extension": item.suffix if item.is_file() else None,
            "size_kb": round(item.stat().st_size / 1024, 2) if item.is_file() else None,
            "relative_path": str(item.relative_to(SANDBOX_ROOT)),
        })

    return json.dumps({
        "directory": str(target.relative_to(SANDBOX_ROOT)),
        "entry_count": len(entries),
        "entries": entries,
        "sandbox_root": str(SANDBOX_ROOT),
    }, indent=2)


@mcp.tool()
def read_file(path: str) -> str:
    """
    Read the contents of a file within the sandbox.

    Args:
        path: Relative path to the file within sandbox.
              Example: "vulnerable_samples/auth.py"

    Returns:
        The raw text content of the file.

    Security:
        - Path validated against SANDBOX_ROOT
        - File extension must be in allowed list
        - File size must be < 512 KB
    """
    target = _validate_path(path)

    if not target.is_file():
        raise IsADirectoryError(f"'{path}' is a directory, not a file. Use list_directory instead.")

    _check_extension(target)
    _check_size(target)

    try:
        content = target.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        raise ValueError(f"'{path}' appears to be a binary file and cannot be read as text.")

    return content


@mcp.tool()
def get_file_stats(path: str) -> str:
    """
    Get metadata about a file within the sandbox.

    Args:
        path: Relative path to the file within sandbox.

    Returns:
        JSON string with file metadata.

    Security: Path validated against SANDBOX_ROOT.
    """
    target = _validate_path(path)

    stat = target.stat()
    line_count = 0

    if target.is_file():
        try:
            content = target.read_text(encoding="utf-8", errors="replace")
            line_count = len(content.splitlines())
        except Exception:
            line_count = -1  # binary or unreadable

    return json.dumps({
        "name": target.name,
        "relative_path": str(target.relative_to(SANDBOX_ROOT)),
        "type": "directory" if target.is_dir() else "file",
        "extension": target.suffix,
        "size_bytes": stat.st_size,
        "size_kb": round(stat.st_size / 1024, 2),
        "line_count": line_count,
        "last_modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
        "readable": target.is_file() and target.suffix in ALLOWED_EXTENSIONS,
    }, indent=2)


# ── DISABLED TOOLS (listed for documentation — not decorated with @mcp.tool()) ─

# write_file  → DISABLED — agents have no write access (ADR-006)
# delete_file → DISABLED — agents have no delete access (ADR-006)
# execute     → DISABLED — no shell execution allowed (ADR-006)


# ── Server Entry Point ─────────────────────────────────────────────────────────

def create_fs_server() -> FastMCP:
    """Return the configured MCP server instance for use with ADK McpToolset."""
    return mcp


def verify_server() -> bool:
    """
    Quick health check — verify sandbox exists and is accessible.
    Called by main.py --verify flag.
    """
    if not SANDBOX_ROOT.exists():
        print(f"❌ Sandbox directory not found: {SANDBOX_ROOT}")
        print(f"   Create it with: mkdir -p {SANDBOX_ROOT}")
        return False
    if not SANDBOX_ROOT.is_dir():
        print(f"❌ Sandbox path is not a directory: {SANDBOX_ROOT}")
        return False
    print(f"✅ MCP filesystem server ready (sandbox: {SANDBOX_ROOT})")
    return True


if __name__ == "__main__":
    # Run MCP server standalone (for testing or external connections)
    print(f"Starting MCP filesystem server...")
    print(f"Sandbox root: {SANDBOX_ROOT}")
    print(f"Allowed extensions: {', '.join(sorted(ALLOWED_EXTENSIONS))}")
    mcp.run()
