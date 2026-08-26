from fastapi import APIRouter
from services.token_tracker import token_tracker

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])

@router.get("/metrics")
async def get_metrics():
    """Returns real-time token, cost, latency and service usage metrics."""
    return token_tracker.get_dashboard_metrics()

@router.get("/activities")
async def get_activities():
    """Returns recent activity stream."""
    return token_tracker.recent_activities
