"""
sandbox-repo/vulnerable_samples/auth.py
────────────────────────────────────────
INTENTIONALLY VULNERABLE CODE — FOR DEMO PURPOSES ONLY
Contains: CWE-798 (Hardcoded Credentials), CWE-89 (SQL Injection)

DO NOT deploy or use this code in production.
"""
import sqlite3
import hashlib

# CWE-798: Hard-coded Credentials
# An attacker with repo access can extract these directly
API_KEY = "sk-1234abcd5678efghijklmnop"
DB_PASSWORD = "admin_password_123"
SECRET_TOKEN = "super_secret_jwt_signing_key"

def authenticate_user(username, password):
    """
    Authenticate user against the database.
    BUG: SQL Injection (CWE-89) + Weak crypto (CWE-327)
    """
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    # CWE-89: SQL Injection — user-controlled input interpolated into SQL
    # An attacker can pass: username = "' OR 1=1 --"
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    result = cursor.execute(query).fetchone()
    conn.close()

    return result is not None


def hash_password(password):
    """
    Hash a password for storage.
    BUG: MD5 is a broken algorithm for passwords (CWE-327)
    """
    # CWE-327: MD5 is not suitable for password hashing
    # Should use bcrypt, argon2, or scrypt
    return hashlib.md5(password.encode()).hexdigest()


def get_user_profile(user_id):
    """
    Fetch user profile.
    BUG: SQL Injection again + Logic bug (no null check)
    """
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    # CWE-89 again — same pattern
    query = f"SELECT name, email, role FROM users WHERE id={user_id}"
    result = cursor.execute(query).fetchone()

    # Logic Bug: result could be None if user not found
    # Accessing result[0] without None check causes AttributeError
    return {"name": result[0], "email": result[1], "role": result[2]}
