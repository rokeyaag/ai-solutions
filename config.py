import os
import tempfile
from typing import Dict, Any

class AppConfig:
    # Server configuration
    HOST: str = "0.0.0.0"
    PORT: int = int(os.getenv("PORT", 8000))
    DEBUG: bool = False
    
    # AI Engine Keys
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    
    # Active engine and model
    ACTIVE_PROVIDER: str = os.getenv("ACTIVE_PROVIDER", "demo")
    ACTIVE_MODEL: str = os.getenv("ACTIVE_MODEL", "smart-demo-v1")
    
    # Demo mode allows testing without real API keys
    DEMO_MODE: bool = True
    
    # Directory paths (Vercel Serverless safe using /tmp)
    BASE_DIR: str = os.path.dirname(os.path.abspath(__file__))
    UPLOAD_DIR: str = os.path.join(tempfile.gettempdir(), "ai_saas_uploads")
    STATIC_DIR: str = os.path.join(BASE_DIR, "static")

config = AppConfig()

try:
    os.makedirs(config.UPLOAD_DIR, exist_ok=True)
except Exception:
    pass
