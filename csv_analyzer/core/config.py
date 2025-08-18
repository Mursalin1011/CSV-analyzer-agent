import os
from dotenv import load_dotenv
from typing import Optional

# Load environment variables from .env file
load_dotenv()

class Config:
    """Application configuration settings"""
    
    # LLM Configuration
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "gemini")  # "gemini" or "ollama"
    
    # Gemini Configuration
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    
    # Ollama Configuration
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen3:0.6b")
    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    
    # LangSmith Configuration
    LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2", "false").lower() == "true"
    LANGCHAIN_ENDPOINT = os.getenv("LANGCHAIN_ENDPOINT", "https://api.smith.langchain.com")
    
    # Database Configuration
    DATABASE_FILE = os.getenv("DATABASE_FILE", "insights_cache.db")
    
    # Application Configuration
    APP_TITLE = "📊 CSV Data Insights Generator"
    APP_DESCRIPTION = "Upload your data file to get AI-powered insights"
    
    @classmethod
    def validate(cls) -> tuple[bool, Optional[str]]:
        """Validate configuration settings"""
        if cls.LLM_PROVIDER not in ["gemini", "ollama"]:
            return False, f"Invalid LLM_PROVIDER: {cls.LLM_PROVIDER}. Must be 'gemini' or 'ollama'"
            
        if cls.LLM_PROVIDER == "gemini" and not cls.GOOGLE_API_KEY:
            return False, "GOOGLE_API_KEY is required when using Gemini provider"
            
        return True, None