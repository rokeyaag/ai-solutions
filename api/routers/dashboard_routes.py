from fastapi import APIRouter
try:
    from services.token_tracker import token_tracker
except Exception:
    from api.services.token_tracker import token_tracker

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])

@router.get("/metrics")
async def get_metrics():
    return token_tracker.get_dashboard_metrics()

@router.get("/activities")
async def get_activities():
    return token_tracker.recent_activities
