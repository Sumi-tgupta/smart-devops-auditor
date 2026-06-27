import os
import json
import uuid
import logging
from typing import List

from google.adk import Agent, Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part

from models.schemas import CodeFinding, PatchSuggestion, PatchStatus
from agents.utils import strip_json_fences, KeyedGemini, get_all_keys

logger = logging.getLogger(__name__)

def load_prompt() -> str:
    """Loads system prompt from txt file."""
    prompt_path = os.path.join(os.path.dirname(__file__), "prompts", "patch_prompt.txt")
    with open(prompt_path, "r", encoding="utf-8") as f:
        return f.read()

# Define Runner Pool per key at module load
_api_keys = get_all_keys()
runners = []
for key in _api_keys:
    model_inst = KeyedGemini(api_key=key, model="gemini-2.5-flash")
    agent = Agent(
        name="patch_artisan",
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

async def generate_patches(code: str, file_path: str, findings: List[CodeFinding]) -> List[PatchSuggestion]:
    """
    Runs Patch Artisan Agent on source code.
    Generates minimal patches to address each CodeFinding.
    """
    if not findings:
        return []
        
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
    
    # Convert findings list into simplified format for agent prompt context
    findings_context = []
    for f in findings:
        findings_context.append({
            "id": f.id,
            "line_number": f.line_number,
            "line_end": f.line_end,
            "finding_type": f.finding_type.value,
            "severity": f.severity.value,
            "description": f.description,
            "cwe_id": f.cwe_id,
            "code_snippet": f.code_snippet
        })
        
    prompt = (
        f"Please generate minimal, surgical patches for the following findings. "
        f"Make sure to preserve surrounding code structure and indentation.\n\n"
        f"File Path: {file_path}\n"
        f"Source Code:\n```python\n{code}\n```\n\n"
        f"Findings to Address:\n{json.dumps(findings_context, indent=2)}"
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
        logger.warning("Patch Artisan Agent returned empty response.")
        return []
        
    # 6. Strip JSON markdown fences
    cleaned_json = strip_json_fences(response_text)
    
    try:
        data = json.loads(cleaned_json)
        if not isinstance(data, list):
            if isinstance(data, dict) and "patches" in data:
                data = data["patches"]
            else:
                raise ValueError("Expected list of patches.")
    except Exception as e:
        logger.error(f"Failed to parse Patch Artisan JSON response: {e}. Raw response: {response_text}")
        return []
        
    patches = []
    for item in data:
        if not isinstance(item, dict):
            continue
            
        finding_id = item.get("finding_id")
        # Match back to original CodeFinding object
        matching_finding = next((f for f in findings if f.id == finding_id), None)
        if not matching_finding:
            logger.warning(f"Patch Artisan returned patch for unknown finding_id: {finding_id}")
            continue
            
        patch = PatchSuggestion(
            finding=matching_finding,
            original_code=str(item.get("original_code", "")),
            patched_code=str(item.get("patched_code", "")),
            explanation=str(item.get("explanation", "")),
            confidence_score=float(item.get("confidence_score", 0.0)),
            status=PatchStatus.PENDING
        )
        patches.append(patch)
        
    return patches
