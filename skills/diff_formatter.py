"""
skills/diff_formatter.py
────────────────────────
Skill 2 of 2: Diff Formatter

Converts Agent C's (original_code, patched_code) pairs into standard
git unified diff format. Uses Python's stdlib difflib — no extra install.

Pattern: FastMCP @tool decorator (see patterns.md — Pattern 2)
Called in orchestrator/pipeline.py AFTER Agent C returns PatchSuggestion objects.
"""

import difflib
from fastmcp import FastMCP

mcp = FastMCP("diff-formatter-skill")


@mcp.tool()
def format_unified_diff(
    original_code: str,
    patched_code: str,
    file_path: str,
    context_lines: int = 3
) -> str:
    """
    Generate a git-compatible unified diff from original and patched code.

    Args:
        original_code: The original (problematic) code block
        patched_code:  The fixed code block from Agent C
        file_path:     Relative file path (shown in diff header)
        context_lines: Number of unchanged lines to show around changes (default: 3)

    Returns:
        Unified diff string in standard git format:
          --- a/<file_path>
          +++ b/<file_path>
          @@ -N,M +N,M @@
          -removed line
          +added line
           unchanged line

        Returns empty string if original == patched (no change needed).

    Example:
        original: "query = f'SELECT * FROM users WHERE id={user_id}'"
        patched:  "query = 'SELECT * FROM users WHERE id=?'\n        cursor.execute(query, (user_id,))"
        result:   standard unified diff showing the SQLi fix
    """
    if original_code == patched_code:
        return ""

    original_lines = original_code.splitlines(keepends=True)
    patched_lines = patched_code.splitlines(keepends=True)

    # Ensure lines end with newline (difflib needs this for clean output)
    if original_lines and not original_lines[-1].endswith("\n"):
        original_lines[-1] += "\n"
    if patched_lines and not patched_lines[-1].endswith("\n"):
        patched_lines[-1] += "\n"

    diff = list(difflib.unified_diff(
        original_lines,
        patched_lines,
        fromfile=f"a/{file_path}",
        tofile=f"b/{file_path}",
        n=context_lines,
    ))

    return "".join(diff)


@mcp.tool()
def format_side_by_side(original_code: str, patched_code: str) -> str:
    """
    Generate a simple side-by-side comparison as plain text.
    Useful for CLI display where unified diff may be harder to read.

    Args:
        original_code: Original code block
        patched_code:  Patched code block

    Returns:
        Human-readable side-by-side comparison.
    """
    original_lines = original_code.splitlines()
    patched_lines = patched_code.splitlines()

    max_width = max((len(line) for line in original_lines), default=40)
    col_width = min(max_width + 2, 60)

    lines = []
    lines.append(f"{'ORIGINAL':<{col_width}}  PATCHED")
    lines.append(f"{'─' * col_width}  {'─' * col_width}")

    max_len = max(len(original_lines), len(patched_lines))
    for i in range(max_len):
        orig = original_lines[i] if i < len(original_lines) else ""
        patched = patched_lines[i] if i < len(patched_lines) else ""

        # Mark lines that changed
        marker = "│" if orig == patched else "◄"
        lines.append(f"{orig:<{col_width}} {marker} {patched}")

    return "\n".join(lines)


def format_diff_for_display(unified_diff: str) -> dict:
    """
    Parse a unified diff string into structured data for Streamlit display.
    Not an MCP tool — called directly by Streamlit UI components.

    Returns:
        dict with keys:
            "added":   list of added lines (without leading +)
            "removed": list of removed lines (without leading -)
            "context": list of context lines
            "hunks":   number of @@ hunks
            "raw":     original unified diff string
    """
    added = []
    removed = []
    context = []
    hunks = 0

    for line in unified_diff.splitlines():
        if line.startswith("+++") or line.startswith("---"):
            continue  # header lines
        elif line.startswith("@@"):
            hunks += 1
        elif line.startswith("+"):
            added.append(line[1:])
        elif line.startswith("-"):
            removed.append(line[1:])
        elif line.startswith(" "):
            context.append(line[1:])

    return {
        "added": added,
        "removed": removed,
        "context": context,
        "hunks": hunks,
        "raw": unified_diff,
        "has_changes": bool(added or removed),
    }


if __name__ == "__main__":
    # Quick test
    original = """def authenticate_user(username, password):
    conn = sqlite3.connect("users.db")
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    result = conn.execute(query).fetchone()
    return result is not None
"""

    patched = """def authenticate_user(username, password):
    conn = sqlite3.connect("users.db")
    query = "SELECT * FROM users WHERE username=? AND password=?"
    result = conn.execute(query, (username, password)).fetchone()
    return result is not None
"""

    diff = format_unified_diff(original, patched, "sandbox-repo/auth.py")
    print("=== UNIFIED DIFF ===")
    print(diff)

    parsed = format_diff_for_display(diff)
    print(f"\n=== PARSED ===")
    print(f"Added lines: {parsed['added']}")
    print(f"Removed lines: {parsed['removed']}")
    print(f"Hunks: {parsed['hunks']}")
