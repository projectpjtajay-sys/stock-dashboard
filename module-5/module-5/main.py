import streamlit as st
import os
from config import Config
from claude_client import ClaudeClient
from openai_client import OpenAIClient
from utils import (
    save_thread_to_session, 
    get_threads_from_session, 
    format_timestamp, 
    export_thread_to_text,
    create_download_button,
    display_metrics
)

# Configure Streamlit page
st.set_page_config(
    page_title="GenAI Research & Writing Assistant",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    st.title("🧠 GenAI Research & Writing Assistant")
    st.markdown("*Powered by Claude for Research & OpenAI for Summarization*")
    
    # Check API keys
    missing_keys = Config.validate_keys()
    if missing_keys:
        st.error(f"Missing API keys: {', '.join(missing_keys)}")
        st.info("Please set your API keys in a .env file or environment variables:")
        st.code("""
ANTHROPIC_API_KEY=your_claude_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
        """)
        st.stop()
    
    # Initialize clients
    try:
        claude_client = ClaudeClient()
        openai_client = OpenAIClient()
    except Exception as e:
        st.error(f"Error initializing clients: {str(e)}")
        st.stop()
    
    # Sidebar for navigation and thread management
    with st.sidebar:
        st.header("Navigation")
        page = st.selectbox(
            "Choose Page",
            ["🔍 Research Assistant", "📝 Summary Generator", "📚 Thread Manager", "⚙️ Settings"]
        )
        
        st.divider()
        
        # Recent threads
        threads = get_threads_from_session()
        if threads:
            st.header("Recent Research")
            for thread in threads[-5:]:  # Show last 5 threads
                if st.button(f"📄 {thread['topic'][:20]}...", key=f"thread_{thread['id']}"):
                    st.session_state.selected_thread = thread
                    st.rerun()
    
    # Main content area
    if page == "🔍 Research Assistant":
        research_page(claude_client)
    elif page == "📝 Summary Generator":
        summary_page(openai_client)
    elif page == "📚 Thread Manager":
        thread_manager_page()
    elif page == "⚙️ Settings":
        settings_page()

def research_page(claude_client):
    st.header("🔍 Research Assistant")
    st.markdown("Use Claude to conduct comprehensive research on any topic")
    
    # Research form
    with st.form("research_form"):
        topic = st.text_input("Research Topic", placeholder="Enter your research topic...")
        
        # Optional specific questions
        st.subheader("Specific Questions (Optional)")
        questions = []
        for i in range(3):
            question = st.text_input(f"Question {i+1}", key=f"q_{i}", placeholder="Optional specific question...")
            if question:
                questions.append(question)
        
        submitted = st.form_submit_button("🔍 Start Research", type="primary")
    
    if submitted and topic:
        with st.spinner("Conducting research with Claude..."):
            # Create new thread
            thread = claude_client.create_research_thread(topic)
            
            # Conduct research
            research_result = claude_client.conduct_research(topic, questions if questions else None)
            
            if research_result:
                # Add to thread
                claude_client.add_message_to_thread(thread, "user", f"Research topic: {topic}")
                claude_client.add_message_to_thread(thread, "assistant", research_result)
                
                # Save thread
                save_thread_to_session(thread)
                st.session_state.current_research = research_result
                st.session_state.current_thread = thread
                
                st.success("Research completed!")
                st.rerun()
    
    # Display current research
    if hasattr(st.session_state, 'current_research'):
        st.divider()
        st.subheader("Research Results")
        
        # Metrics
        display_metrics(st.session_state.current_research)
        
        # Research content
        st.markdown(st.session_state.current_research)
        
        # Action buttons
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("📝 Generate Summary", type="secondary"):
                st.session_state.page = "📝 Summary Generator"
                st.session_state.content_to_summarize = st.session_state.current_research
                st.rerun()
        
        with col2:
            create_download_button(
                st.session_state.current_research,
                f"research_{st.session_state.current_thread['topic'][:20]}.txt",
                "💾 Download Research"
            )
        
        with col3:
            if st.button("❓ Follow-up Question"):
                st.session_state.show_followup = True
                st.rerun()
        
        # Follow-up question form
        if hasattr(st.session_state, 'show_followup') and st.session_state.show_followup:
            st.divider()
            with st.form("followup_form"):
                followup_question = st.text_area("Follow-up Question", placeholder="Ask a follow-up question about your research...")
                followup_submitted = st.form_submit_button("Ask Follow-up")
            
            if followup_submitted and followup_question:
                with st.spinner("Getting follow-up research..."):
                    followup_result = claude_client.follow_up_research(
                        st.session_state.current_thread, 
                        followup_question
                    )
                    
                    if followup_result:
                        # Add to thread
                        claude_client.add_message_to_thread(
                            st.session_state.current_thread, 
                            "user", 
                            followup_question
                        )
                        claude_client.add_message_to_thread(
                            st.session_state.current_thread, 
                            "assistant", 
                            followup_result
                        )
                        
                        # Update session
                        save_thread_to_session(st.session_state.current_thread)
                        st.session_state.current_research += f"\n\n**Follow-up Q&A:**\n\n**Q:** {followup_question}\n\n**A:** {followup_result}"
                        st.session_state.show_followup = False
                        st.rerun()

def summary_page(openai_client):
    st.header("📝 Summary Generator")
    st.markdown("Use OpenAI to generate brief summaries of your research")
    
    # Content input
    content_source = st.radio(
        "Content Source",
        ["Current Research", "Paste Content", "Upload File"]
    )
    
    content_to_summarize = ""
    
    if content_source == "Current Research":
        if hasattr(st.session_state, 'current_research'):
            content_to_summarize = st.session_state.current_research
            st.info(f"Using current research: {st.session_state.current_thread['topic']}")
        else:
            st.warning("No current research found. Please conduct research first.")
    
    elif content_source == "Paste Content":
        content_to_summarize = st.text_area(
            "Paste Content to Summarize",
            height=200,
            placeholder="Paste your content here..."
        )
    
    elif content_source == "Upload File":
        uploaded_file = st.file_uploader("Upload Text File", type=['txt', 'md'])
        if uploaded_file:
            content_to_summarize = uploaded_file.read().decode('utf-8')
    
    if content_to_summarize:
        st.divider()
        
        # Summary options
        col1, col2 = st.columns(2)
        
        with col1:
            summary_type = st.selectbox(
                "Summary Type",
                ["brief", "bullet", "executive"]
            )
        
        with col2:
            creative_style = st.selectbox(
                "Creative Style (Optional)",
                ["None", "narrative", "poetic", "dialogue", "analogy"]
            )
        
        # Generate summaries
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📝 Generate Summary", type="primary"):
                with st.spinner("Generating summary with OpenAI..."):
                    summary = openai_client.generate_brief_summary(content_to_summarize, summary_type)
                    if summary:
                        st.session_state.current_summary = summary
                        st.rerun()
        
        with col2:
            if creative_style != "None":
                if st.button("🎨 Generate Creative Summary", type="secondary"):
                    with st.spinner("Generating creative summary..."):
                        creative_summary = openai_client.generate_creative_summary(
                            content_to_summarize, creative_style
                        )
                        if creative_summary:
                            st.session_state.current_creative_summary = creative_summary
                            st.rerun()
        
        # Display summaries
        if hasattr(st.session_state, 'current_summary'):
            st.divider()
            st.subheader("📝 Standard Summary")
            st.markdown(st.session_state.current_summary)
            
            create_download_button(
                st.session_state.current_summary,
                "summary.txt",
                "💾 Download Summary"
            )
        
        if hasattr(st.session_state, 'current_creative_summary'):
            st.divider()
            st.subheader("🎨 Creative Summary")
            st.markdown(st.session_state.current_creative_summary)
            
            create_download_button(
                st.session_state.current_creative_summary,
                "creative_summary.txt",
                "💾 Download Creative Summary"
            )

def thread_manager_page():
    st.header("📚 Thread Manager")
    st.markdown("Manage your research threads and conversations")
    
    threads = get_threads_from_session()
    
    if not threads:
        st.info("No research threads found. Start by conducting some research!")
        return
    
    # Thread list
    for i, thread in enumerate(threads):
        with st.expander(f"📄 {thread['topic']} - {format_timestamp(thread['created_at'])}"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Messages", len(thread['messages']))
            with col2:
                st.metric("Created", format_timestamp(thread['created_at'])[:10])
            with col3:
                if st.button("🗑️ Delete", key=f"delete_{thread['id']}"):
                    st.session_state.research_threads.remove(thread)
                    st.rerun()
            
            # Show messages
            for msg in thread['messages']:
                with st.chat_message(msg['role']):
                    st.markdown(msg['content'][:500] + "..." if len(msg['content']) > 500 else msg['content'])
            
            # Export thread
            thread_export = export_thread_to_text(thread)
            create_download_button(
                thread_export,
                f"thread_{thread['topic'][:20]}.txt",
                "💾 Export Thread"
            )

def settings_page():
    st.header("⚙️ Settings")
    st.markdown("Configure your GenAI Assistant")
    
    st.subheader("API Configuration")
    
    # Display current configuration (without showing actual keys)
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("Claude API")
        if Config.ANTHROPIC_API_KEY:
            st.success("✅ API Key Configured")
        else:
            st.error("❌ API Key Missing")
        st.text(f"Model: {Config.CLAUDE_MODEL}")
        st.text(f"Max Tokens: {Config.MAX_TOKENS_CLAUDE}")
    
    with col2:
        st.info("OpenAI API")
        if Config.OPENAI_API_KEY:
            st.success("✅ API Key Configured")
        else:
            st.error("❌ API Key Missing")
        st.text(f"Model: {Config.OPENAI_MODEL}")
        st.text(f"Max Tokens: {Config.MAX_TOKENS_OPENAI}")
    
    st.divider()
    
    st.subheader("Application Stats")
    threads = get_threads_from_session()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Research Threads", len(threads))
    with col2:
        total_messages = sum(len(thread['messages']) for thread in threads)
        st.metric("Total Messages", total_messages)
    with col3:
        if st.button("🗑️ Clear All Data"):
            st.session_state.research_threads = []
            st.success("All data cleared!")
            st.rerun()
    
    st.divider()
    
    st.subheader("Setup Instructions")
    st.markdown("""
    **To set up your API keys:**
    
    1. Create a `.env` file in the project directory
    2. Add your API keys:
    ```
    ANTHROPIC_API_KEY=your_claude_api_key_here
    OPENAI_API_KEY=your_openai_api_key_here
    ```
    
    **Get API Keys:**
    - **Claude API**: Visit [Anthropic Console](https://console.anthropic.com/)
    - **OpenAI API**: Visit [OpenAI Platform](https://platform.openai.com/)
    """)

if __name__ == "__main__":
    main() 