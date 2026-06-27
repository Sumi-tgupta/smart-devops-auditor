import streamlit as st
import time
from models.schemas import ScanRequest
from orchestrator.pipeline import run_pipeline
from agents.utils import get_all_keys

def render_scan_panel(target_dir: str, file_exts: list):
    """
    Renders Tab 1: Dashboard Overview, including the scan trigger button,
    progress/loading indicator, metrics, and security score alerts.
    """
    st.markdown("### 🔍 Codebase Execution Control")
    
    # Pre-calculate keys information for user
    keys = get_all_keys()
    st.markdown(f"**API Key Pool Size**: `{len(keys)} key(s)` active for rotation.")
    
    col_btn, col_info = st.columns([1, 3])
    
    with col_btn:
        trigger_scan = st.button("🚀 Start Code Scan", disabled=st.session_state.scan_running)
        
    with col_info:
        if st.session_state.scan_running:
            st.info("Scan in progress... Sequencing Agent A → Agent B → Agent C.")
        else:
            st.write("Click to run sequential multi-agent review on target directory.")
            
    # Render any persistent scan errors or successes
    if "scan_error" in st.session_state and st.session_state.scan_error:
        st.error(st.session_state.scan_error)
    if "scan_success" in st.session_state and st.session_state.scan_success:
        st.success(st.session_state.scan_success)
        
    if trigger_scan:
        st.session_state.scan_running = True
        st.session_state.pipeline_result = None
        st.session_state.scan_error = None
        st.session_state.scan_success = None
        
        # Streamlit progress bar simulation
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            status_text.text("1. Reading codebase and preparing file payloads...")
            progress_bar.progress(10)
            
            # Setup request schema
            request = ScanRequest(
                target_dir=target_dir,
                file_extensions=file_exts,
                enable_secret_redaction=True,
                enable_prompt_sanitization=True
            )
            
            status_text.text("2. Invoking AI Agents (Code Reviewer, SecOps, Patch Artisan)...")
            progress_bar.progress(40)
            
            # Run pipeline (safely executed via ThreadPoolExecutor under the hood)
            result = run_pipeline(request)
            
            progress_bar.progress(90)
            status_text.text("3. Consolidating reports and formatting unified diff patches...")
            
            # Save to session state
            st.session_state.pipeline_result = result
            st.session_state.scan_success = f"Scan completed successfully in {result.total_runtime_seconds:.1f}s!"
            progress_bar.progress(100)
            status_text.empty()
            progress_bar.empty()
            
        except Exception as e:
            st.session_state.scan_error = f"Execution Error: {e}"
            
        st.session_state.scan_running = False
        st.rerun()
        
    # Render Scan Results Metrics if available
    result = st.session_state.pipeline_result
    if result:
        report = result.audit_report
        
        # Dynamic Alerting for Low Score (< 50)
        score = report.security_score
        if score < 50:
            # Extract unique CWE list dynamically
            cwes = []
            for f in report.findings:
                if f.cwe_id and f.cwe_name:
                    cwe_str = f"{f.cwe_id} ({f.cwe_name})"
                    if cwe_str not in cwes:
                        cwes.append(cwe_str)
            
            cwe_desc = ", ".join(cwes) if cwes else "unspecified security vulnerabilities"
            
            st.markdown(f"""
            <div class="danger-alert">
                <strong>🚨 Security Score: {score}/100</strong> — Urgent fixes needed, due to critical: <em>{cwe_desc}</em>
            </div>
            """, unsafe_allow_html=True)
            
        # Display Overview Statistics Cards
        col1, col2, col3, col4 = st.columns(4)
        
        # Verify total_lines_scanned is populated
        lines_scanned = report.total_lines_scanned if report.total_lines_scanned is not None else 0
        
        with col1:
            st.markdown(f"""
            <div class="glass-card">
                <div class="metric-value">{report.files_scanned}</div>
                <div class="metric-label">Files Scanned</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown(f"""
            <div class="glass-card">
                <div class="metric-value">{lines_scanned}</div>
                <div class="metric-label">Lines Checked</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col3:
            st.markdown(f"""
            <div class="glass-card">
                <div class="metric-value">{len(report.findings)}</div>
                <div class="metric-label">Findings Found</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col4:
            st.markdown(f"""
            <div class="glass-card">
                <div class="metric-value">{result.total_runtime_seconds:.1f}s</div>
                <div class="metric-label">Scan Runtime</div>
            </div>
            """, unsafe_allow_html=True)
            
        # Display Pipeline Result Errors if any occurred (e.g. key pool warnings)
        if result.error_log:
            st.warning("⚠️ Scanned completed with non-fatal warnings/errors:")
            for err in result.error_log:
                st.write(f"- {err}")
                
        # Brief description summaries
        st.markdown("### 📝 Analysis Summaries")
        
        st.markdown(f"**Agent A (Code Reviewer)**: {report.reviewer_summary}")
        st.markdown(f"**Agent B (SecOps Engineer)**: {report.secops_summary}")
    else:
        st.info("No scan result loaded. Use the configuration panel to start scanning.")
