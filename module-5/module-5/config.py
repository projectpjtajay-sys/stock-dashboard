import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class for API keys and application settings"""
    
    # API Keys
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    
    # Model configurations
    CLAUDE_MODEL = "claude-3-haiku-20240307"
    OPENAI_MODEL = "gpt-4o-mini-2024-07-18"
    
    # Application settings
    MAX_TOKENS_CLAUDE = 4000
    MAX_TOKENS_OPENAI = 1000
    TEMPERATURE = 0.7
    
    @classmethod
    def validate_keys(cls):
        """Validate that required API keys are present"""
        missing_keys = []
        
        if not cls.ANTHROPIC_API_KEY:
            missing_keys.append("ANTHROPIC_API_KEY")
        if not cls.OPENAI_API_KEY:
            missing_keys.append("OPENAI_API_KEY")
            
        return missing_keys 