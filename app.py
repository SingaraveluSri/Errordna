# app.py
import streamlit as st
from pathlib import Path
import google.generativeai as genai
from llm_analyzer import analyze_log_llm
from chatbot import chat_with_gemini   # <-- using your chatbot file
import time

# -------------------- GEMINI SETUP -------------------- #

genai.configure(api_key="AIzaSyB0B_5nh6l119AvObrLUs90rU6yIa9ZRh4")
gemini_model = genai.GenerativeModel("gemini-2.5-flash")


# -------------------- HELPERS -------------------- #

def load_css():
    css_path = Path("UI/style.css")
    if css_path.exists():
        with css_path.open() as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def load_sample_log(name: str) -> str:
    path = Path("sample_logs") / name
    if path.exists():
        return path.read_text()
    return ""


def build_analysis(log_text: str):
    return analyze_log_llm(log_text)



# -------------------- STREAMLIT UI -------------------- #

st.set_page_config(
    page_title="ErrorDNA – Log Intelligence (Local)",
    layout="wide",
    page_icon="🧬",
)

load_css()

# ChatGPT-style typing animation CSS
typing_css = """
<style>
.typing {
    display: inline-block;
}
.dot {
    height: 8px;
    width: 8px;
    margin: 0 2px;
    background-color: #ccc;
    border-radius: 50%;
    display: inline-block;
    animation: blink 1.4s infinite both;
}
.dot:nth-child(2) {
    animation-delay: 0.2s;
}
.dot:nth-child(3) {
    animation-delay: 0.4s;
}

@keyframes blink {
    0% { opacity: .2; }
    20% { opacity: 1; }
    100% { opacity: .2; }
}
</style>
"""
st.markdown(typing_css, unsafe_allow_html=True)

st.markdown("<h1 class='title'>🧬 ErrorDNA – Local Log Intelligence</h1>", unsafe_allow_html=True)
st.markdown(
    "<p class='subtitle'>Paste a log or upload a .log file to detect patterns, find root causes, and chat about issues.</p>",
    unsafe_allow_html=True,
)

# Initialize session state safely
if "analysis" not in st.session_state:
    st.session_state.analysis = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# -------------------- SIDEBAR -------------------- #

with st.sidebar:
    st.header("⚙️ Input Options")
    sample_choice = st.selectbox("Load sample log", ["None", "sample1.log", "sample2.log"])
    uploaded_file = st.file_uploader("Or upload a .log / .txt file", type=["log", "txt"])

# -------- LOG INPUT SECTION -------- #

st.markdown("<h3 class='section-title'>📄 Log Input</h3>", unsafe_allow_html=True)

log_text = ""
if uploaded_file:
    log_text = uploaded_file.read().decode("utf-8", errors="ignore")
elif sample_choice != "None":
    log_text = load_sample_log(sample_choice)

log_text = st.text_area(
    "Paste or inspect the log here:",
    value=log_text,
    height=280,
    label_visibility="collapsed"
)

analyze_clicked = st.button("🔍 Analyze Log", type="primary")


# -------- INSIGHTS BELOW INPUT -------- #

st.markdown("<h3 class='section-title'>🧠 Detected Insights</h3>", unsafe_allow_html=True)

if st.session_state.analysis is None:
    st.info("Run an analysis to see insights here.")
else:
    st.markdown(
        f"""
        <div class='card'>
            <div class='card-header'>LLM Analysis</div>
            <div class='card-body'>
                <pre style="white-space: pre-wrap;">{st.session_state.analysis}</pre>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )



# -------- RUN ANALYSIS -------- #

if analyze_clicked:
    if not log_text.strip():
        st.warning("Please paste a log or upload a file first.")
    else:
        st.session_state.analysis = build_analysis(log_text)
        st.rerun()


st.markdown("<hr>", unsafe_allow_html=True)

# -------------------- CHATBOT SECTION -------------------- #

st.markdown("## 💬 Chat with ErrorDNA (Local)")

# Show previous history
for role, msg in st.session_state.chat_history:
    st.chat_message(role).markdown(msg)

# Chat input
user_msg = st.chat_input("Ask ErrorDNA (powered by Gemini):")

if user_msg:

    # Store + show user message
    st.session_state.chat_history.append(("user", user_msg))
    st.chat_message("user").markdown(user_msg)

    # Create placeholder for assistant message
    placeholder = st.chat_message("assistant")
    typing_placeholder = placeholder.empty()

    # Show typing dots inside placeholder
    typing_placeholder.markdown(
        """
        <div class="typing">
            <span class="dot"></span>
            <span class="dot"></span>
            <span class="dot"></span>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Generate reply
    answer = chat_with_gemini(
        user_msg,
        st.session_state.analysis,
        st.session_state.chat_history
    )

    # Replace dots with final answer
    typing_placeholder.markdown(answer)

    # Store reply in history
    st.session_state.chat_history.append(("assistant", answer))
