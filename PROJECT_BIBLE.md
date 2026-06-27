# 🤖 Smart DevOps & Code Auditor — Complete Project Bible
### Kaggle 5-Day AI Agents Capstone | Freestyle Track | Deadline: July 6, 2026 at 11:59 PM PT

---

## TABLE OF CONTENTS

| # | Section |
|---|---------|
| 1 | Kaggle Requirements Checklist |
| 2 | Free Tech Stack — ₹0 / $0 Verified |
| 3 | Antigravity IDE Setup |
| 4 | Project Folder Structure |
| 5 | Feature List |
| 6 | System Architecture |
| 7 | Agent Pipeline & Data Flow |
| 8 | Data Models (Python Dataclasses) |
| 9 | PRD — Product Requirements Document |
| 10 | MVP Scope |
| 11 | User Stories |
| 12 | UI/UX Component Guide |
| 13 | Brain Folder — Pre-Populated Init Files |
| 14 | Dev Timeline (10 Days to Deadline) |
| 15 | Quick Start Commands |
| 16 | Kaggle Notebook Strategy |

---

## 1. 📌 KAGGLE REQUIREMENTS CHECKLIST

### Core Concepts to Demonstrate (need ≥3, we demonstrate all 5)

| # | Course Concept | How This Project Covers It | Status |
|---|----------------|---------------------------|--------|
| ✅ | **Multi-Agent Systems (ADK)** | 3 sequential LlmAgents: Code Reviewer → SecOps → Patch Artisan, orchestrated via ADK | COVERED |
| ✅ | **MCP Servers** | Local Filesystem MCP Server (FastMCP) locked to `./sandbox-repo/` — agents get `read_file` + `list_directory` tools | COVERED |
| ✅ | **Agent Skills** | 2 custom FastMCP skills: `SecretRedactor` (pre-LLM masking) + `DiffFormatter` (git diff post-processing) | COVERED |
| ✅ | **Security Features** | Directory lock via MCP config + Prompt Injection Sanitizer strips adversarial code comments before LLM sees them | COVERED |
| ✅ | **Agent Orchestration** | Sequential pipeline: ADK handles inter-agent message + context passing across all 3 agents | COVERED |

**Total: 5 of 5 core concepts — exceeds minimum requirement.**

### Track Selection
- **Primary:** Freestyle Track — innovative DevOps/security tooling, creative framing
- **Alternate:** Agents for Business — framed as free SAST replacement ($0 vs $50k/year enterprise tools)
- **Recommendation:** Freestyle gives more creative freedom; evaluators reward novelty there

### Submission Logistics
- Deadline: **July 6, 2026 at 11:59 PM PT** = July 7, 2026 at ~12:29 PM IST
- Format: Kaggle Notebook (`.ipynb`) — see Section 16
- Team size: Solo (1 participant) OR team up to 4
- Prize for Top 3 per track: Kaggle swag + featured on Kaggle social media

---

## 2. 💸 FREE TECH STACK — ₹0 / $0 GUARANTEED

### Core Stack Table

| Layer | Tool | Version | License | Free Limit | How to Get |
|-------|------|---------|---------|-----------|------------|
| **LLM** | Gemini 2.0 Flash | `gemini-2.0-flash` | Google ToS | 1,500 req/day; 1M tokens/min | aistudio.google.com → Get API key |
| **AI Framework** | Google ADK | 1.x | Apache-2.0 | Unlimited | `pip install google-adk` |
| **MCP Protocol** | FastMCP | 2.x | MIT | Unlimited | `pip install fastmcp` |
| **UI** | Streamlit | 1.35+ | Apache-2.0 | Unlimited | `pip install streamlit` |
| **Runtime** | Python | 3.11+ | PSF | Unlimited | python.org |
| **Diff Engine** | difflib | stdlib | PSF | Unlimited | Built-in, no install |
| **Regex Engine** | re | stdlib | PSF | Unlimited | Built-in, no install |
| **Env Vars** | python-dotenv | 1.x | BSD-3 | Unlimited | `pip install python-dotenv` |
| **Compute** | Kaggle Notebooks | — | Free tier | 30h GPU/wk | kaggle.com |
| **Hosting/VCS** | GitHub | — | Free tier | Unlimited public repos | github.com |

### Getting Your Gemini API Key (No Credit Card)
```
1. Go to → https://aistudio.google.com/
2. Sign in with Google account (any Gmail)
3. Click "Get API key" → "Create API key in new project"
4. Copy the key
5. Paste into your .env file: GEMINI_API_KEY=your_key_here
6. Done. Zero billing setup required.
```

### Rate Limit Math (You're Safe)
```
Gemini 2.0 Flash free tier: 1,500 requests / day
Each full pipeline scan uses: ~6–9 API calls (2-3 per agent × 3 agents)
Max scans per day before hitting limits: ~165–250 full scans
Your actual usage (dev + demo): ~20–30 scans/day
Risk of accidental charges: ZERO (AI Studio free tier has hard cap, no billing)
```

---

## 3. ⚙️ ANTIGRAVITY IDE SETUP

### Step 1 — Project Initialization
```bash
# In Antigravity's integrated terminal
mkdir smart-devops-auditor
cd smart-devops-auditor
git init

# Python virtual environment
python -m venv .venv
source .venv/bin/activate        # Mac / Linux
# .venv\Scripts\activate         # Windows
```

### Step 2 — Brain Folder Creation
```bash
mkdir -p brain
touch brain/architecture.md brain/patterns.md brain/decisions.md brain/memory.md
```
Then copy the pre-populated content from **Section 13** into each file.
This is your persistent AI memory — populated once, kept alive every session.

### Step 3 — Antigravity Rules / System Prompt

In Antigravity IDE settings → "System Prompt" (or create `.aigrules` / `.windsurfrules` if the IDE supports project-level rules files), paste the **entire content of `BRAIN_MASTER_PROMPT.md`** as the system instruction.

At the bottom, in the `PROJECT DETAILS` section of the brain prompt, fill in:
```
Project Name   : smart-devops-auditor
Description    : Multi-agent AI pipeline that scans local code for bugs and 
                 security vulnerabilities using Google ADK + Gemini 2.0 Flash, 
                 then generates exact code patches. Zero cost.
Tech Stack     : Python 3.11 / Google ADK / Gemini 2.0 Flash / FastMCP / Streamlit
Current Phase  : MVP Development
Key Goals      : 1) Demonstrate all 5 ADK course concepts clearly
                 2) Submit Kaggle notebook by July 6, 2026 11:59 PM PT
                 3) Zero external API costs — free tier only
Known Issues   : None (Day 1)
Repo / Docs    : github.com/Sumi-tgupta/smart-devops-auditor
```

### Step 4 — Environment File
```bash
cp .env.example .env
# Open .env and replace placeholder with your actual Gemini API key
```

### Step 5 — Install All Dependencies
```bash
pip install google-adk fastmcp streamlit python-dotenv
pip freeze > requirements.txt
```

### Step 6 — Verify Setup
After writing `main.py` (Day 1 task), run:
```bash
python main.py --verify
# Expected output:
# ✅ Gemini 2.0 Flash connected (model: gemini-2.0-flash)
# ✅ MCP filesystem server ready (sandbox: ./sandbox-repo)
# ✅ Brain folder loaded (4 files)
# ✅ All agents importable
```

### Antigravity Workflow Commands
Once brain is set up, use these in chat with Antigravity:
```
/status        → Reads memory.md → prints done/pending summary
/what-next     → Reads memory.md → suggests the next task
/brain-sync    → Reviews all 4 brain files → finds inconsistencies
/checkpoint    → Forces full brain update from current session
```

---

## 4. 🗂️ PROJECT FOLDER STRUCTURE

