# 🧭 Architecture Decision Records (ADR)

## ADR-001 — Gemini 2.0 Flash as LLM
- **Date:** 2026-06-26
- **Status:** Accepted
- **Context:** Project must operate at $0 cost. Need a capable code analysis model. Kaggle capstone built on Google's ADK course, so Google ecosystem preferred.
- **Decision:** Gemini 2.0 Flash via Google AI Studio. Free tier: 1,500 requests/day, 1M tokens/min. No credit card required. API key in 60 seconds.
- **Rejected Alternatives:**
  - GPT-4o / o3: Paid API, no free tier sufficient for code analysis
  - Claude Sonnet: Paid API
  - Llama 3 local: Too heavy for Kaggle notebook runtime; complex setup
  - Gemini 1.5 Pro: Higher quality but lower free quota
- **Consequences:** Dependent on Google AI Studio uptime. Hard rate limit at 1,500 req/day (sufficient: dev uses ~30 scans/day). Output quality slightly lower than frontier models but adequate for code review.

---

## ADR-002 — Streamlit as UI Framework
- **Date:** 2026-06-26
- **Status:** Accepted
- **Context:** Need a working UI within a 10-day deadline. Solo developer. Must run inside Kaggle notebook for demo.
- **Decision:** Streamlit — Python-native, minimal boilerplate, runs in notebooks via `streamlit run`, no separate frontend language needed.
- **Rejected Alternatives:**
  - React + FastAPI: Correct architecture but requires 3-4 days just for setup; too slow for this deadline
  - Gradio: Easier but less layout control; diff viewer would be inferior
  - CLI only: No visual diff viewer; evaluators get worse experience
  - Flask + Jinja2: More control than Streamlit but still slower than needed
- **Consequences:** UI constrained to Streamlit's component system. No custom syntax-highlighted diff without CSS hacks. Acceptable for MVP demo.

---

## ADR-003 — FastMCP over raw MCP Python SDK
- **Date:** 2026-06-26
- **Status:** Accepted
- **Context:** Need to build both an MCP server (filesystem access) and MCP skill tools. Speed matters; have 10 days total.
- **Decision:** FastMCP — decorator-based API (@mcp.tool()), minimal boilerplate, similar to Flask/FastAPI pattern already familiar.
- **Rejected Alternatives:**
  - Raw MCP Python SDK: More control but significantly more boilerplate; slower to build
  - No MCP (direct file reads): Would violate Kaggle's MCP requirement; cannot demonstrate the concept
  - External MCP hosting (paid services): Against zero-cost constraint
- **Consequences:** Extra pip dependency. FastMCP is actively maintained (MIT license). Risk: API changes between versions — pin to 2.x in requirements.txt.

---

## ADR-004 — Sequential Agent Pipeline (A → B → C)
- **Date:** 2026-06-26
- **Status:** Accepted
- **Context:** Three agents each produce output that feeds the next. Agent B benefits from Agent A's context (avoids re-flagging structural issues as security issues). Agent C needs both A and B output to generate comprehensive patches.
- **Decision:** Strict sequential pipeline: Code Reviewer → SecOps → Patch Artisan. Each agent's output is passed as context to the next.
- **Rejected Alternatives:**
  - Parallel A + B then C: Possible technically, but Agent B would miss structural context from A; more complex orchestration code
  - Single "super agent": Cannot demonstrate multi-agent system (violates Kaggle requirement); would be less specialized output
  - DAG/graph orchestration: Overkill for 3-agent linear flow; adds complexity without benefit at this scale
- **Consequences:** Longer per-file pipeline runtime (sequential API calls add latency). For 5-file sandbox: ~12-20s total. Acceptable for demo scale. If scanning large repos, parallelism would be needed (post-MVP).

---

## ADR-005 — Python Dataclasses over Pydantic
- **Date:** 2026-06-26
- **Status:** Accepted
- **Context:** Need typed inter-agent data models for CodeFinding, PatchSuggestion, PipelineResult. Want type safety without extra complexity.
- **Decision:** Python stdlib dataclasses — zero extra dependency. field(default_factory=...) for mutable defaults. Manual JSON validation in orchestrator.
- **Rejected Alternatives:**
  - Pydantic v2: Better validation + serialization but extra dependency; overkill for this scope
  - TypedDict: Less ergonomic than dataclasses for complex nested structures
  - Plain dicts: No type safety; error-prone when agent outputs don't match expected structure
