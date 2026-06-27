# 🧠 Smart DevOps & Code Auditor

An automated multi-agent AI pipeline built using **Google ADK** and **Gemini 2.5 Flash** that scans local source code repositories for bugs and security vulnerabilities, maps threats to CWE categories, and generates surgical, copyable code patches.

---

## 🚀 Key Features

*   **Sequential Multi-Agent Pipeline (`A ➔ B ➔ C`)**:
    *   **Agent A (Code Reviewer)**: Scans for logic flaws, code smells, and performance bottlenecks.
    *   **Agent B (SecOps Engineer)**: Maps code weaknesses to CWE standards using Agent A's output as context.
    *   **Agent C (Patch Artisan)**: Generates minimal, surgical code corrections to resolve findings.
*   **API Key Rotation Pool**: pre-creates Agent/Runner instances per key at module load and rotates them by index to avoid 429 rate limit delays.
*   **Visual Streamlit Dashboard**: Renders glassmorphic metrics, dynamic alerts, and syntax-highlighted git diffs.
*   **Security Guardrails**:
    *   *Directory Path Lock*: Enforced lock restricting file reads strictly within the repository sandbox.
    *   *Secret Redactor*: Masking variables (passwords, tokens, API keys) before passing to any LLM.
    *   *Adversarial Comment Sanitizer*: Strips comment-based prompt injections before execution.

---

## 📂 Project Structure

```
smart-devops-auditor/
├── agents/
│   ├── prompts/          # Directives text files for Agents A, B, C
│   ├── code_reviewer.py  # Agent A wrapper definition
│   ├── secops_agent.py   # Agent B wrapper definition
│   ├── patch_agent.py    # Agent C wrapper definition
│   └── utils.py          # Custom KeyedGemini model and fence stripper
├── orchestrator/
│   └── pipeline.py       # Sequential coordinator with rate-limit retries
├── mcp_servers/
│   ├── fs_server.py      # Local read-only filesystem MCP server
│   └── mcp_config.json   # Filesystem server configuration rules
├── skills/
│   ├── secret_redactor.py# Regex-based pre-LLM credential masking
│   └── diff_formatter.py # Unified git-diff patch generator
├── models/
│   └── schemas.py        # Typed dataclass schemas (findings, requests, results)
├── ui/
│   ├── app.py            # Streamlit dashboard entrypoint
│   └── components/       # Dashboard tab panel layouts
├── tests/
│   ├── test_skills.py    # Secret redaction & diff formatter tests
│   └── test_pipeline.py  # Mocked sequential orchestration tests
├── main.py               # CLI scanner entrypoint
└── .env.example                  # Environment keys & sandbox root settings
```

---

## 🛠️ Installation & Setup

1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/Sumi-tgupta/smart-devops-auditor.git
    cd smart-devops-auditor
    ```

2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Environment Variables**:
    Create a `.env` file in the root directory:
    ```ini
    # Primary Gemini API key
    GEMINI_API_KEY=YOUR_GEMINI_API_KEY
    
    # Optional additional keys for rotation pool
    GEMINI_API_KEY_TWO=YOUR_GEMINI_API_KEY_TWO
    GEMINI_API_KEY_THREE=YOUR_GEMINI_API_KEY_THREE
    
    # Repository sandbox path
    SANDBOX_ROOT=./sandbox-repo
    ```

---

## 🏃 Run Instructions

### 1. Verification Check
Check system readiness and API connectivity:
```bash
python main.py --verify
```

### 2. Command Line Interface (CLI) Scan
Run a full scan on the sandbox repository and output findings directly:
```bash
python main.py --scan ./sandbox-repo
```

### 3. Streamlit Web Dashboard
Launch the visual interactive UI:
```bash
streamlit run ui/app.py
```
Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 🎓 Mapping to Google ADK Course Concepts

This repository is built for the Kaggle Capstone and explicitly demonstrates all 5 key concepts of the Google Agent Development Kit (ADK):

1.  **Agent Class**: Custom configurations using the standard ADK `Agent` class in `agents/*.py` (directing system instructions, setting models, and binding configurations).
2.  **Runner Execution**: Sessions state management in `agents/*.py` using `InMemorySessionService` and async runner streaming (`runner.run_async()`) to feed data between agents sequentially.
3.  **MCP Server**: Implements a secure local filesystem server `mcp_servers/fs_server.py` with read-only tools to strictly confine agents' file access boundary.
4.  **Pre-processing Guards**: Regex-based masking of API tokens (`skills/secret_redactor.py`) and regex sanitization of comments (`orchestrator/pipeline.py`) executed before LLM calls.
5.  **Post-processing Skills**: Invokes `skills/diff_formatter.py` using standard `difflib` to generate unified git-compatible diff patches from the raw LLM outputs.

---

## 🧪 Running Tests
Verify execution pipelines and skills offline:
```bash
pytest -v
```
# smart-devops-auditor