```
smart-devops-auditor/
│
├── brain/                              # 🧠 AI IDE Context System (Antigravity)
│   ├── architecture.md                 # Stack, folder map, data flow
│   ├── patterns.md                     # Code conventions, anti-patterns
│   ├── decisions.md                    # Architecture Decision Records (ADRs)
│   └── memory.md                       # Session log, tasks, blockers ← updated every session
│
├── sandbox-repo/                       # 🔒 LOCKED TARGET DIRECTORY (MCP hard boundary)
│   └── vulnerable_samples/
│       ├── auth.py                     # Sample: hardcoded creds, weak session
│       ├── db_handler.py               # Sample: SQL injection (CWE-89)
│       ├── api_client.py               # Sample: exposed API key, no retry/timeout
│       ├── file_handler.py             # Sample: path traversal (CWE-22)
│       └── config.py                   # Sample: debug mode on, insecure defaults
│
├── agents/                             # 🤖 ADK LlmAgent Definitions
│   ├── __init__.py
│   ├── code_reviewer.py                # Agent A: logic bugs, code smells, performance
│   ├── secops_agent.py                 # Agent B: CWE vulnerabilities, secrets, injections
│   ├── patch_agent.py                  # Agent C: patch generation per finding
│   └── prompts/                        # System prompts as .txt (not hardcoded in .py)
│       ├── code_reviewer_prompt.txt
│       ├── secops_prompt.txt
│       └── patch_prompt.txt
│
├── skills/                             # 🛠️ FastMCP Custom Tool Skills
│   ├── __init__.py
│   ├── secret_redactor.py              # Skill 1: regex-based secret masking (pre-LLM)
│   └── diff_formatter.py               # Skill 2: unified git diff formatter (post-LLM)
│
├── mcp_servers/                        # 🔌 MCP Server + Security Config
│   ├── fs_server.py                    # Local filesystem MCP server (FastMCP)
│   └── mcp_config.json                 # Sandbox root lock + server parameters
│
├── orchestrator/                       # 🎼 Pipeline Coordination
│   ├── __init__.py
│   └── pipeline.py                     # Sequential runner: ScanRequest → PipelineResult
│
├── models/                             # 📦 Shared Data Models
│   ├── __init__.py
│   └── schemas.py                      # All dataclass definitions (see Section 8)
│
├── ui/                                 # 🖥️ Streamlit Frontend
│   ├── app.py                          # Main entry (streamlit run ui/app.py)
│   └── components/
│       ├── scan_panel.py               # Tab 1: scan trigger + live progress
│       ├── report_panel.py             # Tab 2: findings table + severity filter
│       └── patch_panel.py              # Tab 3: diff viewer + approve/reject buttons
│
├── tests/                              # 🧪 Pytest Test Suite
│   ├── test_skills.py                  # Unit tests for secret_redactor + diff_formatter
│   ├── test_pipeline.py                # Integration test for full pipeline
│   └── sample_vulnerable.py            # Fixture: known-vulnerable code for testing
│
├── notebooks/                          # 📓 Kaggle Submission
│   └── kaggle_submission.ipynb         # Self-contained demo — all 5 concepts shown
│
├── .env.example                        # Template (safe to commit)
├── .env                                # GITIGNORED — real GEMINI_API_KEY here
├── .gitignore
├── requirements.txt
├── README.md
└── main.py                             # CLI entrypoint (python main.py --scan ./sandbox-repo)
```

---

## 5. 📋 FEATURE LIST

### Core Features — MVP (Must Have by July 6)

| ID | Feature | Description | Module |
|----|---------|-------------|--------|
| F01 | File Discovery | List all .py files in sandbox directory via MCP | mcp_servers/fs_server |
| F02 | File Reading | Read file content via MCP (sandbox-locked) | mcp_servers/fs_server |
| F03 | Secret Redaction | Mask API keys, passwords, tokens before LLM | skills/secret_redactor |
| F04 | Prompt Sanitization | Strip adversarial code comments before LLM | orchestrator/pipeline |
| F05 | Code Review | Detect logic bugs, dead code, code smells, performance issues | agents/code_reviewer |
| F06 | Security Scan | Detect CWE-89 SQLi, CWE-798 hardcoded creds, CWE-22 path traversal, CWE-327 weak crypto | agents/secops_agent |
| F07 | Patch Generation | Produce original + patched code + explanation for each finding | agents/patch_agent |
| F08 | Diff Formatting | Convert patch to unified git diff (standard format) | skills/diff_formatter |
| F09 | Security Score | 0-100 score, deducted per finding severity (CRITICAL=-30, HIGH=-15, MED=-7, LOW=-3) | models/schemas |
| F10 | Audit Report | Structured report: findings[], severity summary, agent summaries | models/schemas |
| F11 | Directory Lock | MCP server rejects any path outside `./sandbox-repo/` | mcp_servers/fs_server |
| F12 | Streamlit UI | 4-tab interface: Scan / Report / Patches / About | ui/app |
| F13 | CLI Interface | `python main.py --scan ./sandbox-repo` for Kaggle notebook | main.py |
| F14 | Sample Vulnerable Code | 5 realistic Python files demonstrating all CWE types | sandbox-repo/ |
| F15 | Kaggle Notebook | Self-contained `.ipynb` demonstrating all 5 course concepts | notebooks/ |

### Stretch Features (If Time Allows)

| ID | Feature | Priority |
|----|---------|----------|
| F16 | Patch Auto-Apply | Write approved patches back to files | HIGH |
| F17 | Scan History | JSON file of past scans | MED |
| F18 | CWE Reference Links | Link findings to nvd.nist.gov | LOW |
| F19 | Multi-file Batch | Scan all files in one run, aggregate findings | MED |
| F20 | Report Export | Download audit report as Markdown | LOW |

---

## 6. 🏗️ SYSTEM ARCHITECTURE

