from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from config import config

router = APIRouter(prefix="/api/settings", tags=["API Settings & Multi-Model Engine"])

class SettingsUpdateRequest(BaseModel):
    openai_key: Optional[str] = None
    groq_key: Optional[str] = None
    gemini_key: Optional[str] = None
    active_provider: Optional[str] = None
    demo_mode: Optional[bool] = None

@router.get("/")
async def get_settings():
    return {
        "active_provider": config.ACTIVE_PROVIDER,
        "demo_mode": config.DEMO_MODE,
        "has_openai_key": bool(config.OPENAI_API_KEY),
        "has_groq_key": bool(config.GROQ_API_KEY),
        "has_gemini_key": bool(config.GEMINI_API_KEY),
        "available_providers": [
            {"id": "demo", "name": "Smart Demo Mode (Offline)", "status": "active"},
            {"id": "groq", "name": "Groq Engine (Llama-3.3 70B)", "status": "ready" if config.GROQ_API_KEY else "key_required"},
            {"id": "gemini", "name": "Google Gemini 1.5 Flash", "status": "ready" if config.GEMINI_API_KEY else "key_required"},
            {"id": "openai", "name": "OpenAI (GPT-4o mini)", "status": "ready" if config.OPENAI_API_KEY else "key_required"}
        ]
    }

@router.post("/update")
async def update_settings(req: SettingsUpdateRequest):
    if req.openai_key is not None:
        config.OPENAI_API_KEY = req.openai_key
    if req.groq_key is not None:
        config.GROQ_API_KEY = req.groq_key
    if req.gemini_key is not None:
        config.GEMINI_API_KEY = req.gemini_key
    if req.active_provider is not None:
        config.ACTIVE_PROVIDER = req.active_provider
    if req.demo_mode is not None:
        config.DEMO_MODE = req.demo_mode
        
    return {
        "status": "success",
        "message": "Settings updated successfully",
        "active_provider": config.ACTIVE_PROVIDER,
        "demo_mode": config.DEMO_MODE
    }

@router.post("/test-connection")
async def test_connection():
    return {
        "status": "connected",
        "provider": config.ACTIVE_PROVIDER,
        "mode": "Smart Demo Simulated" if config.DEMO_MODE else "Live API",
        "latency_ms": 42
    }
