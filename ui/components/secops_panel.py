import streamlit as st
from models.schemas import AgentSource

def render_secops_panel():
    """
    Renders Tab 3: Security Vulnerabilities (CWE) (Agent B output).
    Displays security weaknesses, hardcoded credentials, injection vulnerabilities, etc.
    """
    result = st.session_state.pipeline_result
    if not result:
        st.info("No scan results available. Execute a code scan from the Dashboard Overview tab.")
        return
        
    report = result.audit_report
    # Filter for Agent B findings
    sec_findings = [f for f in report.findings if f.agent_source == AgentSource.SECOPS]
    
    if not sec_findings:
        st.success("🎉 No security vulnerabilities detected by Agent B.")
        return
        
    st.markdown(f"### 🔒 SecOps Security Findings ({len(sec_findings)})")
    st.markdown("Weaknesses mapped to Common Weakness Enumeration (CWE) standards.")
    
    # Group findings by file path
    grouped = {}
    for f in sec_findings:
        grouped.setdefault(f.file_path, []).append(f)
        
    for file_path, findings in grouped.items():
        with st.expander(f"📁 {file_path} ({len(findings)} security flaws)", expanded=True):
            for i, f in enumerate(findings):
                col_sev, col_det = st.columns([1, 6])
                
                with col_sev:
                    # Renders custom styled badge
                    sev_class = f.severity.value.lower()
                    st.markdown(f'<span class="badge badge-{sev_class}">{f.severity.value}</span>', unsafe_allow_html=True)
                    st.markdown(f"**CWE**: `{f.cwe_id}`")
                    st.markdown(f"**CWE Name**: `{f.cwe_name}`")
                    st.markdown(f"**Confidence**: `{int(f.confidence * 100)}%`")
                    
                with col_det:
                    st.markdown(f"**Line {f.line_number} - {f.line_end}**")
                    st.markdown(f"**Description**: {f.description}")
                    
                    if f.code_snippet:
                        st.markdown("**Vulnerable Code:**")
                        st.code(f.code_snippet, language="python")
                        
                if i < len(findings) - 1:
                    st.markdown("---")
