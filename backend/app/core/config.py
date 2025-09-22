from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # Database
    database_url: str = "postgresql://genai_user:genai_password@localhost:5432/genai_stack"
    
    # ChromaDB
    chroma_host: str = "localhost"
    chroma_port: int = 8001
    
    # API Keys - These will be loaded from environment variables
    openai_api_key: Optional[str] = None
    gemini_api_key: Optional[str] = None
    serpapi_key: Optional[str] = None
    
    # Security
    secret_key: str = "your-secret-key-here-change-this-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Application
    app_name: str = "GenAI Stack"
    debug: bool = False
    
    class Config:
        env_file = ".env"
        case_sensitive = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Validate that required API keys are provided
        if not self.openai_api_key and not self.gemini_api_key:
            print("WARNING: No LLM API keys provided. Please set OPENAI_API_KEY or GEMINI_API_KEY in your .env file")

settings = Settings()



