# 🏗️ Architecture

## Stack
- Frontend:    Streamlit 1.35+ (ui/app.py)
- Backend:     Python 3.11+
- AI Core:     Google ADK (google-adk) — LlmAgent + McpToolset
- LLM:         Gemini 2.0 Flash via Google AI Studio (free tier, 1500 req/day)
- MCP Layer:   FastMCP (fastmcp) — local filesystem server
- Data Models: Python dataclasses (models/schemas.py)
- Diff Engine: Python difflib — stdlib, no install
- Regex/Scan:  Python re — stdlib, no install
- Env:         python-dotenv (.env file)

## Folder Map
```
smart-devops-auditor/
├── brain/                ← AI IDE context (4 files, NEVER scan unless told)
├── sandbox-repo/         ← ONLY folder agents can read (MCP hard boundary)
│   └── vulnerable_samples/
├── agents/               ← LlmAgent definitions (3 agents: A, B, C)
│   └── prompts/          ← System prompt .txt files (not hardcoded in .py)
├── skills/               ← FastMCP @tool decorated custom skills
├── mcp_servers/          ← FastMCP server + security config JSON
├── orchestrator/         ← Sequential pipeline: ScanRequest → PipelineResult
├── models/               ← Shared Python dataclass schemas
├── ui/                   ← Streamlit frontend + 3 component files
│   └── components/
├── tests/                ← Pytest test suite
├── notebooks/            ← Kaggle submission (.ipynb)
└── main.py               ← CLI entrypoint
```

## Data Flow
```
ScanRequest (target_dir, extensions, guardrails)
  └─► Orchestrator
        ├─► MCP: list_directory() → file list
        └─► For each file:
              ├─► MCP: read_file() → raw_code
              ├─► SecretRedactor.run(raw_code) → redacted_code     [SKILL, pre-LLM]
              ├─► PromptSanitizer.clean(redacted_code) → clean_code [in orchestrator]
              ├─► Agent A: code_reviewer → CodeFinding[] (logic, smells, perf)
              ├─► Agent B: secops → CodeFinding[] (CWE-89, CWE-798, CWE-22, CWE-327)
              ├─► Agent C: patch_artisan → PatchSuggestion[] (original+patched+explanation)
              └─► DiffFormatter.format() → adds unified_diff to each patch [SKILL, post-LLM]
  └─► PipelineResult(audit_report, patches, security_score, error_log)
  └─► Streamlit UI / CLI output
```

## Key Integrations
- GEMINI_API_KEY (env var) → Google AI Studio → Gemini 2.0 Flash
- SANDBOX_ROOT (env var, default: ./sandbox-repo) → MCP path lock
- difflib.unified_diff() → git-compatible diff output
- re.sub() with REDACTION_PATTERNS → secret masking
- No external database, no paid services, no cloud storage

## Security Boundaries
1. MCP server validates ALL file paths against SANDBOX_ROOT at call time
   - Uses Path.resolve() to prevent ../../../ traversal bypasses
   - Raises PermissionError immediately — agent gets error, not file contents
2. Secret redaction runs BEFORE every LLM context injection
   - Patterns: API_KEY, password, token, secret, private_key, access_key
3. Prompt sanitization strips adversarial code comments
   - Patterns: "ignore previous", "system:", "forget", "jailbreak", "new instructions"
4. MCP tools are READ-ONLY — no write/delete tools exposed to any agent
5. Guardrails hardcoded ON in sidebar — user cannot disable them

## Agent Definitions
| Agent | Name | Gemini Role | Input | Output |
|-------|------|------------|-------|--------|
| A | code_reviewer | Expert code reviewer — logic, smells, performance | clean_code + file_path | List[CodeFinding] severity LOW/MED/HIGH |
| B | secops_engineer | Senior security engineer — CWE threat hunting only | clean_code + file_path + A's findings | List[CodeFinding] severity MED/HIGH/CRITICAL with CWE IDs |
| C | patch_artisan | Patch generator — minimal, focused fixes | clean_code + all_findings + file_path | List[PatchSuggestion] with original+patched+explanation |

## Changelog
---
### [2026-06-26 | SESSION-1 | OPERATION: Create]

**File(s) Affected:** all brain files, project root structure
**Status:** ✅ Done

#### BEFORE
> NEW PROJECT — nothing existed

#### AFTER
> Project scaffolded, brain initialized, PROJECT_BIBLE.md generated

#### REASON
> Kaggle 5-Day AI Agents Capstone project kick-off. Deadline July 6, 2026.

#### REMAINING
> Build all modules. See memory.md for full task list.
---
