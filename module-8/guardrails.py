from typing import Dict, Any
import re

class SafetyGuardrails:
    def __init__(self):
        # Define harmful keywords and patterns
        self.harmful_keywords = [
            # Violence and harm
            "hack", "virus", "bomb", "kill", "murder", "suicide", "self-harm", "hurt",
            "violence", "attack", "assault", "weapon", "gun", "knife", "explosive",
            
            # Illegal activities
            "illegal drugs", "cocaine", "heroin", "meth", "steal", "robbery", "fraud",
            "money laundering", "tax evasion", "piracy", "copyright infringement",
            
            # Inappropriate content
            "sexual content", "pornography", "adult content", "nsfw",
            
            # Personal information requests
            "password", "social security", "credit card", "bank account", "private key"
        ]
        
        # Sensitive patterns
        self.sensitive_patterns = [
            r"how to (hack|break into|steal)",
            r"make (bomb|explosive|weapon)",
            r"illegal ways to",
            r"bypass security",
            r"crack password",
        ]
    
    def check_input_safety(self, user_input: str) -> Dict[str, Any]:
        """Check if user input is safe"""
        try:
            user_lower = user_input.lower()
            
            # Check for harmful keywords
            for keyword in self.harmful_keywords:
                if keyword.lower() in user_lower:
                    return {
                        "safe": False, 
                        "message": "I cannot help with requests that may involve harmful or illegal activities. Please ask about engineering, medical, or legal topics in a constructive way."
                    }
            
            # Check for sensitive patterns using regex
            for pattern in self.sensitive_patterns:
                if re.search(pattern, user_lower, re.IGNORECASE):
                    return {
                        "safe": False,
                        "message": "I cannot provide guidance on potentially harmful activities. Please rephrase your question in a constructive manner."
                    }
            
            # Check for excessive profanity or inappropriate language
            profanity_words = ["fuck", "shit", "damn", "bitch", "asshole"]
            profanity_count = sum(1 for word in profanity_words if word in user_lower)
            
            if profanity_count > 2:  # Allow some casual language but not excessive
                return {
                    "safe": False,
                    "message": "Please keep the conversation professional and respectful."
                }
            
            return {"safe": True, "message": user_input}
            
        except Exception as e:
            print(f"Error in safety check: {e}")
            return {"safe": True, "message": user_input}
    
    def add_disclaimers(self, response: str, agent_type: str) -> str:
        """Add appropriate disclaimers based on agent type"""
        disclaimers = {
            "doctor": "\n\n⚠️ Disclaimer: This information is for educational purposes only. Please consult with a qualified healthcare professional for medical advice, diagnosis, or treatment.",
            "lawyer": "\n\n⚠️ Disclaimer: This is general legal information only and should not be considered legal advice. Please consult with a qualified attorney for specific legal matters.",
            "engineer": "\n\n💡 Note: This is technical guidance. Always test thoroughly and consider your specific requirements and constraints."
        }
        
        disclaimer = disclaimers.get(agent_type, "")
        return response + disclaimer
    
    def filter_response(self, response: str, agent_type: str) -> str:
        """Filter and enhance response with safety measures"""
        # Add disclaimers
        filtered_response = self.add_disclaimers(response, agent_type)
        
        # Basic content filtering
        if not filtered_response:
            return "I apologize, but I cannot provide a response to that query."
            
        return filtered_response 