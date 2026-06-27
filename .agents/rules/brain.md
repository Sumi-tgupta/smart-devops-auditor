---
trigger: always_on
---

# 🧠 BRAIN SYSTEM — MASTER PROMPT
### AI IDE Operating Protocol | Token-Efficient · Git-Style · Session-Aware

---

## ◈ CORE DIRECTIVE

You are a context-aware AI coding assistant operating under strict token
efficiency rules. Your single source of truth is the /brain folder.
You never read the full codebase unless explicitly instructed.
You treat every operation like a Git commit — traceable, diffable, logged.

---

## ◈ SESSION START PROTOCOL (Every New Message)

Execute in this exact order — do NOT skip steps:

  STEP 1 → Read  /brain/memory.md        (what happened, what's pending)
  STEP 2 → Read  /brain/architecture.md  (only if task touches structure/stack)
  STEP 3 → Read  /brain/patterns.md      (only if task involves new code)
  STEP 4 → Read  /brain/decisions.md     (only if task involves a design choice)
  STEP 5 → Proceed with the task
  STEP 6 → Update brain files (see UPDATE PROTOCOL)

⛔ NEVER scan or read source files outside /brain unless the task requires it.
   If you need a specific file, ask for its path. Read only that file.

---

## ◈ UPDATE PROTOCOL — After Every Operation

After every completed operation, update brain files using this format:

---
### [YYYY-MM-DD | SESSION-N | OPERATION: Edit/Create/Delete/Refactor]

**File(s) Affected:** `path/to/file.ext`
**Status:** ✅ Done / 🔄 In Progress / ❌ Blocked

#### BEFORE
> [Previous state or NEW FILE]

#### AFTER
> [What changed]

#### REASON
> [Why this change was made]

#### REMAINING
> [What still needs to be done]
---

Which file to update:
  Folder/stack change     → architecture.md
  New pattern/convention  → patterns.md
  Design/tech choice      → decisions.md
  Task done/blocked/next  → memory.md ← ALWAYS, no exceptions

---

## ◈ TOKEN EFFICIENCY RULES

  ✅ DO:
    Read only /brain files at session start
    Read source files only when path is given or task demands it
    Summarize changes in brain — don't paste full file contents
    Keep brain entries concise (bullet points > paragraphs)

  ⛔ DON'T:
    Scan or list entire project directories unprompted
    Re-read files you've already read this session
    Paste unchanged code blocks into brain files
    Update brain files with redundant/duplicate info

---

## ◈ COMMAND SHORTCUTS

  /status        → Read memory.md → print done/pending summary
  /brain-sync    → Review all 4 brain files → report inconsistencies
  /what-next     → Read memory.md → suggest next logical task
  /decision [X]  → Log a new ADR to decisions.md
  /checkpoint    → Force full brain update from current session

---

## ◈ PROJECT DETAILS

Project Name   : smart-devops-auditor
Description    : Multi-agent AI pipeline (Google ADK + Gemini 2.0 Flash)
                 that scans local Python code for bugs and security
                 vulnerabilities (CWE-mapped), then generates exact code
                 patches. 3 specialized agents: Code Reviewer → SecOps
                 → Patch Artisan. Zero cost — free tier only.
Tech Stack     : Python 3.11 / Google ADK / Gemini 2.0 Flash (free) /
                 FastMCP / Streamlit / difflib / python-dotenv
Current Phase  : MVP Development
Key Goals      : 1) Demonstrate all 5 ADK course concepts for Kaggle
                 2) Submit notebook by July 6 2026, 11:59 PM PT
                 3) Zero cost — Gemini free tier only, no credit card
Known Issues   : None (Day 1 — just initialized)
Repo           : github.com/Sumi-tgupta/smart-devops-auditor
Deadline       : July 6, 2026 at 11:59 PM PT (IST: July 7, 12:29 PM)

---

## ◈ ARCHITECTURE SNAPSHOT (for quick reference)

  Agents:
    Agent A (code_reviewer)  → logic bugs, smells, performance
    Agent B (secops_engineer) → CWE-89/798/22/327/78/16
    Agent C (patch_artisan)  → original + patched + explanation

  Skills (FastMCP):
    SecretRedactor  → masks API_KEY/password/token BEFORE any LLM call
    DiffFormatter   → git unified diff via difflib AFTER Agent C

  MCP Server:
    fs_server.py    → read-only, locked to ./sandbox-repo/
    Tools: list_directory, read_file, get_file_stats
    BLOCKED: write_file, delete_file, execute_command

  Security:
    Directory lock  → Path.resolve() validates all paths vs SANDBOX_ROOT
    Prompt sanitize → strips adversarial code comments before LLM

  Pipeline:
    ScanRequest → MCP reads files → SecretRedactor → PromptSanitizer
    → Agent A → Agent B → Agent C → DiffFormatter → PipelineResult

---

## ◈ CURRENT TASK PRIORITY (read memory.md for full list)

  HIGH (do these first):
    models/schemas.py             ← DONE ✅
    mcp_servers/fs_server.py      ← DONE ✅
    skills/secret_redactor.py     ← DONE ✅
    skills/diff_formatter.py      ← DONE ✅
    main.py                       ← DONE ✅
    agents/code_reviewer.py       ← BUILD NEXT
    agents/secops_agent.py
    agents/patch_agent.py
    orchestrator/pipeline.py
    ui/app.py

---

## ◈ GOLDEN RULE

  "Read the brain. Do the work. Update the brain. Never touch what you don't need."

  The brain folder is a living document.
  It grows smarter every session.
  The codebase is the implementation.
  The brain is the understanding.

---
Brain System v2.0 — smart-devops-auditor | Kaggle Capstone 2026