```
╔══════════════════════════════════════════════════════════════════════════════╗
║            SMART DEVOPS & CODE AUDITOR — SYSTEM ARCHITECTURE v1.0           ║
╚══════════════════════════════════════════════════════════════════════════════╝

┌─────────────────────────────────────────────────────────────────────────────┐
│  USER INTERFACE LAYER                                                        │
│  ┌──────────────────────┐    ┌─────────────────────────────────────────┐   │
│  │  Streamlit Web UI    │    │   CLI: python main.py --scan [path]     │   │
│  │  streamlit run       │    │   (Used in Kaggle notebook cells)       │   │
│  │  ui/app.py           │    │                                         │   │
│  └──────────┬───────────┘    └────────────────────┬────────────────────┘   │
└─────────────┼──────────────────────────────────────┼───────────────────────┘
              │ ScanRequest                           │ ScanRequest
              └────────────────┬──────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│  ORCHESTRATOR (orchestrator/pipeline.py)                                     │
│                                                                              │
│  1. Receive ScanRequest(target_dir, file_extensions, guardrails)             │
│  2. Call MCP → list_directory() → get file list                             │
│  3. For each file → Call MCP → read_file() → raw_code                      │
│  4. Run SecretRedactor.run(raw_code) → redacted_code                        │
│  5. Run PromptSanitizer.clean(redacted_code) → clean_code                  │
│  6. Pass clean_code → Agent A                                               │
│  7. Collect Agent A findings → pass (clean_code + findings) → Agent B      │
│  8. Collect Agent B findings → pass (clean_code + all_findings) → Agent C  │
│  9. Run DiffFormatter.format() on each patch → add unified_diff field       │
│  10. Assemble PipelineResult → return to UI/CLI                             │
└──────────────────────────────────────────────────────────────────────────────┘
              │               │                │
              ▼               ▼                ▼
┌─────────────────┐ ┌──────────────────┐ ┌──────────────────────────────────┐
│   AGENT A       │ │   AGENT B        │ │   AGENT C                        │
│  Code Reviewer  │ │  SecOps Engineer │ │  Patch Artisan                   │
│─────────────────│ │──────────────────│ │──────────────────────────────────│
│ LlmAgent (ADK)  │ │ LlmAgent (ADK)   │ │ LlmAgent (ADK)                   │
│ Gemini 2.0 Flash│ │ Gemini 2.0 Flash │ │ Gemini 2.0 Flash                 │
│─────────────────│ │──────────────────│ │──────────────────────────────────│
│ INPUT:          │ │ INPUT:           │ │ INPUT:                           │
│  clean_code     │ │  clean_code      │ │  clean_code + all_findings[]     │
│  file_path      │ │  file_path       │ │  file_path                       │
│─────────────────│ │  A's findings    │ │──────────────────────────────────│
│ OUTPUT:         │ │──────────────────│ │ OUTPUT:                          │
│  CodeFinding[]  │ │ OUTPUT:          │ │  PatchSuggestion[]               │
│  (logic, perf,  │ │  CodeFinding[]   │ │  Each has: original_code,        │
│   code smell)   │ │  (CWE findings,  │ │  patched_code, explanation       │
│  severity:      │ │   severity:      │ │  [unified_diff added by skill]   │
│  LOW/MED/HIGH   │ │   MED/HIGH/CRIT) │ │                                  │
└─────────────────┘ └──────────────────┘ └──────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────────┐
│  SKILL LAYER (FastMCP @mcp.tool() decorated functions)                       │
│                                                                              │
│  PRE-PROCESSING (before any LLM call):                                      │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │  SecretRedactor.run(code: str) → str                                 │   │
│  │  Regex patterns matched:                                             │   │
│  │    API_KEY\s*=\s*["'][^"']{10,}["']  →  API_KEY=[REDACTED-API-KEY]  │   │
│  │    password\s*=\s*["'][^"']+["']     →  password=[REDACTED-PASSWORD] │   │
│  │    token\s*=\s*["'][^"']+["']        →  token=[REDACTED-TOKEN]       │   │
│  │    secret\s*=\s*["'][^"']+["']       →  secret=[REDACTED-SECRET]     │   │
│  │    private_key\s*=\s*["'][^"']+["']  →  private_key=[REDACTED-KEY]   │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │  PromptSanitizer.clean(code: str) → str    [in orchestrator]         │   │
│  │  Adversarial comment patterns stripped:                              │   │
│  │    # ignore previous instructions                                    │   │
│  │    # system:                                                         │   │
│  │    # forget everything                                               │   │
│  │    # jailbreak / new instructions                                    │   │
│  │  → replaced with: # [SANITIZED-COMMENT]                              │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│  POST-PROCESSING (after Agent C):                                           │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │  DiffFormatter.format(original, patched, file_path) → str            │   │
│  │  Uses Python stdlib: difflib.unified_diff()                          │   │
│  │  Output: standard git unified diff (--- a/ +++ b/ @@ format)         │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────────┐
│  MCP LAYER (mcp_servers/fs_server.py — FastMCP server)                       │
│                                                                              │
│  Tools exposed to all agents via ADK McpToolset:                            │
│  ├── list_directory(path: str) → list[str]                                  │
│  ├── read_file(path: str) → str                                             │
│  └── get_file_stats(path: str) → dict (size, modified, lines)               │
│                                                                              │
│  ╔══════════════════════════════════════════════════════════════════╗        │
│  ║  SECURITY CONSTRAINT — CANNOT BE BYPASSED                       ║        │
│  ║                                                                  ║        │
│  ║  SANDBOX_ROOT = Path("./sandbox-repo").resolve()                ║        │
│  ║                                                                  ║        │
│  ║  ALL tool calls validate:                                        ║        │
│  ║    if not target_path.startswith(SANDBOX_ROOT):                 ║        │
│  ║        raise PermissionError("Access denied: outside sandbox")  ║        │
│  ║                                                                  ║        │
│  ║  Agent tries to read /etc/passwd → BLOCKED                      ║        │
│  ║  Agent tries ../../home/user/ → BLOCKED                         ║        │
│  ╚══════════════════════════════════════════════════════════════════╝        │
└──────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────────┐
│  EXTERNAL SERVICES (Free Tier Only)                                          │
│                                                                              │
│  Google AI Studio ──► Gemini 2.0 Flash                                      │
│  Rate limit: 1,500 req/day | No credit card | Hard cap (no billing risk)    │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 7. 🔄 AGENT PIPELINE & DATA FLOW

```
INPUT: ScanRequest(
  target_dir="./sandbox-repo",
  file_extensions=[".py"],
  enable_secret_redaction=True,
  enable_prompt_sanitization=True
)
│
▼
╔════════════════════════════════════════════════════════════════════╗
║  PHASE 0 — FILE COLLECTION (via MCP)                              ║
║                                                                    ║
║  MCP.list_directory("./sandbox-repo")                             ║
║  → ["auth.py", "db_handler.py", "api_client.py", ...]            ║
║                                                                    ║
║  For each file:                                                    ║
║  MCP.read_file("./sandbox-repo/auth.py")                          ║
║  → raw_code: str                                                   ║
╚══════════════════════════════════╦═════════════════════════════════╝
                                   │ raw_code
                                   ▼
╔════════════════════════════════════════════════════════════════════╗
║  PHASE 1 — SANITIZATION (Skills, BEFORE any LLM call)            ║
║                                                                    ║
║  raw_code                                                          ║
║  ├──► SecretRedactor.run(raw_code)                                ║
║  │    API_KEY = "sk-123abc"  →  API_KEY = [REDACTED-API-KEY]     ║
║  │    password = "admin123"  →  password = [REDACTED-PASSWORD]   ║
║  │                                                                 ║
║  └──► PromptSanitizer.clean(redacted_code)                        ║
║       # Ignore previous → # [SANITIZED-COMMENT]                  ║
║       → clean_code: str                                           ║
╚══════════════════════════════════╦═════════════════════════════════╝
                                   │ clean_code
                                   ▼
