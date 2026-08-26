from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict
from services.ai_engine import ai_engine
from services.token_tracker import token_tracker

router = APIRouter(prefix="/api/chat", tags=["Multi-Persona Chatbot"])

PERSONA_SYSTEM_PROMPTS = {
    "software_architect": (
        "You are an elite Chief Software Architect. You design highly scalable, fault-tolerant, "
        "microservices and event-driven distributed systems. You provide technical diagrams, trade-offs, "
        "and architectural patterns."
    ),
    "business_consultant": (
        "You are a Senior SaaS Business Consultant and Venture Strategist. You specialize in pricing "
        "strategies, GTM execution, unit economics (CAC, LTV, NRR), and customer retention."
    ),
    "seo_copywriter": (
        "You are a World-Class SEO Copywriter and Conversion Rate Optimization (CRO) expert. You craft "
        "catchy headlines, compelling value propositions, and search-engine optimized copy."
    ),
    "legal_advisor": (
        "You are a Corporate Legal and AI Compliance Specialist. You provide risk assessments, GDPR/CCPA "
        "frameworks, Terms of Service reviews, and intellectual property advisories."
    ),
    "ai_engineer": (
        "You are a Senior Full-Stack AI Engineer specialized in PyTorch, FastAPI, LangChain, RAG architectures, "
        "and production LLM optimization."
    )
}

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    persona: str = "software_architect"
    message: str
    history: Optional[List[ChatMessage]] = []
    temperature: float = 0.7

@router.get("/personas")
async def get_personas():
    return [
        {"id": "software_architect", "name": "Software Architect", "badge": "System Design", "icon": "fa-sitemap"},
        {"id": "business_consultant", "name": "Business Consultant", "badge": "Strategy & GTM", "icon": "fa-chart-line"},
        {"id": "seo_copywriter", "name": "SEO & Copywriter", "badge": "Content & Growth", "icon": "fa-pen-nib"},
        {"id": "legal_advisor", "name": "Legal & Compliance", "badge": "Risk & GDPR", "icon": "fa-scale-balanced"},
        {"id": "ai_engineer", "name": "Senior AI Engineer", "badge": "Code & Models", "icon": "fa-brain"}
    ]

@router.post("/send")
async def send_chat_message(request: ChatRequest):
    system_prompt = PERSONA_SYSTEM_PROMPTS.get(request.persona, PERSONA_SYSTEM_PROMPTS["software_architect"])
    history_dicts = [{"role": msg.role, "content": msg.content} for msg in request.history] if request.history else []
    
    result = await ai_engine.generate_response(
        system_prompt=system_prompt,
        user_message=request.message,
        history=history_dicts,
        temperature=request.temperature
    )
    
    # Record telemetry
    token_tracker.record_usage(
        service="Multi-Persona Chat",
        action=f"Chatted with {request.persona.replace('_', ' ').title()}",
        prompt_tokens=result["prompt_tokens"],
        completion_tokens=result["completion_tokens"],
        latency_ms=result["latency_ms"]
    )
    
    return {
        "persona": request.persona,
        "reply": result["response"],
        "model": result["model"],
        "provider": result["provider"],
        "tokens": result["prompt_tokens"] + result["completion_tokens"],
        "latency_ms": result["latency_ms"]
    }
