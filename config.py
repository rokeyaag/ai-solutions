import os
from pydantic import BaseModel
from typing import Dict, Any

class AppConfig:
    # Server configuration
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    DEBUG: bool = True
    
    # AI Engine Keys
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    
    # Active engine and model
    ACTIVE_PROVIDER: str = "demo"  # "demo", "groq", "gemini", "openai"
    ACTIVE_MODEL: str = "smart-demo-v1"
    
    # Demo mode allows testing without real API keys
    DEMO_MODE: bool = True
    
    # Directories
    UPLOAD_DIR: str = os.path.join(os.path.dirname(__file__), "uploads")
    STATIC_DIR: str = os.path.join(os.path.dirname(__file__), "static")

config = AppConfig()
os.makedirs(config.UPLOAD_DIR, exist_ok=True)