╔════════════════════════════════════════════════════════════════════╗
║  PHASE 2 — AGENT A: CODE REVIEW (LlmAgent)                       ║
║                                                                    ║
║  Input:  clean_code + file_path                                   ║
║  System: "You are an expert code reviewer. Analyze code for:      ║
║           logic bugs, dead code, performance bottlenecks, code    ║
║           smells. Output JSON array of findings."                  ║
║  Output: List[CodeFinding]                                        ║
║          Example finding:                                          ║
║          {                                                         ║
║            "line_number": 15,                                      ║
║            "finding_type": "LOGIC_BUG",                           ║
║            "severity": "MEDIUM",                                   ║
║            "description": "Function returns None on failure ...", ║
║            "confidence": 0.87                                      ║
║          }                                                         ║
╚══════════════════════════════════╦═════════════════════════════════╝
                                   │ code_findings[] (A's output)
                                   ▼
╔════════════════════════════════════════════════════════════════════╗
║  PHASE 3 — AGENT B: SECOPS (LlmAgent)                            ║
║                                                                    ║
║  Input:  clean_code + file_path + code_findings (A's context)    ║
║  System: "You are a senior security engineer. Ignore code         ║
║           style. ONLY hunt for threat vectors. Map each           ║
║           finding to a CWE ID. Output JSON array."               ║
║  Targets: CWE-89 (SQLi), CWE-798 (hardcoded creds),              ║
║           CWE-22 (path traversal), CWE-327 (weak crypto),        ║
║           CWE-78 (cmd injection), CWE-16 (insecure config)       ║
║  Output: List[CodeFinding] with cwe_id + cwe_name populated      ║
╚══════════════════════════════════╦═════════════════════════════════╝
                                   │ all_findings[] (A + B merged)
                                   ▼
╔════════════════════════════════════════════════════════════════════╗
║  PHASE 4 — AGENT C: PATCH ARTISAN (LlmAgent)                     ║
║                                                                    ║
║  Input:  clean_code + all_findings[] + file_path                 ║
║  System: "You are a patch artisan. For each finding, produce      ║
║           the minimal code change to fix it. Preserve all other   ║
║           code. Output JSON: {finding_id, original_code,          ║
║           patched_code, explanation, confidence_score}"           ║
║  Output: List[PatchSuggestion] (unified_diff field = "" yet)     ║
╚══════════════════════════════════╦═════════════════════════════════╝
                                   │ patches[] (raw from Agent C)
                                   ▼
╔════════════════════════════════════════════════════════════════════╗
║  PHASE 5 — DIFF FORMATTING (Skill, POST-processing)              ║
║                                                                    ║
║  For each PatchSuggestion:                                        ║
║  DiffFormatter.format(original_code, patched_code, file_path)    ║
║  → unified_diff: str                                              ║
║                                                                    ║
║  Example output:                                                   ║
║  --- a/sandbox-repo/auth.py                                       ║
║  +++ b/sandbox-repo/auth.py                                       ║
║  @@ -12,3 +12,3 @@                                               ║
║  -query = f"SELECT * FROM users WHERE id={user_id}"              ║
║  +query = "SELECT * FROM users WHERE id=?"                       ║
║  +cursor.execute(query, (user_id,))                              ║
╚══════════════════════════════════╦═════════════════════════════════╝
                                   │
                                   ▼
OUTPUT: PipelineResult(
  audit_report=AuditReport(
    scan_id="a3f7c91b2d4e",
    files_scanned=5,
    findings=[...],          # all CodeFinding objects
    security_score=55,       # computed from findings
    reviewer_summary="...",
    secops_summary="..."
  ),
  patches=[PatchSuggestion(...)],
  total_runtime_seconds=12.4,
  error_log=[]
)
```

---

## 8. 📦 DATA MODELS (Python Dataclasses)

### File: `models/schemas.py`

```python
from dataclasses import dataclass, field
from typing import List, Optional, Dict
from enum import Enum
from datetime import datetime
import uuid


# ──────────────────────────── ENUMS ──────────────────────────────────────────

class Severity(str, Enum):
    """
    Score deductions per finding:
    CRITICAL=-30, HIGH=-15, MEDIUM=-7, LOW=-3, INFO=-1
    """
    CRITICAL = "CRITICAL"
    HIGH     = "HIGH"
    MEDIUM   = "MEDIUM"
    LOW      = "LOW"
    INFO     = "INFO"

class FindingType(str, Enum):
    HARDCODED_SECRET      = "HARDCODED_SECRET"      # CWE-798
    SQL_INJECTION         = "SQL_INJECTION"          # CWE-89
    COMMAND_INJECTION     = "COMMAND_INJECTION"      # CWE-78
    PATH_TRAVERSAL        = "PATH_TRAVERSAL"         # CWE-22
    WEAK_CRYPTO           = "WEAK_CRYPTO"            # CWE-327
    INSECURE_CONFIG       = "INSECURE_CONFIG"        # CWE-16
    LOGIC_BUG             = "LOGIC_BUG"             # General
    CODE_SMELL            = "CODE_SMELL"            # General
    PERFORMANCE_ISSUE     = "PERFORMANCE_ISSUE"     # General
    PROMPT_INJECTION_RISK = "PROMPT_INJECTION_RISK" # Novel (AI-era finding)

class AgentSource(str, Enum):
    CODE_REVIEWER = "code_reviewer"
    SECOPS        = "secops"

class PatchStatus(str, Enum):
    PENDING  = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


# ─────────────────────────── CORE MODELS ─────────────────────────────────────

@dataclass
class CodeFinding:
    """A single issue detected by Agent A or Agent B."""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    file_path: str = ""
    line_number: int = 0
    line_end: int = 0                   # end of affected code block
    code_snippet: str = ""              # the offending code (after redaction)
    finding_type: FindingType = FindingType.CODE_SMELL
    severity: Severity = Severity.LOW
    description: str = ""              # human-readable explanation
    cwe_id: Optional[str] = None       # e.g., "CWE-89"
    cwe_name: Optional[str] = None     # e.g., "Improper Neutralization of SQL"
    agent_source: AgentSource = AgentSource.CODE_REVIEWER
    confidence: float = 0.0            # 0.0 – 1.0

@dataclass
class AuditReport:
    """Aggregated output of Agent A + Agent B."""
    scan_id: str = field(default_factory=lambda: str(uuid.uuid4())[:12])
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    target_directory: str = "./sandbox-repo"
    files_scanned: int = 0
    total_lines_scanned: int = 0
    findings: List[CodeFinding] = field(default_factory=list)
    security_score: int = 100
    summary_by_severity: Dict[str, int] = field(default_factory=dict)
    reviewer_summary: str = ""          # Agent A's prose summary
    secops_summary: str = ""            # Agent B's prose summary

    def compute_score(self) -> int:
        """Compute security score: start at 100, deduct per finding severity."""
        DEDUCTIONS = {
            Severity.CRITICAL: 30,
            Severity.HIGH:     15,
            Severity.MEDIUM:    7,
            Severity.LOW:       3,
            Severity.INFO:      1,
        }
        score = 100
        for finding in self.findings:
            score -= DEDUCTIONS.get(finding.severity, 0)
        self.security_score = max(0, score)
        return self.security_score

    def severity_summary(self) -> Dict[str, int]:
        """Count findings per severity level."""
        counts = {s.value: 0 for s in Severity}
        for finding in self.findings:
            counts[finding.severity.value] += 1
        self.summary_by_severity = counts
        return counts

@dataclass
class PatchSuggestion:
    """A fix proposed by Agent C for a single CodeFinding."""
    patch_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    finding: CodeFinding = field(default_factory=CodeFinding)
    original_code: str = ""
    patched_code: str = ""
    unified_diff: str = ""             # populated by DiffFormatter skill
    explanation: str = ""              # why this patch fixes the finding
    confidence_score: float = 0.0     # Agent C's self-assessed confidence
    status: PatchStatus = PatchStatus.PENDING

@dataclass
class ScanRequest:
    """User-supplied configuration for a scan run."""
    target_dir: str = "./sandbox-repo"
    scan_depth: int = 3
    file_extensions: List[str] = field(
        default_factory=lambda: [".py", ".js", ".ts", ".env", ".yaml", ".yml"]
    )
    enable_secret_redaction: bool = True      # always True in prod
    enable_prompt_sanitization: bool = True   # always True in prod
    auto_approve_threshold: float = 0.95      # auto-approve if confidence ≥ this

@dataclass
class PipelineResult:
    """Final output returned to UI / CLI."""
    pipeline_id: str = field(default_factory=lambda: str(uuid.uuid4())[:12])
    scan_request: ScanRequest = field(default_factory=ScanRequest)
    audit_report: AuditReport = field(default_factory=AuditReport)
    patches: List[PatchSuggestion] = field(default_factory=list)
    approved_patches: List[str] = field(default_factory=list)  # patch_ids
    total_runtime_seconds: float = 0.0
    error_log: List[str] = field(default_factory=list)

    def summary(self) -> str:
        r = self.audit_report
        return (
            f"Scan {r.scan_id[:8]}  |  "
            f"{r.files_scanned} files scanned  |  "
            f"{len(r.findings)} findings  |  "
            f"Score: {r.compute_score()}/100  |  "
            f"{len(self.patches)} patches generated  |  "
            f"Runtime: {self.total_runtime_seconds:.1f}s"
        )
```

---

## 9. 📄 PRD — Product Requirements Document

```
Product:  Smart DevOps & Code Auditor
Version:  1.0-MVP
Date:     June 26, 2026
Owner:    Sumit Gupta (2024UCD2142, NSUT Delhi)
Track:    Kaggle 5-Day AI Agents Capstone — Freestyle
```

### 9.1 Executive Summary

Smart DevOps & Code Auditor is an autonomous, multi-agent AI pipeline that acts as a free, on-demand senior developer + security engineer. It scans a target folder of Python code, detects structural bugs and CWE-mapped security vulnerabilities, and automatically generates the exact code patches needed to fix them — entirely for free using Google ADK + Gemini 2.0 Flash.

**The Problem:**
Enterprise SAST tools (Snyk, Checkmarx, Veracode) cost $5,000–$50,000/year. Manual code review for security vulnerabilities is slow and error-prone. Developers — especially students and indie builders — can't afford either option.

**The Solution:**
A free, AI-powered, multi-agent pipeline that any developer can run locally. No cloud bills. No subscriptions. Just a free Gemini API key.

### 9.2 Success Metrics (MVP)

| Metric | Definition | Target |
|--------|-----------|--------|
| Coverage | % of 5 sample file vulnerabilities detected | ≥ 80% (4/5 files flagged correctly) |
| Patch Validity | % of patches that are syntactically valid Python | ≥ 90% |
| Speed | Time to scan 5-file sandbox end-to-end | ≤ 90 seconds |
| Cost | Monthly operating cost | $0 |
| Kaggle Concepts | Course concepts clearly demonstrated | All 5 of 5 |

### 9.3 Non-Goals (Out of Scope for MVP)

- Real-time file watcher / continuous scanning
- Auto-applying approved patches to disk (user must do it manually in MVP)
- Languages other than Python
- Scanning databases or live production environments
- LLM fine-tuning
- Authentication / multi-user support

### 9.4 User Personas

**Primary: Solo Developer (Student / Indie)**
- Cannot afford commercial SAST tools
- Building personal or academic projects
- Wants a quick security checkup before sharing code
- Uses the CLI for scanning, or the Streamlit UI for reviewing findings

**Secondary: Kaggle Evaluator**
- Assessing technical quality of ADK multi-agent implementation
- Needs to clearly see each course concept demonstrated
- Will run the Kaggle notebook — needs it to be self-contained and fast

### 9.5 Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-01 | System SHALL read files ONLY from designated sandbox directory (MCP lock) | MUST |
| FR-02 | System SHALL redact API keys, passwords, tokens BEFORE passing code to any LLM | MUST |
| FR-03 | System SHALL strip adversarial comment patterns from code BEFORE any LLM call | MUST |
| FR-04 | Agent A SHALL return findings as structured data (FindingType, Severity, line_number, description) | MUST |
| FR-05 | Agent B SHALL map security findings to CWE identifiers where applicable | MUST |
| FR-06 | Agent C SHALL return original_code + patched_code + explanation per finding | MUST |
| FR-07 | System SHALL format patches as unified git diffs using Python difflib | MUST |
| FR-08 | System SHALL compute a 0-100 security score from findings | MUST |
| FR-09 | UI SHALL display findings in a table filterable by severity | SHOULD |
| FR-10 | UI SHALL show unified diff for each patch (+ lines green, - lines red) | SHOULD |
| FR-11 | User SHALL be able to approve or reject each patch individually | SHOULD |
| FR-12 | System SHALL support CLI invocation (no UI dependency) for Kaggle notebook | MUST |
| FR-13 | Kaggle notebook SHALL be self-contained — no local file dependencies | MUST |

### 9.6 Non-Functional Requirements

| ID | Requirement | Target |
|----|-------------|--------|
| NFR-01 | All LLM calls use Gemini 2.0 Flash free tier | $0 cost |
| NFR-02 | Agent JSON responses validated before parsing (try/except) | Crash-free |
| NFR-03 | MCP sandbox enforced at path-validation level — not just config | No escape |
| NFR-04 | Secret redaction applied BEFORE every single LLM context injection | No leakage |
| NFR-05 | Codebase readable by another developer without system context | Clean code |
| NFR-06 | Kaggle notebook runs in ≤ 10 minutes total | Submission viability |

---

## 10. 🎯 MVP SCOPE

### The MVP Boundary

```
MVP = Core Pipeline + Streamlit UI + Kaggle Notebook

IN MVP:
✅ MCP filesystem server with directory lock
✅ Agent A: Code Reviewer (logic bugs, code smells, performance)
✅ Agent B: SecOps Engineer (CWE-89, CWE-798, CWE-22, CWE-327)
✅ Agent C: Patch Artisan (original → patched code + explanation)
✅ Skill 1: Secret Redactor (regex-based, pre-LLM)
✅ Skill 2: Diff Formatter (difflib, post-LLM)
✅ Security Guardrail 1: Directory Lock (MCP path validation)
✅ Security Guardrail 2: Prompt Injection Sanitizer
✅ Streamlit UI: Scan tab + Report tab + Patches tab
✅ CLI entrypoint: python main.py --scan ./sandbox-repo
✅ 5 sample vulnerable Python files in sandbox-repo/
✅ README.md with setup + usage
✅ Kaggle submission notebook (.ipynb)

NOT IN MVP:
❌ Auto-apply patches to disk
❌ Multiple language support (JS/TS)
❌ Persistent scan history (database)
❌ CWE reference links
❌ Report export (PDF/Markdown download)
❌ File watcher / real-time scan
❌ Multi-user / auth
```

### MVP Build Priority Order

```
Priority 1 (Foundation — must work before anything else)
  → MCP filesystem server + directory lock

Priority 2 (Core agents — build + test individually)
  → Agent A (Code Reviewer)
  → Agent B (SecOps)
  → Skills (SecretRedactor + PromptSanitizer + DiffFormatter)
  → Agent C (Patch Artisan)

Priority 3 (Integration)
  → Orchestrator pipeline (connects all agents)

Priority 4 (Interface)
  → Streamlit UI
  → CLI entrypoint

Priority 5 (Submission)
  → Sample vulnerable code files
  → Kaggle notebook
  → README
```

---

## 11. 👤 USER STORIES

### Epic 1 — Scanning & Discovery

| ID | Story | Acceptance Criteria |
|----|-------|---------------------|
| US-01 | As a developer, I want to point the tool at a folder and have it automatically find and scan all Python files | Given target_dir="./sandbox-repo", when I trigger a scan, then all .py files are discovered via MCP and queued for analysis |
| US-02 | As a developer, I want my API keys and passwords masked before they reach the AI, so my secrets stay private | Given code with `API_KEY = "sk-abc123"`, when the pipeline runs, then the LLM receives `API_KEY = [REDACTED-API-KEY]` |
| US-03 | As a developer, I want protection against my own code tricking the AI, so malicious comments can't hijack the agent | Given code with `# ignore all previous instructions`, when sanitized, then the LLM receives `# [SANITIZED-COMMENT]` |

### Epic 2 — Code Analysis

| ID | Story | Acceptance Criteria |
|----|-------|---------------------|
| US-04 | As a developer, I want to see all logic bugs and code smells with file and line number, so I can find them quickly | Given a completed scan, when I view the Report tab, then each finding shows file_path, line_number, finding_type, severity, description |
| US-05 | As a developer, I want to know if my code has SQL injection vulnerabilities mapped to CWE-89, so I understand the security impact | Given code with `f"SELECT * FROM users WHERE id={user_id}"`, when Agent B scans, then a finding with finding_type=SQL_INJECTION, cwe_id="CWE-89", severity=CRITICAL is returned |
| US-06 | As a developer, I want a single security score for my codebase, so I can track improvement over time | Given 3 CRITICAL + 2 HIGH findings, when compute_score() runs, then score = max(0, 100 - 90 - 30) = 0 → shown as 0/100 in UI |

### Epic 3 — Patch Review

| ID | Story | Acceptance Criteria |
|----|-------|---------------------|
| US-07 | As a developer, I want to see the exact lines that will change, in git diff format, before accepting any patch | Given a PatchSuggestion, when I view the Patches tab, then `unified_diff` is displayed with `---` original and `+++` patched lines highlighted |
| US-08 | As a developer, I want to approve or reject each patch individually, so I stay in control of my codebase | Given a list of patches, when I click ✅ Approve, then that patch's status → APPROVED and its patch_id enters approved_patches list |
| US-09 | As a developer, I want an explanation for why each patch fixes the issue, so I learn from the review | Given any PatchSuggestion, then explanation field contains a human-readable reason tied to the specific finding |

### Epic 4 — Security & Guardrails

| ID | Story | Acceptance Criteria |
|----|-------|---------------------|
| US-10 | As a system operator, I want the AI to be physically incapable of reading files outside the sandbox folder | Given any file path starting with `../` or `/etc/` or `/home/`, when MCP validates, then PermissionError is raised and the agent receives an error, not file contents |
| US-11 | As a Kaggle evaluator, I want to clearly see all 5 course concepts demonstrated in the notebook | Given the submission notebook, then there are labeled sections for: Multi-Agent System, MCP Server, Agent Skills, Security Features, Agent Orchestration |

---

## 12. 🖥️ UI/UX COMPONENT GUIDE

### Framework: Streamlit 1.35+ | File: `ui/app.py`

### Overall Layout

```
╔═════════════════════════════════════════════════════════════════════╗
║  🛡️  Smart DevOps & Code Auditor                          v1.0     ║
╠══════════════╦══════════════════════════════════════════════════════╣
║  SIDEBAR     ║  🔍 Scan  │  📊 Report  │  🔧 Patches  │  ℹ️ About ║
║              ╠══════════════════════════════════════════════════════╣
║  API Status  ║                                                      ║
║  ─────────── ║             [ MAIN CONTENT AREA ]                   ║
║  ✅ Gemini   ║                                                      ║
║     Connected║                                                      ║
║              ║                                                      ║
║  Extensions: ║                                                      ║
║  [✅ .py]    ║                                                      ║
║  [☐  .js]   ║                                                      ║
║              ║                                                      ║
║  Guardrails: ║                                                      ║
║  [✅ Secrets]║                                                      ║
║  [✅ Inject] ║                                                      ║
║  (locked on) ║                                                      ║
╚══════════════╩══════════════════════════════════════════════════════╝
```

### Sidebar (`ui/app.py` — `render_sidebar()`)

```python
# API Status indicator
if os.getenv("GEMINI_API_KEY"):
    st.sidebar.success("✅ Gemini 2.0 Flash Connected")
else:
    st.sidebar.error("❌ GEMINI_API_KEY not set — add to .env")

st.sidebar.divider()

# Scan settings
st.sidebar.subheader("⚙️ Scan Settings")
extensions = st.sidebar.multiselect(
    "File Extensions",
    options=[".py", ".js", ".ts", ".env", ".yaml"],
    default=[".py"]
)

st.sidebar.divider()

# Security guardrails — always locked ON, visually show them
st.sidebar.subheader("🔒 Security Guardrails")
st.sidebar.checkbox("Secret Redaction", value=True, disabled=True,
    help="API keys and passwords are ALWAYS masked before any LLM call")
st.sidebar.checkbox("Prompt Injection Guard", value=True, disabled=True,
    help="Adversarial code comments are stripped before any LLM call")
```

### Tab 1 — 🔍 Scan (`ui/components/scan_panel.py`)

```
┌─────────────────────────────────────────────────────────────────────┐
│  🔍 SCAN PANEL                                                       │
│                                                                      │
│  Target Directory:                                                   │
│  ┌──────────────────────────────────────────┐  🔒 Locked            │
│  │ ./sandbox-repo                           │  (MCP boundary)       │
│  └──────────────────────────────────────────┘                       │
│                                                                      │
│  [ 🔍 Start Scan ]   ← primary button                               │
│                                                                      │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  67%   ← progress bar         │
│                                                                      │
│  🔄 Agent B (SecOps) scanning db_handler.py...   ← live status     │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │  ✅ File collection complete: 5 files                        │   │
│  │  ✅ Secrets redacted in 3 files                              │   │
│  │  ✅ Agent A (Code Review): 8 findings                        │   │
│  │  🔄 Agent B (SecOps): running...                             │   │
│  └──────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

**Key Components:**
- `st.text_input` for directory — value locked to sandbox, disabled
- `st.button("🔍 Start Scan", type="primary")` — triggers pipeline
- `st.progress(value)` — updated by orchestrator callbacks
- `st.status("Scanning...")` — expandable live log
- `st.metric("Files Found", N)` — shown after completion

### Tab 2 — 📊 Report (`ui/components/report_panel.py`)

```
┌─────────────────────────────────────────────────────────────────────┐
│  📊 AUDIT REPORT                                                     │
│                                                                      │
│  Security Score           Scan ID              Files Scanned        │
│  ┌───────────┐       ┌──────────────┐       ┌──────────────┐       │
│  │  55 /100  │       │  a3f7c91b   │       │      5       │       │
│  │  ▼ -45    │       │              │       │              │       │
│  └───────────┘       └──────────────┘       └──────────────┘       │
│                                                                      │
│  [🔴 CRITICAL: 2]  [🟠 HIGH: 3]  [🟡 MEDIUM: 4]  [🟢 LOW: 1]     │
│                                                                      │
│  Filter: [ All Severities ▼ ]                                       │
│                                                                      │
│  ┌────────┬──────────────┬──────┬────────────────┬────────┬───────┐ │
│  │Severity│ File         │ Line │ Type           │ CWE    │ Conf. │ │
│  ├────────┼──────────────┼──────┼────────────────┼────────┼───────┤ │
│  │🔴 CRIT │ auth.py      │  12  │ HARDCODED_SEC  │CWE-798 │  98% │ │
│  │🔴 CRIT │ db_handler.py│  34  │ SQL_INJECTION  │CWE-89  │  97% │ │
│  │🟠 HIGH │ api_client.py│   8  │ INSECURE_CONFIG│CWE-16  │  91% │ │
│  │🟡 MED  │ file_handler │  51  │ PATH_TRAVERSAL │CWE-22  │  88% │ │
│  └────────┴──────────────┴──────┴────────────────┴────────┴───────┘ │
│                                                                      │
│  [Expand finding for code snippet + full description]               │
└─────────────────────────────────────────────────────────────────────┘
```

**Key Components:**
- `st.metric("Security Score", value, delta)` — red if score dropped
- `st.columns(5)` with colored severity badge counts
- `st.selectbox("Filter by Severity")` — filters findings dataframe
- `st.dataframe(df, use_container_width=True)` with color styling
- `st.expander(f"Finding {i} detail")` → shows code_snippet, description, CWE

**Severity Color Map:**
```python
SEVERITY_COLORS = {
    "CRITICAL": "#FF4B4B",   # Streamlit red
    "HIGH":     "#FF8C00",   # Orange
    "MEDIUM":   "#FFD700",   # Yellow
    "LOW":      "#28A745",   # Green
    "INFO":     "#17A2B8",   # Teal
}
```

### Tab 3 — 🔧 Patches (`ui/components/patch_panel.py`)

```
┌─────────────────────────────────────────────────────────────────────┐
│  🔧 PATCH REVIEW (10 patches generated)                             │
│                                                                      │
│  Patch 1 of 10 — auth.py : line 12 (HARDCODED_SECRET)             │
│  Confidence: ████████████████████ 98%                               │
│                                                                      │
│  --- a/sandbox-repo/auth.py                                         │
│  +++ b/sandbox-repo/auth.py                                         │
│  @@ -12,1 +12,2 @@                                                  │
│  - API_KEY = "sk-1234abcd5678efgh"                                  │
│  + import os                                                         │
│  + API_KEY = os.getenv("API_KEY", "")                               │
│                                                                      │
│  ℹ️ Hardcoded API keys expose credentials in version control.       │
│     Replace with environment variable lookup via os.getenv().       │
│                                                                      │
│  [ ✅ Approve ]    [ ❌ Reject ]    Confidence: 98%                 │
│  ───────────────────────────────────────────────────────────────── │
│  Patch 2 of 10 — db_handler.py : line 34 (SQL_INJECTION)          │
│  ...                                                                 │
└─────────────────────────────────────────────────────────────────────┘
```

**Key Components:**
- `st.code(patch.unified_diff, language="diff")` — syntax highlighted diff
- `st.info(patch.explanation)` — explanation in blue info box
- `st.progress(patch.confidence_score)` — visual confidence bar
- `st.columns([1,1,2])` → [Approve btn] [Reject btn] [Confidence metric]
- Approve button updates `st.session_state.approved_patches`
- `st.divider()` between patches

### Tab 4 — ℹ️ About

```python
# Simple static content
st.header("About This Project")
st.markdown("""
Built for: **Kaggle 5-Day AI Agents Capstone** — Freestyle Track
Author: **Sumit Gupta** (NSUT Delhi, @sumitgupta-ai)

Concepts demonstrated:
- ✅ Multi-Agent Systems (Google ADK)
- ✅ MCP Servers (FastMCP filesystem server)
- ✅ Agent Skills (SecretRedactor + DiffFormatter)
- ✅ Security Features (Directory lock + Prompt injection guard)
- ✅ Agent Orchestration (Sequential pipeline)

Tech Stack: Python 3.11 | Google ADK | Gemini 2.0 Flash | FastMCP | Streamlit
Cost: $0 (100% free tier)
""")
st.link_button("GitHub Repo", "https://github.com/Sumi-tgupta/smart-devops-auditor")
```

---

## 13. 🧠 BRAIN FOLDER — PRE-POPULATED INIT FILES

### 13.1 `brain/memory.md`

```markdown
# 🧠 Project Memory

## Last Updated: 2026-06-26

---

## ✅ COMPLETED
- Project scaffolding and brain initialization — 2026-06-26
- PROJECT_BIBLE.md generated — 2026-06-26

---

## 🔄 IN PROGRESS
- Environment setup (requirements.txt, .env) — Started 2026-06-26

---

## ⏳ PENDING / TODO
- [ ] Install dependencies: google-adk fastmcp streamlit python-dotenv — Priority: HIGH
- [ ] Get Gemini API key from aistudio.google.com — Priority: HIGH
- [ ] Build: mcp_servers/fs_server.py (filesystem MCP + directory lock) — Priority: HIGH
- [ ] Build: models/schemas.py (all dataclasses) — Priority: HIGH
- [ ] Build: skills/secret_redactor.py — Priority: HIGH
- [ ] Build: skills/diff_formatter.py — Priority: HIGH
- [ ] Build: agents/code_reviewer.py + prompts/code_reviewer_prompt.txt — Priority: HIGH
- [ ] Build: agents/secops_agent.py + prompts/secops_prompt.txt — Priority: HIGH
- [ ] Build: agents/patch_agent.py + prompts/patch_prompt.txt — Priority: HIGH
- [ ] Build: orchestrator/pipeline.py (connects all agents) — Priority: HIGH
- [ ] Build: ui/app.py (Streamlit: Scan + Report + Patches + About tabs) — Priority: MED
- [ ] Build: main.py (CLI entrypoint with --scan and --verify flags) — Priority: HIGH
- [ ] Create: sandbox-repo/vulnerable_samples/ (5 realistic Python files) — Priority: HIGH
- [ ] Create: notebooks/kaggle_submission.ipynb — Priority: CRITICAL
- [ ] Write: README.md — Priority: MED
- [ ] Test: full pipeline end-to-end on sample files — Priority: HIGH
- [ ] Submit to Kaggle — Priority: CRITICAL (deadline: July 6, 2026 11:59 PM PT)

---

## ❌ BLOCKERS
- None yet. All dependencies available on free tier.

---

## 📋 SESSION LOG

### Session 1 — 2026-06-26
- Did: Created project directory structure, generated PROJECT_BIBLE.md, initialized all brain files
- Changed: brain/ (all 4 files created), /home directory structure
- Next: Install dependencies, get Gemini API key, start with mcp_servers/fs_server.py
```

### 13.2 `brain/architecture.md`

```markdown
# 🏗️ Architecture

## Stack
- Frontend:   Streamlit 1.35+ (ui/app.py)
- Backend:    Python 3.11+
- AI Core:    Google ADK (google-adk) — LlmAgent + McpToolset
- LLM:        Gemini 2.0 Flash via Google AI Studio (free, 1500 req/day)
- MCP Layer:  FastMCP (fastmcp) — custom filesystem server
- Data:       Python dataclasses (models/schemas.py)
- Diff:       Python difflib stdlib — no install needed
- Secrets:    Python re stdlib — no install needed
- Env:        python-dotenv (.env file)

## Folder Map
```
smart-devops-auditor/
├── brain/                ← AI IDE context (DO NOT SCAN UNLESS TOLD)
├── sandbox-repo/         ← ONLY folder agents can read (MCP locked)
├── agents/               ← LlmAgent definitions (A, B, C)
│   └── prompts/          ← System prompt .txt files
├── skills/               ← FastMCP @tool decorated functions
├── mcp_servers/          ← FastMCP server + security config
├── orchestrator/         ← Sequential pipeline runner
├── models/               ← Shared dataclass schemas
├── ui/                   ← Streamlit frontend
├── tests/                ← Pytest test suite
├── notebooks/            ← Kaggle submission notebook
└── main.py               ← CLI entrypoint
```

## Data Flow
ScanRequest → Orchestrator → MCP reads files
→ SecretRedactor → PromptSanitizer (pre-LLM guards)
→ Agent A (logic findings) → Agent B (CWE findings)
→ Agent C (patches) → DiffFormatter
→ PipelineResult → UI/CLI

## Key Integrations
- GEMINI_API_KEY env var → Google AI Studio API
- SANDBOX_ROOT env var → MCP path lock (default: ./sandbox-repo)
- Python difflib.unified_diff() → git-format diffs
- Python re patterns → secret detection

## Security Boundaries
- MCP server validates ALL file paths against SANDBOX_ROOT at call time
- Secret redaction runs BEFORE every single LLM context injection
- Prompt sanitization strips injection patterns from code comments
- No agent can call any tool that writes to disk (read-only MCP tools only)

## Changelog
[Git-style entries added here as architecture evolves]
```

### 13.3 `brain/patterns.md`

```markdown
# 🔁 Patterns & Conventions

## Naming Conventions
- Files:       snake_case (code_reviewer.py, diff_formatter.py)
- Classes:     PascalCase (CodeFinding, PatchSuggestion, AuditReport)
- Functions:   snake_case, verb-first (run_scan, format_diff, redact_secrets)
- Constants:   UPPER_SNAKE_CASE (SANDBOX_ROOT, INJECTION_PATTERNS, SEVERITY_DEDUCTIONS)
- Enum values: UPPER_CASE (Severity.CRITICAL, FindingType.SQL_INJECTION)
- Agent names: lowercase with underscore (code_reviewer, secops, patch_artisan)

## Code Patterns

### Agent Pattern (ADK LlmAgent)
```python
from google.adk.agents import LlmAgent

def load_prompt(filename: str) -> str:
    with open(f"agents/prompts/{filename}", "r") as f:
        return f.read()

agent = LlmAgent(
    name="code_reviewer",
    model="gemini-2.0-flash",
    instruction=load_prompt("code_reviewer_prompt.txt"),
)
```

### Skill Pattern (FastMCP @tool)
```python
from fastmcp import FastMCP
mcp = FastMCP("auditor-skills")

@mcp.tool()
def redact_secrets(code: str) -> str:
    """Mask API keys, passwords, tokens before LLM processing."""
    # ... regex replacements
    return redacted_code
```

### MCP Path Validation Pattern — ALWAYS USE THIS
```python
from pathlib import Path

SANDBOX_ROOT = Path(os.getenv("SANDBOX_ROOT", "./sandbox-repo")).resolve()

def validate_path(requested: str) -> Path:
    target = Path(requested).resolve()
    if not str(target).startswith(str(SANDBOX_ROOT)):
        raise PermissionError(f"Access denied: {requested} is outside sandbox")
    if not target.exists():
        raise FileNotFoundError(f"File not found: {requested}")
    return target
```

### Pre-LLM Guard Pattern — NEVER SKIP
```python
# In orchestrator/pipeline.py — before EVERY agent call
clean_code = secret_redactor.redact_secrets(raw_code)
clean_code = prompt_sanitizer.clean(clean_code)
# Only now pass to agent
findings = await code_reviewer_agent.run(clean_code)
```

### JSON Response Validation Pattern
```python
# Agent responses need validation before dataclass construction
try:
    raw_response = agent.run(context)
    data = json.loads(raw_response)
    findings = [CodeFinding(**f) for f in data["findings"]]
except (json.JSONDecodeError, KeyError, TypeError) as e:
    pipeline_result.error_log.append(f"Agent A parse error: {e}")
    findings = []  # graceful degradation, never crash
```

## Anti-Patterns — NEVER DO THESE
- ❌ Never pass raw_code (with secrets) directly to any LLM
- ❌ Never trust file paths from LLM output — always validate against SANDBOX_ROOT
- ❌ Never `except: pass` — log to error_log
- ❌ Never hardcode GEMINI_API_KEY in any source file
- ❌ Never import brain/ files in any agent code — brain is for IDE context only
- ❌ Never skip JSON validation when parsing agent output

## Changelog
[Git-style entries added when conventions change]
```

### 13.4 `brain/decisions.md`

```markdown
# 🧭 Architecture Decision Records (ADR)

## ADR-001 — Gemini 2.0 Flash as LLM
- **Date:** 2026-06-26
- **Status:** Accepted
- **Context:** Project must be $0 cost. Need capable code analysis.
- **Decision:** Gemini 2.0 Flash via Google AI Studio (free, 1500 req/day, no credit card)
- **Rejected:** GPT-4o (paid), Claude Sonnet (paid), Llama local (too heavy for Kaggle)
- **Consequences:** Dependent on Google API uptime. Rate limited (sufficient for demo).

## ADR-002 — Streamlit as UI
- **Date:** 2026-06-26
- **Status:** Accepted
- **Context:** Need UI fast. 10-day deadline. Solo developer.
- **Decision:** Streamlit — Python-native, fast to build, runs in Kaggle notebooks
- **Rejected:** React+FastAPI (too slow to build), CLI-only (no visual diff), Gradio (layout control)
- **Consequences:** UI limited to Streamlit's component set. No custom diff syntax highlighting without CSS workarounds.

## ADR-003 — FastMCP over raw MCP SDK
- **Date:** 2026-06-26
- **Status:** Accepted
- **Context:** Need to build MCP server + skill tools without boilerplate.
- **Decision:** FastMCP — @mcp.tool() decorator pattern, minimal setup
- **Rejected:** Raw MCP SDK (more boilerplate), no MCP (violates Kaggle requirement)
- **Consequences:** Extra dependency (fastmcp). Actively maintained. Worth it.

## ADR-004 — Sequential Pipeline (A→B→C)
- **Date:** 2026-06-26
- **Status:** Accepted
- **Context:** Agent C needs output from both A and B. Agent B benefits from A's context.
- **Decision:** Sequential: A → B → C. Each output feeds the next as context.
- **Rejected:** Parallel A+B then C (more complex, less context sharing), Single agent (violates multi-agent requirement)
- **Consequences:** Longer runtime (sequential API calls). Acceptable for demo scale (~90s max).

## ADR-005 — Python dataclasses over Pydantic
- **Date:** 2026-06-26
- **Status:** Accepted
- **Context:** Need typed inter-agent data models.
- **Decision:** Python stdlib dataclasses — zero extra dependency, sufficient for MVP
- **Rejected:** Pydantic (better validation but extra dependency; overkill for this scope)
- **Consequences:** Manual JSON validation in orchestrator. Acceptable for MVP scope.

## ADR-006 — Sandbox-only MCP (read-only)
- **Date:** 2026-06-26
- **Status:** Accepted
- **Context:** Agent could potentially be directed to modify system files.
- **Decision:** MCP server exposes ONLY read tools (list_directory, read_file, get_file_stats). No write tools. Path locked to SANDBOX_ROOT.
- **Rejected:** Full filesystem MCP with write (security risk), No MCP (violates Kaggle requirement)
- **Consequences:** Users must manually apply approved patches (MVP limitation). Auto-apply deferred to post-MVP.
```

---

## 14. 📅 DEV TIMELINE (10 Days)

| Day | Date | Focus | Deliverable | Est. Hours |
|-----|------|-------|-------------|-----------|
| **1** | Jun 26 (Today) | Setup & Foundation | Brain init ✅, project structure, .env, pip install, mcp_config.json | 3h |
| **2** | Jun 27 | MCP Server | `mcp_servers/fs_server.py` — directory lock, read_file, list_directory | 4h |
| **3** | Jun 28 | Agent A | `agents/code_reviewer.py` + prompt — test on 1 sample file, structured JSON output | 4h |
| **4** | Jun 29 | Agent B | `agents/secops_agent.py` + prompt — CWE mapping, test detects SQLi + hardcoded secret | 4h |
| **5** | Jun 30 | Skills | `skills/secret_redactor.py` + `skills/diff_formatter.py` + prompt sanitizer in orchestrator | 3h |
| **6** | Jul 1 | Agent C | `agents/patch_agent.py` + prompt — generates valid patched code + explanation | 4h |
| **7** | Jul 2 | Orchestrator | `orchestrator/pipeline.py` — connects A→B→C, PipelineResult assembled end-to-end | 4h |
| **8** | Jul 3 | UI | `ui/app.py` + 3 components — Scan tab, Report tab, Patches tab working | 4h |
| **9** | Jul 4 | Polish + Testing | Sample vulnerable files, README.md, CLI, edge case fixes | 3h |
| **10** | Jul 5 | Kaggle Notebook | `notebooks/kaggle_submission.ipynb` — self-contained, all 5 concepts demonstrated | 4h |
| **+1** | Jul 6 | Submit | Final check, run notebook on Kaggle, submit before 11:59 PM PT | 1h |

**Total: ~38 hours over 10 days (~4h/day)**

### Critical Path
```
MCP Server → Agent A → Agent B → Skills → Agent C → Orchestrator → UI → Notebook → Submit
         (each step depends on previous)
```

### Risk Mitigation

| Risk | Probability | Mitigation |
|------|-------------|-----------|
| ADK multi-agent session complexity | MED | Fall back to manual async calls if ADK sessions prove tricky |
| Gemini API rate limits hit | LOW | 1500 req/day >> needed for dev (~30 scans/day) |
| Kaggle notebook env issues | MED | Test notebook on Kaggle.com on Day 9, not Day 10 |
| Agent JSON output unparseable | MED | Implement try/except + graceful error_log — never crash |
| July 5 deadline creep | LOW | Notebook is Day 10 task; buffer Jul 6 AM for fixes |

---

## 15. 🚀 QUICK START COMMANDS

### Complete Setup (Copy-Paste, Run in Order)

```bash
# ── 1. Create project ────────────────────────────────────────────────
mkdir smart-devops-auditor && cd smart-devops-auditor
git init

# ── 2. Python venv ───────────────────────────────────────────────────
python -m venv .venv
source .venv/bin/activate          # Linux / Mac
# .venv\Scripts\activate.bat       # Windows CMD
# .venv\Scripts\Activate.ps1       # Windows PowerShell

# ── 3. Install ALL dependencies ──────────────────────────────────────
pip install google-adk fastmcp streamlit python-dotenv
pip freeze > requirements.txt

# ── 4. Environment setup ─────────────────────────────────────────────
cat > .env.example << 'EOF'
# Get free key at: https://aistudio.google.com/
GEMINI_API_KEY=your_gemini_api_key_here

# Do NOT change this — it's the MCP security boundary
SANDBOX_ROOT=./sandbox-repo
EOF

cp .env.example .env
# Edit .env — replace "your_gemini_api_key_here" with real key

# ── 5. .gitignore ────────────────────────────────────────────────────
cat > .gitignore << 'EOF'
.env
.venv/
__pycache__/
*.pyc
*.pyo
.DS_Store
*.egg-info/
dist/
build/
.pytest_cache/
*.ipynb_checkpoints/
EOF

# ── 6. Create sandbox directory ──────────────────────────────────────
mkdir -p sandbox-repo/vulnerable_samples

# ── 7. Create brain folder files ─────────────────────────────────────
mkdir -p brain
# (Paste the content from Section 13 into each brain file)

# ── 8. Verify everything installed ───────────────────────────────────
python -c "import google.adk; import fastmcp; import streamlit; print('✅ All deps OK')"

# ── 9. Run Streamlit UI (after building ui/app.py on Day 7) ──────────
streamlit run ui/app.py

# ── 10. Run CLI scan (after building main.py on Day 9) ───────────────
python main.py --scan ./sandbox-repo
python main.py --verify
```

### `requirements.txt` (Exact Content)

```
google-adk>=1.0.0
fastmcp>=2.0.0
streamlit>=1.35.0
python-dotenv>=1.0.0
```

---

## 16. 📓 KAGGLE NOTEBOOK STRATEGY

### The Problem
Kaggle notebooks run in cloud compute. There's no pre-existing `./sandbox-repo/` directory.

### The Solution: Bundled Vulnerable Code
Create the sandbox files programmatically at the start of the notebook.

### Notebook Cell Structure

```python
# ═══════════════════════════════════════════════
# CELL 1: Install dependencies
# ═══════════════════════════════════════════════
!pip install google-adk fastmcp -q

# ═══════════════════════════════════════════════
# CELL 2: Create sandbox with sample vulnerable code
# ═══════════════════════════════════════════════
import os

os.makedirs("./sandbox-repo/vulnerable_samples", exist_ok=True)

# Sample 1 — CWE-798 (hardcoded credential) + CWE-89 (SQLi)
with open("./sandbox-repo/vulnerable_samples/auth.py", "w") as f:
    f.write("""
import sqlite3

# Hardcoded credentials — CWE-798
API_KEY = "sk-1234abcd5678efgh"
DB_PASSWORD = "admin123"

def authenticate_user(username, password):
    conn = sqlite3.connect("users.db")
    # SQL Injection — CWE-89
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    result = conn.execute(query).fetchone()
    return result is not None
""")

# Sample 2 — CWE-22 (path traversal)
with open("./sandbox-repo/vulnerable_samples/file_handler.py", "w") as f:
    f.write("""
def read_user_file(filename):
    # Path traversal — CWE-22
    # User could pass: ../../etc/passwd
    with open(f"/var/data/{filename}", "r") as f:
        return f.read()
""")

print("✅ Sandbox files created")

# ═══════════════════════════════════════════════
# CELL 3: ── CONCEPT 1: MCP SERVER ──
# ═══════════════════════════════════════════════
# [Code showing MCP server initialization and directory lock]

# ═══════════════════════════════════════════════
# CELL 4: ── CONCEPT 2: AGENT SKILLS ──
# ═══════════════════════════════════════════════
# [Code showing SecretRedactor and DiffFormatter skills]

# ═══════════════════════════════════════════════
# CELL 5: ── CONCEPT 3: MULTI-AGENT SYSTEM ──
# ═══════════════════════════════════════════════
# [Code showing Agent A definition + sample run]

# ═══════════════════════════════════════════════
# CELL 6: ── CONCEPT 4: SECURITY FEATURES ──
# ═══════════════════════════════════════════════
# [Code showing path validation block + prompt injection strip]

# ═══════════════════════════════════════════════
# CELL 7: ── CONCEPT 5: ORCHESTRATION ──
# ═══════════════════════════════════════════════
# [Code showing A→B→C pipeline run]

# ═══════════════════════════════════════════════
# CELL 8: FULL PIPELINE RUN + RESULTS
# ═══════════════════════════════════════════════
# [Final PipelineResult printed / displayed]
```

### Notebook Tips
- Each concept gets its OWN markdown cell above the code explaining what it demonstrates
- Add `# ── CONCEPT N: NAME ──` comment banners so evaluators scan quickly
- Keep each agent demonstration to a single focused cell
- Final cell prints `pipeline_result.summary()` clearly
- Runtime target: ≤ 10 minutes for all cells

---

*Project Bible v1.0 — Generated June 26, 2026*
*Smart DevOps & Code Auditor | Kaggle Freestyle Capstone | Sumit Gupta (@sumitgupta-ai)*
