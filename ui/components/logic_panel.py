import streamlit as st
from models.schemas import AgentSource

def render_logic_panel():
    """
    Renders Tab 2: Logic & Quality Findings (Agent A output).
    Displays code quality issues, code smells, and performance bottlenecks.
    """
    result = st.session_state.pipeline_result
    if not result:
        st.info("No scan results available. Execute a code scan from the Dashboard Overview tab.")
        return
        
    report = result.audit_report
    # Filter for Agent A findings
    logic_findings = [f for f in report.findings if f.agent_source == AgentSource.CODE_REVIEWER]
    
    if not logic_findings:
        st.success("🎉 No logic bugs or code smells detected by Agent A.")
        return
        
    st.markdown(f"### 🐞 Code Reviewer Findings ({len(logic_findings)})")
    st.markdown("Issues related to code architecture, syntax issues, performance bottlenecks, or clean code violations.")
    
    # Group findings by file path
    grouped = {}
    for f in logic_findings:
        grouped.setdefault(f.file_path, []).append(f)
        
    for file_path, findings in grouped.items():
        with st.expander(f"📁 {file_path} ({len(findings)} issues found)", expanded=True):
            for i, f in enumerate(findings):
                col_sev, col_det = st.columns([1, 6])
                
                with col_sev:
                    # Renders custom styled badge
                    sev_class = f.severity.value.lower()
                    st.markdown(f'<span class="badge badge-{sev_class}">{f.severity.value}</span>', unsafe_allow_html=True)
                    st.markdown(f"**Type**: `{f.finding_type.value}`")
                    st.markdown(f"**Confidence**: `{int(f.confidence * 100)}%`")
                    
                with col_det:
                    st.markdown(f"**Line {f.line_number} - {f.line_end}**")
                    st.markdown(f"**Description**: {f.description}")
                    
                    if f.code_snippet:
                        st.markdown("**Problematic Code Snippet:**")
                        st.code(f.code_snippet, language="python")
                        
                if i < len(findings) - 1:
                    st.markdown("---")
