"""
sandbox-repo/vulnerable_samples/file_handler.py
─────────────────────────────────────────────────
INTENTIONALLY VULNERABLE CODE — FOR DEMO PURPOSES ONLY
Contains: CWE-22 (Path Traversal), Logic Bug (no error handling)

DO NOT deploy or use this code in production.
"""
import os


BASE_UPLOAD_DIR = "/var/app/uploads"


def read_user_file(filename):
    """
    Read a file from the uploads directory.
    BUG: Path Traversal (CWE-22) — no sanitization of filename
    """
    # CWE-22: Path Traversal
    # An attacker can pass: filename = "../../etc/passwd"
    # Which resolves to: /var/app/uploads/../../etc/passwd = /etc/passwd
    filepath = os.path.join(BASE_UPLOAD_DIR, filename)

    with open(filepath, "r") as f:
        return f.read()


def save_user_file(filename, content):
    """
    Save content to the uploads directory.
    BUG: Same path traversal issue on write.
    """
    # CWE-22: same problem — attacker can write anywhere
    filepath = f"{BASE_UPLOAD_DIR}/{filename}"

    # Logic Bug: no error handling — if directory doesn't exist, unhandled exception
    with open(filepath, "w") as f:
        f.write(content)


def list_user_files(user_id):
    """
    List all files for a given user.
    BUG: Logic Bug — result not filtered, returns all users' files
    """
    all_files = os.listdir(BASE_UPLOAD_DIR)

    # Logic Bug: filtering by user_id prefix assumes a naming convention
    # but never validates that the convention is actually enforced
    # An attacker could name their file "other_user_123_malware.py"
    user_files = []
    for f in all_files:
        # Dead Code: this condition is never False due to the empty string prefix trick
        if f.startswith(f"user_{user_id}_") or f.startswith(""):
            user_files.append(f)

    return user_files
