"""
Streamlit Web User Interface for AI Research Assistant.
Features centered input layout, live progress orchestration, and structured tabbed output.
"""

from pathlib import Path
import sys

# -----------------------------------------------------------------------------
# Module Namespace Conflict Resolution
# When running `streamlit run backend/app/app.py`, Python registers the script itself
# as the top-level module 'app' in sys.modules, masking the actual package directory 'app'.
# We clean sys.modules and properly register 'backend' and 'app' packages.
# -----------------------------------------------------------------------------
CURRENT_FILE = Path(__file__).resolve()
APP_DIR = CURRENT_FILE.parent             # .../backend/app
BACKEND_DIR = APP_DIR.parent              # .../backend

# Remove colliding top-level 'app' module if it points to this single file
if "app" in sys.modules and getattr(sys.modules["app"], "__file__", None) == str(CURRENT_FILE):
    del sys.modules["app"]

# Ensure backend root is the primary search path
if str(BACKEND_DIR) in sys.path:
    sys.path.remove(str(BACKEND_DIR))
sys.path.insert(0, str(BACKEND_DIR))

import streamlit as st
from app.models.research_state import ResearchState
from app.workflow.container import create_workflow

st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Custom CSS for styling and centering
st.markdown(
    """
    <style>
    .main-title {
        text-align: center;
        font-size: 2.6rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        text-align: center;
        color: #6c757d;
        font-size: 1.15rem;
        margin-bottom: 2rem;
    }
    .stTextInput > div > div > input {
        font-size: 1.1rem;
        padding: 12px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Centered Header
st.markdown('<div class="main-title">🤖 AI Multi-Agent Research Assistant</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">Powered by LangGraph, Google Gemini, and Clean Multi-Agent Architecture</div>',
    unsafe_allow_html=True,
)

# Initialize workflow in session state
if "workflow" not in st.session_state:
    st.session_state.workflow = create_workflow()
if "last_state" not in st.session_state:
    st.session_state.last_state = None

# Centered Input Section using 3 Columns
_, center_col, _ = st.columns([1, 2.5, 1])

with center_col:
    with st.container():
        topic_input = st.text_input(
            "Enter Research Topic",
            value="",
            placeholder="e.g. Artificial Intelligence in Healthcare, Quantum Computing, Climate Tech...",
            help="Type the topic you wish the multi-agent system to investigate.",
        )
        start_btn = st.button("🚀 Start Deep Research", type="primary", use_container_width=True)

# Execution Logic
if start_btn:
    if not topic_input.strip():
        st.warning("⚠️ Please enter a research topic to begin.")
    else:
        st.session_state.last_state = None
        initial_state = ResearchState(topic=topic_input.strip())

        progress_container = st.container()
        with progress_container:
            progress_bar = st.progress(5, text="Initiating multi-agent workflow...")
            status = st.status(f"Conducting research on: **{topic_input.strip()}**", expanded=True)

            with status:
                st.write("📋 **PlannerAgent**: Decomposing topic into logical research sections...")
                progress_bar.progress(20, text="PlannerAgent formulating plan...")

                # Execute full LangGraph pipeline
                final_state = st.session_state.workflow.run(initial_state)
                st.session_state.last_state = final_state

                st.write(f"🔍 **SearchAgent**: Retrieved facts for {len(final_state.search_results)} sections from Wikipedia.")
                progress_bar.progress(40, text="SearchAgent retrieved sources...")

                st.write(f"📖 **ReaderAgent**: Extracted and normalized raw facts.")
                progress_bar.progress(60, text="ReaderAgent processed findings...")

                st.write(f"✅ **FactCheckerAgent**: Verified factual consistency across all sections.")
                progress_bar.progress(80, text="FactCheckerAgent verified claims...")

                st.write(f"📝 **SummarizerAgent**: Synthesized findings into a cohesive core summary.")
                st.write(f"✍️ **WriterAgent**: Formatted final research report in Markdown.")
                progress_bar.progress(100, text="Research complete!")

                status.update(label="🎉 Research Workflow Completed Successfully!", state="complete", expanded=False)

# Render Results
if st.session_state.last_state is not None:
    state = st.session_state.last_state

    st.markdown("---")
    st.subheader(f"📊 Results: {state.topic}")

    tab_report, tab_summary, tab_sections, tab_logs = st.tabs(
        ["📄 Final Report", "📌 Executive Summary", "🗂️ Sections Breakdown", "📜 Event Logs"]
    )

    with tab_report:
        st.markdown(state.report or "_No report generated._")
        if state.report:
            st.download_button(
                label="📥 Download Markdown Report",
                data=state.report,
                file_name=f"{state.topic.replace(' ', '_').lower()}_report.md",
                mime="text/markdown",
            )

    with tab_summary:
        st.markdown("### Synthesized Executive Summary")
        st.info(state.final_summary or "No summary available.")

    with tab_sections:
        st.markdown("### Research Plan & Section Verification")
        for idx, section in enumerate(state.plan, 1):
            with st.expander(f"Section {idx}: {section}"):
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown("**📖 Reader Extracted Notes**")
                    st.write(state.read_results.get(section, "No data extracted."))
                with c2:
                    st.markdown("**✅ Fact-Checked Notes**")
                    st.write(state.verified_results.get(section, "No verified data."))

    with tab_logs:
        st.markdown("### Execution Activity Stream")
        for log in state.logs:
            timestamp_str = log.timestamp.strftime("%H:%M:%S")
            st.code(f"[{timestamp_str}] [{log.agent.value.upper()}] {log.message}", language="log")
