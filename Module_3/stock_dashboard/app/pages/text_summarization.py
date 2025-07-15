import streamlit as st
import sys
import os

# Debug sys.path and project root
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(project_root)
print(f"Project root (text_summarization.py): {project_root}")
print(f"sys.path (text_summarization.py): {sys.path}")

from src.data.summarization import summarize_text

st.title("Stock Text Summarization")

# Input text area
input_text = st.text_area(
    "Enter text to summarize (e.g., stock news, analysis, or reports)",
    height=200,
    placeholder="Paste your stock-related text here..."
)

# Summary parameters
max_length = st.slider("Maximum summary length (words)", 50, 300, 150)
min_length = st.slider("Minimum summary length (words)", 20, 100, 50)

# Summarize button
if st.button("Generate Summary"):
    if input_text.strip():
        with st.spinner("Generating summary..."):
            try:
                summary = summarize_text(input_text, max_length, min_length)
                st.subheader("Summary")
                st.write(summary)
            except Exception as e:
                st.error(f"Error generating summary: {str(e)}")
    else:
        st.warning("Please enter text to summarize")