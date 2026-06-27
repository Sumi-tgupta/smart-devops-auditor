import os
import sys
import streamlit as st
from dotenv import load_dotenv

# Add parent directory of ui/ to sys.path to allow absolute imports under Streamlit
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load environment variables
load_dotenv()

# Set up page configurations
st.set_page_config(
    page_title="Smart DevOps & Code Auditor",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for premium glassmorphism dark theme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@400;500;600;700&display=swap');

    /* Global styling */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        background-color: #0b0f19;
        color: #f1f5f9;
    }
    
    /* Title typography */
    h1, h2, h3, h4 {
        font-family: 'Outfit', sans-serif;
        color: #f8fafc;
        font-weight: 600;
    }
    
    /* Header Gradient styling */
    .header-container {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.15) 0%, rgba(139, 92, 246, 0.15) 100%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 24px;
        backdrop-filter: blur(12px);
    }
    
    .header-title {
        font-size: 2.5rem;
        background: linear-gradient(90deg, #818cf8, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        font-weight: 700;
    }
    
    .header-subtitle {
        color: #94a3b8;
        font-size: 1.1rem;
        margin-top: 8px;
        margin-bottom: 0;
    }
    
    /* Glassmorphic Cards */
    .glass-card {
        background: rgba(30, 41, 59, 0.45);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 16px;
        backdrop-filter: blur(8px);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .glass-card:hover {
        transform: translateY(-2px);
        border-color: rgba(99, 102, 241, 0.3);
    }
    
    /* Metric styling */
    .metric-value {
        font-size: 2.2rem;
        font-weight: 700;
        font-family: 'Outfit', sans-serif;
        color: #f8fafc;
        margin: 0;
        line-height: 1.2;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-top: 4px;
    }
    
    /* Severity badges */
    .badge {
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.8rem;
        font-weight: 600;
        display: inline-block;
        text-transform: uppercase;
    }
    .badge-critical { background-color: rgba(239, 68, 68, 0.2); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.4); }
    .badge-high { background-color: rgba(249, 115, 22, 0.2); color: #fb923c; border: 1px solid rgba(249, 115, 22, 0.4); }
    .badge-medium { background-color: rgba(234, 179, 8, 0.2); color: #facc15; border: 1px solid rgba(234, 179, 8, 0.4); }
    .badge-low { background-color: rgba(59, 130, 246, 0.2); color: #60a5fa; border: 1px solid rgba(59, 130, 246, 0.4); }
    
    /* Custom Streamlit adjustments */
    div[data-testid="stSidebar"] {
        background-color: #090d16;
        border-right: 1px solid rgba(255, 255, 255, 0.06);
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
        color: white;
        border: none;
        padding: 10px 24px;
        border-radius: 8px;
        font-weight: 600;
        transition: opacity 0.2s;
        width: 100%;
    }
    .stButton>button:hover {
        opacity: 0.9;
        color: white;
    }
    
    /* Low-score banner styling */
    .danger-alert {
        background-color: rgba(220, 38, 38, 0.15);
        border: 1px solid rgba(220, 38, 38, 0.4);
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 24px;
        color: #fca5a5;
    }
</style>
""", unsafe_allow_html=True)

# 1. Initialize Streamlit Session State variables
if "pipeline_result" not in st.session_state:
    st.session_state.pipeline_result = None
if "scan_running" not in st.session_state:
    st.session_state.scan_running = False
if "active_key_idx" not in st.session_state:
    st.session_state.active_key_idx = 0

# Header Container
st.markdown("""
<div class="header-container">
    <div class="header-title">🧠 Smart DevOps & Code Auditor</div>
    <div class="header-subtitle">Multi-agent AI pipeline sequencing Code Reviewer → SecOps → Patch Artisan for secure code automation</div>
</div>
""", unsafe_allow_html=True)

# Sidebar Configuration
st.sidebar.markdown("### ⚙️ Scan Configuration")

sandbox_root = os.getenv("SANDBOX_ROOT", "./sandbox-repo")
target_dir = st.sidebar.text_input("📁 Target Directory Path", value=sandbox_root)
file_exts = st.sidebar.multiselect("📄 File Extensions", options=[".py", ".js", ".go", ".ts", ".html"], default=[".py"])

st.sidebar.markdown("---")
st.sidebar.markdown("### 🛡️ Active Guardrails")

# Visual feedback for our required safety features
st.sidebar.info("""
🔒 **Directory Lock**: MCP strictly restricts all access to sandbox directory path.  
🔍 **Secret Redaction**: Credentials masked before LLM context calls.  
🚫 **Prompt Sanitizer**: Comment-based adversarial injection patterns removed.
""")

# Import Tab panels
from ui.components.scan_panel import render_scan_panel
from ui.components.logic_panel import render_logic_panel
from ui.components.secops_panel import render_secops_panel
from ui.components.patch_panel import render_patch_panel

# 4 Primary Tabs (No nested st.tabs)
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Dashboard Overview", 
    "🐞 Logic & Quality Findings", 
    "🔒 Security Vulnerabilities (CWE)", 
    "🛠️ Surgical Patches"
])

with tab1:
    render_scan_panel(target_dir, file_exts)

with tab2:
    render_logic_panel()

with tab3:
    render_secops_panel()

with tab4:
    render_patch_panel()
