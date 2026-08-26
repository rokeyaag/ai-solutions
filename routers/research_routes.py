from fastapi import APIRouter
from pydantic import BaseModel
from services.research_engine import research_engine
from services.token_tracker import token_tracker

router = APIRouter(prefix="/api/research", tags=["Autonomous Research Agent"])

class ResearchRequest(BaseModel):
    topic: str
    focus_area: str = "Market & Technology Landscape"

@router.post("/execute")
async def execute_research(request: ResearchRequest):
    result = research_engine.conduct_deep_research(
        topic=request.topic,
        focus_area=request.focus_area
    )
    
    token_tracker.record_usage(
        service="Research Agent",
        action=f"Deep Research on '{request.topic[:30]}...'",
        prompt_tokens=850,
        completion_tokens=1450,
        latency_ms=920
    )
    
    return result
