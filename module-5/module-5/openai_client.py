import openai
from config import Config
import streamlit as st
from typing import List, Dict

class OpenAIClient:
    """Client for interacting with OpenAI API for summary generation"""
    
    def __init__(self):
        if not Config.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        self.client = openai.OpenAI(api_key=Config.OPENAI_API_KEY)
        self.model = Config.OPENAI_MODEL
    
    def generate_brief_summary(self, research_content: str, summary_type: str = "brief") -> str:
        """Generate a brief summary of research content"""
        
        if summary_type == "brief":
            prompt = f"""
            Please create a brief, concise summary of the following research content. 
            The summary should:
            1. Capture the key points and main ideas
            2. Be easy to understand
            3. Be approximately 2-3 paragraphs long
            4. Highlight the most important information
            
            Research Content:
            {research_content}
            
            Brief Summary:
            """
        elif summary_type == "bullet":
            prompt = f"""
            Please create a bullet-point summary of the following research content.
            The summary should:
            1. List key points as bullet points
            2. Be concise and easy to scan
            3. Include 5-10 main points
            4. Focus on the most important information
            
            Research Content:
            {research_content}
            
            Bullet Point Summary:
            """
        elif summary_type == "executive":
            prompt = f"""
            Please create an executive summary of the following research content.
            The summary should:
            1. Be professional and formal
            2. Highlight key findings and implications
            3. Be suitable for decision-makers
            4. Include recommendations if applicable
            
            Research Content:
            {research_content}
            
            Executive Summary:
            """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=Config.MAX_TOKENS_OPENAI,
                temperature=Config.TEMPERATURE
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            st.error(f"Error generating summary: {str(e)}")
            return None
    
    def generate_creative_summary(self, research_content: str, style: str = "narrative") -> str:
        """Generate a creative summary in different styles"""
        
        style_prompts = {
            "narrative": "Create a narrative story-like summary that tells the information as an engaging story",
            "poetic": "Create a poetic summary that captures the essence in a creative, artistic way",
            "dialogue": "Present the information as a dialogue between two experts discussing the topic",
            "analogy": "Explain the research using analogies and metaphors to make it more relatable"
        }
        
        prompt = f"""
        {style_prompts.get(style, style_prompts["narrative"])}
        
        Research Content:
        {research_content}
        
        Creative Summary:
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=Config.MAX_TOKENS_OPENAI,
                temperature=0.8  # Higher temperature for creativity
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            st.error(f"Error generating creative summary: {str(e)}")
            return None
    
    def compare_summaries(self, content1: str, content2: str) -> str:
        """Compare two pieces of content and provide a comparative summary"""
        
        prompt = f"""
        Please compare and contrast the following two pieces of content.
        Highlight similarities, differences, and provide insights about both.
        
        Content 1:
        {content1}
        
        Content 2:
        {content2}
        
        Comparative Analysis:
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=Config.MAX_TOKENS_OPENAI,
                temperature=Config.TEMPERATURE
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            st.error(f"Error generating comparison: {str(e)}")
            return None 