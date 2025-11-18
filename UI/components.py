import streamlit as st

def render_header():
    st.title("🧬 ErrorDNA – Local Log Intelligence")

def render_log_input():
    return st.text_area("📄 Log Input", height=300)
