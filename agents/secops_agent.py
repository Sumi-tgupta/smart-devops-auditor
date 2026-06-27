import os
import json
import uuid
import logging
from typing import List

from google.adk import Agent, Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part

from models.schemas import CodeFinding, FindingType, Severity, AgentSource
from agents.utils import strip_json_fences, KeyedGemini, get_all_keys

logger = logging.getLogger(__name__)

def load_prompt() -> str:
    """Loads system prompt from txt file."""
    prompt_path = os.path.join(os.path.dirname(__file__), "prompts", "secops_prompt.txt")
    with open(prompt_path, "r", encoding="utf-8") as f:
        return f.read()

# Define Runner Pool per key at module load
_api_keys = get_all_keys()
runners = []
for key in _api_keys:
    model_inst = KeyedGemini(api_key=key, model="gemini-2.5-flash")
    agent = Agent(
        name="secops_engineer",
        model=model_inst,
        instruction=load_prompt()
    )
    session_service = InMemorySessionService()
    runner = Runner(
        agent=agent,
        session_service=session_service,
        app_name="smart_devops_auditor"
    )
    runners.append(runner)

_current_runner_idx = 0

def get_current_runner_idx() -> int:
    try:
        import streamlit as st
        if "active_key_idx" not in st.session_state:
            st.session_state.active_key_idx = 0
        return st.session_state.active_key_idx % len(runners)
    except Exception:
        global _current_runner_idx
        return _current_runner_idx % len(runners)

def rotate_runner() -> None:
    try:
        import streamlit as st
        if "active_key_idx" not in st.session_state:
            st.session_state.active_key_idx = 0
        st.session_state.active_key_idx = (st.session_state.active_key_idx + 1) % len(runners)
    except Exception:
        global _current_runner_idx
        _current_runner_idx = (_current_runner_idx + 1) % len(runners)

async def analyze_code(code: str, file_path: str, reviewer_findings: List[CodeFinding]) -> List[CodeFinding]:
    """
    Runs SecOps Agent on source code.
    Detects security vulnerabilities and maps them to CWEs.
    Uses Code Reviewer findings as additional context.
    """
    idx = get_current_runner_idx()
    runner = runners[idx]
    session_service = runner.session_service
    
    # 1. Generate unique session ID
    session_id = str(uuid.uuid4())
    session = await session_service.create_session(
        app_name="smart_devops_auditor",
        user_id="default_user",

        session_id=session_id
    )
    
    # Convert previous findings to simple dict for prompt context
    reviewer_context = []
    for f in reviewer_findings:
        reviewer_context.append({
            "line_number": f.line_number,
            "line_end": f.line_end,
            "finding_type": f.finding_type.value,
            "severity": f.severity.value,
            "description": f.description
        })
        
    prompt = (
        f"Please analyze the following Python code for security vulnerabilities (CWE). "
        f"Use the logic review context if relevant, but focus ONLY on security issues.\n\n"
        f"File Path: {file_path}\n"
        f"Code:\n```python\n{code}\n```\n\n"
        f"Logic Review Context:\n{json.dumps(reviewer_context, indent=2)}"
    )
    message = Content(role="user", parts=[Part(text=prompt)])
    
    # 2. Collect only the last non-empty part.text
    response_text = ""
    async for event in runner.run_async(
        user_id="default_user",
        session_id=session.id,
        new_message=message
    ):
        if event.content and event.content.parts:
            for part in event.content.parts:
                if part.text:
                    response_text = part.text
                    
    if not response_text.strip():
        logger.warning("SecOps Agent returned empty response.")
        return []
        
    # 6. Strip JSON markdown fences
    cleaned_json = strip_json_fences(response_text)
    
    try:
        data = json.loads(cleaned_json)
        if not isinstance(data, list):
            if isinstance(data, dict) and "findings" in data:
                data = data["findings"]
            else:
                raise ValueError("Expected list of findings.")
    except Exception as e:
        logger.error(f"Failed to parse SecOps JSON response: {e}. Raw response: {response_text}")
        return []
        
    findings = []
    for item in data:
        if not isinstance(item, dict):
            continue
            
        # 4. Safe enum parsing
        try:
            finding_type = FindingType(item.get("finding_type"))
        except ValueError:
            finding_type = FindingType.INSECURE_CONFIG
            
        try:
            severity = Severity(item.get("severity"))
        except ValueError:
            severity = Severity.MEDIUM  # Default to MEDIUM for security vulnerabilities
            
        finding = CodeFinding(
            file_path=file_path,
            line_number=int(item.get("line_number", 0)),
            line_end=int(item.get("line_end", 0)),
            code_snippet=str(item.get("code_snippet", "")),
            finding_type=finding_type,
            severity=severity,
            description=str(item.get("description", "")),
            cwe_id=item.get("cwe_id"),
            cwe_name=item.get("cwe_name"),
            agent_source=AgentSource.SECOPS,
            confidence=float(item.get("confidence", 0.0))
        )
        findings.append(finding)
        
    return findings
