from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, List
from services.ai_engine import ai_engine
from services.token_tracker import token_tracker

router = APIRouter(prefix="/api/widget", tags=["Embeddable Website Widget"])

class WidgetMessageRequest(BaseModel):
    bot_id: str = "widget_default"
    message: str
    visitor_id: Optional[str] = "vis_anon"
    theme_color: Optional[str] = "#3b82f6"

@router.get("/config")
async def get_widget_config():
    return {
        "bot_id": "widget_default",
        "bot_name": "SaaS AI Assistant",
        "greeting": "Hi there! 👋 How can I help you explore our product today?",
        "primary_color": "#3b82f6",
        "placeholder": "Type your question here...",
        "embed_code": '<script src="http://localhost:8000/static/widget.js" data-bot-id="widget_default"></script>'
    }

@router.post("/message")
async def handle_widget_message(request: WidgetMessageRequest):
    system_prompt = (
        "You are a friendly, highly helpful customer support and sales AI assistant embedded "
        "on a SaaS website. Keep answers crisp, warm, helpful, and encourage users to sign up for a trial."
    )
    result = await ai_engine.generate_response(
        system_prompt=system_prompt,
        user_message=request.message
    )
    
    token_tracker.record_usage(
        service="Embeddable Widget",
        action=f"Widget inquiry: '{request.message[:25]}...'",
        prompt_tokens=result["prompt_tokens"],
        completion_tokens=result["completion_tokens"],
        latency_ms=result["latency_ms"]
    )
    
    return {
        "reply": result["response"],
        "bot_name": "SaaS AI Assistant",
        "latency_ms": result["latency_ms"]
    }
