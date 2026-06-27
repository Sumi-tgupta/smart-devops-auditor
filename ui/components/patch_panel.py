import streamlit as st
from models.schemas import PatchStatus

def render_patch_panel():
    """
    Renders Tab 4: Surgical Patches (Agent C output).
    Displays the generated code patches, explanations, confidence scores, and diff blocks.
    """
    result = st.session_state.pipeline_result
    if not result:
        st.info("No scan results available. Execute a code scan from the Dashboard Overview tab.")
        return
        
    patches = result.patches
    
    if not patches:
        st.success("🎉 No patch suggestions needed (or generated).")
        return
        
    st.markdown(f"### 🛠️ Patch Artisan Suggestions ({len(patches)})")
    st.markdown("Surgical corrections targeted at solving the detected security and code quality vulnerabilities.")
    
    # Group patches by target file
    grouped = {}
    for p in patches:
        # Get the file path from the associated finding
        file_path = p.finding.file_path
        grouped.setdefault(file_path, []).append(p)
        
    for file_path, file_patches in grouped.items():
        with st.expander(f"📁 Patches for {file_path} ({len(file_patches)} patches)", expanded=True):
            for i, p in enumerate(file_patches):
                finding = p.finding
                
                col_met, col_diff = st.columns([1, 4])
                
                with col_met:
                    st.markdown(f"**Patch ID**: `{p.patch_id}`")
                    st.markdown(f"**Target Finding**: `{finding.finding_type.value}`")
                    st.markdown(f"**Target Line**: `Line {finding.line_number}`")
                    st.markdown(f"**Confidence**: `{int(p.confidence_score * 100)}%`")
                    st.markdown(f"**Status**: `{p.status.value}`")
                    
                with col_diff:
                    st.markdown(f"**Artisan Explanation**: {p.explanation}")
                    
                    if p.unified_diff:
                        st.markdown("**Unified Diff Patch:**")
                        # st.code has built-in copy, which matches the user request perfectly
                        st.code(p.unified_diff, language="diff")
                    else:
                        st.markdown("**Original Snippet:**")
                        st.code(p.original_code, language="python")
                        st.markdown("**Suggested Fix Snippet:**")
                        st.code(p.patched_code, language="python")
                        
                if i < len(file_patches) - 1:
                    st.markdown("---")