- **Consequences:** Must write manual JSON validation in orchestrator (Pattern 5 in patterns.md). No automatic serialization — use dataclasses.asdict() when needed.

---

## ADR-006 — Read-Only MCP Tools (No Write Access)
- **Date:** 2026-06-26
- **Status:** Accepted
- **Context:** Agents could theoretically be directed to modify files. Even within the sandbox, write access creates risk. Kaggle requires demonstrating security features.
- **Decision:** MCP server exposes ONLY three read tools: list_directory, read_file, get_file_stats. No write_file, delete_file, or execute_command tools.
- **Rejected Alternatives:**
  - Full read+write MCP: Enables patch auto-apply but creates security risk even in sandbox; agents could corrupt sample files
  - Write with confirmation: More complex orchestration; outside MVP scope
- **Consequences:** Users must manually apply approved patches in MVP (copy from diff viewer). Auto-apply deferred to post-MVP stretch goal (F16).

---

## ADR-007 — Sandbox-Only File Access (Hard MCP Lock)
- **Date:** 2026-06-26
- **Status:** Accepted
- **Context:** Security requirement: agents must not be able to read sensitive system files, user home directory, or any file outside the designated code sandbox.
- **Decision:** Path validation using Path.resolve() to canonicalize the path before checking against SANDBOX_ROOT. Prevents symlink attacks and ../../../ traversal. Implemented at MCP tool level, not just config level.
- **Rejected Alternatives:**
  - Config-only restriction: MCP config can be bypassed if agent constructs clever paths; code-level validation is stronger
  - No restriction: Obvious security risk; violates Kaggle's security feature requirement
- **Consequences:** Agents are completely sandboxed. If evaluators want to scan code outside sandbox, they must explicitly add it there. This is by design.

---

## ADR-008 — Secret Redaction at Code Level (Not Prompt Level)
- **Date:** 2026-06-26
- **Status:** Accepted
- **Context:** Secrets in scanned code could leak into LLM context. Want to protect these before any LLM sees them.
- **Decision:** Apply SecretRedactor skill before constructing any agent prompt context. Regex-based replacement of known secret patterns with [REDACTED-X] tokens.
- **Rejected Alternatives:**
  - Prompt-level instruction ("don't repeat secrets"): LLMs are not reliable at following such instructions; not a technical control
  - Post-processing (remove from output): Too late; secrets already in LLM context
  - Skip entirely: Violates security requirement; makes demo less impressive
- **Consequences:** Redacted tokens ([REDACTED-API-KEY]) remain visible to Agent A/B/C, which may report them as "HARDCODED_SECRET" findings. This is correct behavior — the finding is valid; only the actual value is masked.

---

## ADR-009 — Gemini 2.5 Flash for Free Tier Quota Stability
- **Date:** 2026-06-27
- **Status:** Accepted
- **Context:** Gemini 2.0 Flash free tier metric requests in standard trial keys frequently report `limit: 0` or are fully exhausted.
- **Decision:** Switch to `gemini-2.5-flash` model which has verified active free tier quota and supports same generation parameters.
- **Rejected Alternatives:**
  - `gemini-1.5-flash`: Returns `404 NOT_FOUND` for v1beta in ADK default calls.
- **Consequences:** Code scanning completes successfully and generates findings without throwing 429 quota exceptions.

---

## ADR-010 — Escaping Prompt Curly Braces for ADK Compatibility
- **Date:** 2026-06-27
- **Status:** Accepted
- **Context:** The Google ADK framework automatically parses any instruction curly-brace blocks (e.g. `{user_input}`) matching valid Python identifiers as session context variables. If not found in the session state, a `KeyError` is thrown, halting execution.
- **Decision:** Use square brackets (e.g. `[user_input]`, `[user_id]`) instead of curly braces for syntax and code patterns in prompt text files.
- **Rejected Alternatives:**
  - Populating session state with empty dummy values: fragile and requires maintaining variables list at orchestrator level.
- **Consequences:** Completely prevents interpolation KeyErrors in ADK instructions.
