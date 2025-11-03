import anthropic
from config import Config
import streamlit as st
from typing import List, Dict, Any
import uuid
from datetime import datetime

class ClaudeClient:
    """Client for interacting with Claude API for research purposes"""
    
    def __init__(self):
        if not Config.ANTHROPIC_API_KEY:
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables")
        
        self.client = anthropic.Anthropic(
            api_key=Config.ANTHROPIC_API_KEY
        )
        self.model = Config.CLAUDE_MODEL
        
    def create_research_thread(self, topic: str) -> Dict[str, Any]:
        """Create a new research thread for a given topic"""
        thread_id = str(uuid.uuid4())
        thread = {
            "id": thread_id,
            "topic": topic,
            "messages": [],
            "created_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat()
        }
        return thread
    
    def conduct_research(self, topic: str, specific_questions: List[str] = None) -> str:
        """Conduct comprehensive research on a given topic"""
        
        research_prompt = f"""
        You are a research assistant tasked with conducting comprehensive research on the topic: "{topic}"
        
        Please provide detailed, well-structured research that includes:
        1. An overview of the topic
        2. Key concepts and definitions
        3. Current trends and developments
        4. Important facts and statistics
        5. Notable experts or organizations in this field
        6. Recent developments or news
        7. Potential applications or implications
        
        """
        
        if specific_questions:
            research_prompt += f"\nAlso address these specific questions:\n"
            for i, question in enumerate(specific_questions, 1):
                research_prompt += f"{i}. {question}\n"
        
        research_prompt += "\nProvide comprehensive, accurate, and well-organized information suitable for research purposes."
        
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=Config.MAX_TOKENS_CLAUDE,
                temperature=Config.TEMPERATURE,
                messages=[{"role": "user", "content": research_prompt}]
            )
            
            return response.content[0].text
            
        except Exception as e:
            st.error(f"Error conducting research: {str(e)}")
            return None
    
    def follow_up_research(self, thread: Dict[str, Any], follow_up_question: str) -> str:
        """Continue research with follow-up questions"""
        
        # Build context from previous messages
        context = f"Previous research on '{thread['topic']}':\n"
        for msg in thread['messages'][-3:]:  # Last 3 messages for context
            context += f"\n{msg['role']}: {msg['content'][:500]}..."
        
        follow_up_prompt = f"""
        {context}
        
        Based on the previous research, please provide detailed information addressing this follow-up question:
        "{follow_up_question}"
        
        Provide specific, detailed information that builds upon the previous research.
        """
        
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=Config.MAX_TOKENS_CLAUDE,
                temperature=Config.TEMPERATURE,
                messages=[{"role": "user", "content": follow_up_prompt}]
            )
            
            return response.content[0].text
            
        except Exception as e:
            st.error(f"Error in follow-up research: {str(e)}")
            return None
    
    def add_message_to_thread(self, thread: Dict[str, Any], role: str, content: str):
        """Add a message to the research thread"""
        message = {
            "id": str(uuid.uuid4()),
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        }
        thread['messages'].append(message)
        thread['last_updated'] = datetime.now().isoformat() 