# 🧠 Project Memory

## Last Updated: 2026-06-27

---

## ✅ COMPLETED
- Project scaffolding and brain initialization — 2026-06-26
- PROJECT_BIBLE.md generated — 2026-06-26
- Data models defined in models/schemas.py — 2026-06-27
- MCP filesystem server built in mcp_servers/fs_server.py — 2026-06-27
- Secret redactor skill built in skills/secret_redactor.py — 2026-06-27
- Diff formatter skill built in skills/diff_formatter.py — 2026-06-27
- System prompts written in agents/prompts/ — 2026-06-27
- CLI entrypoint built in main.py — 2026-06-27
- Vulnerable sample files created in sandbox-repo/ — 2026-06-27
- Core reviewers, secops, and patch agents built — 2026-06-27
- Orchestrator pipeline built with rate-limit and injection safeguards — 2026-06-27
- Verified and successfully ran first codebase scan and patch generation (29 patches) — 2026-06-27
- Streamlit UI Dashboard completed with dynamic metrics, CWE alerts, copyable diffs, and runner pools — 2026-06-27
- Multi-key API rotation implemented at module-load level with explicit client bindings — 2026-06-27
- Comprehensive test suite implemented and passing (pytest -v) — 2026-06-27
- README.md setup, usage, and course concept mapping written — 2026-06-27
- Jupyter notebook for Kaggle submission compiled and generated — 2026-06-27

---

## 🔄 IN PROGRESS
- None (All local codebase components are fully completed and verified!)

---

## ⏳ PENDING / TODO

### Priority: CRITICAL (Submission)
- [ ] Test full notebook run on Kaggle.com (not just locally)
- [ ] Submit to Kaggle Capstone — DEADLINE: July 6, 2026 at 11:59 PM PT (= Jul 7 IST 12:29 PM)

---

## ❌ BLOCKERS
- None yet.

---

## 📋 SESSION LOG

### Session 1 — 2026-06-26
- Did: Project initialized, folder structure created, PROJECT_BIBLE.md generated, brain files initialized
- Changed: brain/ (all 4 files), project root structure
- Next: Install deps, get Gemini key, start with models/schemas.py then mcp_servers/fs_server.py

### Session 2 — 2026-06-27
- Did: Synchronized memory.md with existing files on disk. Installed dependencies, created `.env` file, and fixed console Unicode encoding issue on Windows. Resolved model quota rate limits (429) by switching to `gemini-2.5-flash` (which has active quota). Implemented Agent A, Agent B, and Agent C under `agents/` using Pydantic ADK Agent class, and built the orchestrator `pipeline.py` incorporating dynamic rate limit retries and prompt injection guards. Ran verification checks and verified successful end-to-end sandbox code scan (generated 29 patches).
- Next: Build ui/app.py and Streamlit UI panels.

### Session 3 — 2026-06-27 (Current Session)
- Did: Built premium Streamlit dashboard UI (ui/app.py) and modularized it into scan_panel.py, logic_panel.py, secops_panel.py, and patch_panel.py. Implemented multi-key API rotation using explicit `api_key` constructor parameters in a custom subclassed `KeyedGemini` class to avoid global environment pollution. Structured thread-safe synchronous pipeline runner to run smoothly under Streamlit's loop thread. Fixed ModuleNotFoundError: No module named 'ui' by dynamically prepending the parent directory to sys.path in ui/app.py.
- Next: Test and submit to Kaggle.

---
### [2026-06-27 | SESSION-3 | OPERATION: Implement Streamlit UI, Tests, README & Kaggle Notebook]

**File(s) Affected:** `ui/app.py`, `ui/components/*.py`, `tests/test_*.py`, `README.md`, `notebooks/kaggle_submission.ipynb`
**Status:** ✅ Done

#### BEFORE
> Only CLI entrypoint existed. No visual dashboard interface, no API key rotation, no test suite, and no self-contained submission notebook.

#### AFTER
> Full Streamlit dashboard built with key rotation and error persistence. Unit tests for skills and orchestrator pipeline implemented and passing (pytest -v). Detailed README.md explaining architecture and ADK concepts completed. Self-contained Jupyter notebook generated under notebooks/kaggle_submission.ipynb for Kaggle run.

#### REASON
> To complete all repository deliverables for Capstone MVP, ensure robust offline test validation, document the SDK patterns, and package the pipeline for evaluation.

#### REMAINING
> Test the notebook run directly on Kaggle.com and submit before deadline.
---

---
### [2026-06-27 | SESSION-2 | OPERATION: Create & Verify Agents & Pipeline]

**File(s) Affected:** `agents/code_reviewer.py`, `agents/secops_agent.py`, `agents/patch_agent.py`, `orchestrator/pipeline.py`, `agents/prompts/*.txt`
**Status:** ✅ Done

#### BEFORE
> Scaffolding and interface shells established. No Agent classes or execution pipeline logic implemented. Prompts used raw curly braces that triggered ADK interpolation crashes.

#### AFTER
> All three specialized agents (Code Reviewer, SecOps, Patch Artisan) fully wrapped in ADK Agent + Runner interfaces, utilizing `gemini-2.5-flash` for quota stability. The orchestrator pipeline executes these sequentially, applying regex-based secret redaction, prompt injection comment sanitization, and unified diff formats. Prompt files escaped.

#### REASON
> To complete the core auditor scan pipeline MVP. Transition to `gemini-2.5-flash` and escaping prompt variables was necessary to overcome 429 quota locks and ADK KeyError crashes.

#### REMAINING
> Development of ui/app.py Streamlit interface and UI panels.
---


