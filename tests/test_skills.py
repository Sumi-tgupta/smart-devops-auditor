import os
import sys

# Ensure root folder is in path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from skills.secret_redactor import redact_secrets_with_report
from skills.diff_formatter import format_unified_diff

def test_secret_redactor():
    """Verify that credentials are correctly identified and masked with logs."""
    code = (
        "API_KEY = 'sk-1234abcd5678efgh'\n"
        "password = \"prod_admin_password_99\"\n"
        "db_password = \"secret_pass\"\n"
    )
    
    redacted, logs = redact_secrets_with_report(code)
    
    # Check that secrets were redacted
    assert "sk-1234abcd5678efgh" not in redacted
    assert "prod_admin_password_99" not in redacted
    assert "secret_pass" not in redacted
    
    assert "[REDACTED-API-KEY]" in redacted
    assert "[REDACTED-PASSWORD]" in redacted
    assert "[REDACTED-PASSWORD]" in redacted # db_password contains 'password'
    
    # Check that logs were generated
    assert len(logs) == 2
    assert any("API-KEY" in log for log in logs)
    assert any("PASSWORD" in log for log in logs)

def test_diff_formatter():
    """Verify that unified diffs are correctly generated."""
    original = "def hello():\n    print('Hello World')\n"
    patched = "def hello():\n    print('Hello Dynamic World')\n"
    file_path = "vulnerable_samples/greet.py"
    
    diff = format_unified_diff(original, patched, file_path)
    
    assert "--- a/vulnerable_samples/greet.py" in diff
    assert "+++ b/vulnerable_samples/greet.py" in diff
    assert "-    print('Hello World')" in diff
    assert "+    print('Hello Dynamic World')" in diff
