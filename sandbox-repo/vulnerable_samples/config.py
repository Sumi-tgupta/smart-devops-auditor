"""
sandbox-repo/vulnerable_samples/config.py
──────────────────────────────────────────
INTENTIONALLY VULNERABLE CODE — FOR DEMO PURPOSES ONLY
Contains: CWE-16 (Insecure Config), CWE-798, Code Smells

DO NOT deploy or use this code in production.
"""

# ─── Application Settings ────────────────────────────────────────────────────

# CWE-16: Debug mode hardcoded ON — exposes stack traces and internals in production
DEBUG = True

# CWE-16: Secret key hardcoded — should come from environment
SECRET_KEY = "hardcoded-django-secret-key-do-not-use"

# CWE-16: CORS wildcard allows any origin to make authenticated requests
ALLOWED_ORIGINS = ["*"]

# CWE-16: SSL verification disabled — allows MITM attacks
VERIFY_SSL = False

# CWE-798: Database credentials hardcoded
DATABASE = {
    "host": "localhost",
    "port": 5432,
    "name": "production_db",
    "user": "admin",
    "password": "prod_password_2024",   # CWE-798
}

# Code Smell: Magic numbers without named constants
# 86400 means "1 day in seconds" — but it's not obvious without a comment
SESSION_TIMEOUT = 86400
MAX_UPLOAD_SIZE = 104857600  # 100MB — not obvious


# ─── Logging ────────────────────────────────────────────────────────────────

# CWE-16: Logging sensitive data (passwords, tokens) to stdout
LOGGING = {
    "level": "DEBUG",
    "log_passwords": True,     # NEVER do this
    "log_request_bodies": True,
}


# ─── Email Settings ──────────────────────────────────────────────────────────

EMAIL_CONFIG = {
    "smtp_host": "smtp.mailserver.com",
    "smtp_port": 587,
    "username": "noreply@company.com",
    # CWE-798: Email password hardcoded
    "password": "email_smtp_password_123",
    "use_tls": False,   # CWE-16: TLS disabled
}


# Code Smell: God function that configures everything
def setup_all_the_things():
    import os
    import sys
    import logging
    import sqlite3
    import json
    import requests
    import smtplib
    # ... this function does way too many unrelated things
    # violates single responsibility principle
    logging.basicConfig(level="DEBUG")
    os.environ["DEBUG"] = "1"
    # ... 50 more lines doing unrelated setup
    pass
