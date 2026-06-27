"""
main.py
───────
CLI entrypoint for Smart DevOps & Code Auditor.

Usage:
  python main.py --verify              # Health check all components
  python main.py --scan ./sandbox-repo # Run full pipeline on target directory
  python main.py --help                # Show usage

This entrypoint is also used inside the Kaggle submission notebook
to run the pipeline without the Streamlit UI.
"""

import argparse
import os
import sys
import time
from pathlib import Path

# Force UTF-8 encoding on Windows to prevent UnicodeEncodeError with emojis
if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

from dotenv import load_dotenv

load_dotenv()  # Load .env before any other imports that need env vars


def cmd_verify() -> bool:
    """
    Health check: verify all components are ready.
    Run this first after initial setup.
    """
    print("\n🔍 Smart DevOps & Code Auditor — System Check\n")
    all_ok = True

    # 1. Gemini API key
    api_key = os.getenv("GEMINI_API_KEY", "")
    if api_key and api_key != "your_gemini_api_key_here":
        print("✅ GEMINI_API_KEY found")
    else:
        print("❌ GEMINI_API_KEY not set")
        print("   Get free key at: https://aistudio.google.com/")
        print("   Add to .env: GEMINI_API_KEY=your_key_here")
        all_ok = False

    # 2. MCP Sandbox
    from mcp_servers.fs_server import verify_server
    if not verify_server():
        all_ok = False

    # 3. Dependencies
    deps = ["google.adk", "fastmcp", "streamlit"]
    for dep in deps:
        try:
            __import__(dep.replace(".", "/").split("/")[0])
            print(f"✅ {dep} installed")
        except ImportError:
            print(f"❌ {dep} not installed — run: pip install {dep.split('.')[0]}")
            all_ok = False

    # 4. Brain folder
    brain_files = ["brain/memory.md", "brain/architecture.md", "brain/patterns.md", "brain/decisions.md"]
    brain_ok = all(Path(f).exists() for f in brain_files)
    if brain_ok:
        print("✅ Brain folder initialized (4 files)")
    else:
        missing = [f for f in brain_files if not Path(f).exists()]
        print(f"⚠️  Brain files missing: {missing}")
        print("   Copy pre-populated content from PROJECT_BIBLE.md Section 13")

    # 5. Models importable
    try:
        from models.schemas import CodeFinding, AuditReport, PatchSuggestion, PipelineResult  # noqa
        print("✅ Data models importable")
    except ImportError as e:
        print(f"❌ Model import error: {e}")
        all_ok = False

    print()
    if all_ok:
        print("🎉 All checks passed — system ready to scan!\n")
        print("   Next step: python main.py --scan ./sandbox-repo")
    else:
        print("⚠️  Fix the issues above before running a scan.\n")

    return all_ok


def cmd_scan(target_dir: str) -> None:
    """
    Run the full pipeline on a target directory and print results.
    """
    from models.schemas import ScanRequest
    from orchestrator.pipeline import run_pipeline

    print(f"\n🚀 Smart DevOps & Code Auditor — Scanning: {target_dir}\n")
    print("─" * 60)

    request = ScanRequest(target_dir=target_dir)

    start = time.time()
    result = run_pipeline(request)
    elapsed = time.time() - start

    result.total_runtime_seconds = elapsed

    # Print results
    print(f"\n{'═' * 60}")
    print(f"  SCAN COMPLETE")
    print(f"{'═' * 60}")
    print(result.summary())
    print()

    if result.audit_report.findings:
        print(f"{'─' * 60}")
        print(f"  FINDINGS ({len(result.audit_report.findings)} total)")
        print(f"{'─' * 60}")

        from models.schemas import SEVERITY_EMOJI
        for i, finding in enumerate(result.audit_report.findings, 1):
            emoji = SEVERITY_EMOJI.get(finding.severity.value, "•")
            cwe = f" [{finding.cwe_id}]" if finding.cwe_id else ""
            print(f"  {i:2}. {emoji} {finding.severity.value:<8}  "
                  f"{finding.file_path}:{finding.line_number}{cwe}")
            print(f"      {finding.finding_type.value}")
            print(f"      {finding.description[:100]}...")
            print()

    if result.patches:
        print(f"{'─' * 60}")
        print(f"  PATCHES ({len(result.patches)} generated)")
        print(f"{'─' * 60}")
        for i, patch in enumerate(result.patches, 1):
            print(f"  {i}. Patch {patch.patch_id} — confidence {patch.confidence_score:.0%}")
            if patch.unified_diff:
                # Print first 10 lines of diff
                diff_lines = patch.unified_diff.splitlines()[:10]
                for line in diff_lines:
                    print(f"     {line}")
            print()

    if result.error_log:
        print(f"{'─' * 60}")
        print(f"  ERRORS ({len(result.error_log)})")
        print(f"{'─' * 60}")
        for err in result.error_log:
            print(f"  ⚠️  {err}")

    security_score = result.audit_report.compute_score()
    print(f"{'═' * 60}")
    print(f"  Security Score: {security_score}/100  |  Runtime: {elapsed:.1f}s")
    print(f"{'═' * 60}\n")

    if security_score < 50:
        print("🚨 CRITICAL: Security score below 50 — urgent fixes needed.")
    elif security_score < 80:
        print("⚠️  WARNING: Security issues detected — review patches above.")
    else:
        print("✅ Code quality looks good. Review any remaining findings.")


def main():
    parser = argparse.ArgumentParser(
        prog="smart-devops-auditor",
        description="Smart DevOps & Code Auditor — AI-powered multi-agent SAST + patch generation",
    )

    parser.add_argument(
        "--verify",
        action="store_true",
        help="Run system health check (verify API key, sandbox, dependencies)",
    )
    parser.add_argument(
        "--scan",
        metavar="DIRECTORY",
        type=str,
        help="Scan a directory for bugs and security vulnerabilities",
    )
    parser.add_argument(
        "--ui",
        action="store_true",
        help="Launch Streamlit web UI (equivalent to: streamlit run ui/app.py)",
    )

    args = parser.parse_args()

    if args.verify:
        ok = cmd_verify()
        sys.exit(0 if ok else 1)

    elif args.scan:
        target = args.scan
        if not Path(target).exists():
            print(f"❌ Directory not found: {target}")
            sys.exit(1)
        cmd_scan(target)

    elif args.ui:
        print("🌐 Launching Streamlit UI...")
        os.system("streamlit run ui/app.py")

    else:
        parser.print_help()
        print("\nQuick start:")
        print("  python main.py --verify           # Check setup")
        print("  python main.py --scan ./sandbox-repo  # Run scan")
        print("  streamlit run ui/app.py           # Launch UI")


if __name__ == "__main__":
    main()
