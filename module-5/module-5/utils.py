import streamlit as st
import json
from datetime import datetime
from typing import Dict, List, Any
import re

def save_thread_to_session(thread: Dict[str, Any]):
    """Save research thread to Streamlit session state"""
    if 'research_threads' not in st.session_state:
        st.session_state.research_threads = []
    
    # Check if thread already exists and update it
    thread_exists = False
    for i, existing_thread in enumerate(st.session_state.research_threads):
        if existing_thread['id'] == thread['id']:
            st.session_state.research_threads[i] = thread
            thread_exists = True
            break
    
    if not thread_exists:
        st.session_state.research_threads.append(thread)

def get_threads_from_session() -> List[Dict[str, Any]]:
    """Get all research threads from session state"""
    if 'research_threads' not in st.session_state:
        st.session_state.research_threads = []
    return st.session_state.research_threads

def format_timestamp(iso_timestamp: str) -> str:
    """Format ISO timestamp to readable format"""
    try:
        dt = datetime.fromisoformat(iso_timestamp.replace('Z', '+00:00'))
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except:
        return iso_timestamp

def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text to specified length"""
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."

def count_words(text: str) -> int:
    """Count words in text"""
    return len(text.split())

def extract_key_points(text: str, num_points: int = 5) -> List[str]:
    """Extract key points from text using simple heuristics"""
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
    
    # Simple scoring based on length and position
    scored_sentences = []
    for i, sentence in enumerate(sentences):
        score = len(sentence.split())  # Word count
        if i < len(sentences) * 0.3:  # Earlier sentences get bonus
            score *= 1.2
        scored_sentences.append((sentence, score))
    
    # Sort by score and return top points
    scored_sentences.sort(key=lambda x: x[1], reverse=True)
    return [sentence for sentence, _ in scored_sentences[:num_points]]

def export_thread_to_text(thread: Dict[str, Any]) -> str:
    """Export research thread to formatted text"""
    output = f"Research Thread: {thread['topic']}\n"
    output += f"Created: {format_timestamp(thread['created_at'])}\n"
    output += f"Last Updated: {format_timestamp(thread['last_updated'])}\n"
    output += "=" * 50 + "\n\n"
    
    for message in thread['messages']:
        output += f"{message['role'].upper()}:\n"
        output += f"{message['content']}\n"
        output += f"Timestamp: {format_timestamp(message['timestamp'])}\n"
        output += "-" * 30 + "\n\n"
    
    return output

def create_download_button(content: str, filename: str, button_text: str):
    """Create a download button for content"""
    st.download_button(
        label=button_text,
        data=content,
        file_name=filename,
        mime="text/plain"
    )

def display_metrics(research_content: str):
    """Display metrics about the research content"""
    word_count = count_words(research_content)
    char_count = len(research_content)
    reading_time = max(1, word_count // 200)  # Assume 200 words per minute
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Word Count", word_count)
    with col2:
        st.metric("Characters", char_count)
    with col3:
        st.metric("Est. Reading Time", f"{reading_time} min") 