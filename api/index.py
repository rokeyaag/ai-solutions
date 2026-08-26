import os
import sys

# Ensure both api folder and parent folder are in sys.path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(CURRENT_DIR)

for p in [CURRENT_DIR, PARENT_DIR]:
    if p not in sys.path:
        sys.path.insert(0, p)

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, Response, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

# Resilient dual-fallback imports
try:
    from config import config
    from routers.dashboard_routes import router as dashboard_router
    from routers.chat_routes import router as chat_router
    from routers.rag_routes import router as rag_router
    from routers.copy_routes import router as copy_router
    from routers.vision_routes import router as vision_router
    from routers.audio_routes import router as audio_router
    from routers.code_routes import router as code_router
    from routers.research_routes import router as research_router
    from routers.widget_routes import router as widget_router
    from routers.settings_routes import router as settings_router
except Exception:
    from api.config import config
    from api.routers.dashboard_routes import router as dashboard_router
    from api.routers.chat_routes import router as chat_router
    from api.routers.rag_routes import router as rag_router
    from api.routers.copy_routes import router as copy_router
    from api.routers.vision_routes import router as vision_router
    from api.routers.audio_routes import router as audio_router
    from api.routers.code_routes import router as code_router
    from api.routers.research_routes import router as research_router
    from api.routers.widget_routes import router as widget_router
    from api.routers.settings_routes import router as settings_router

# Initialize FastAPI App
app = FastAPI(
    title="NexusAI - Comprehensive AI SaaS Dashboard Platform",
    description="Enterprise-ready multi-feature AI SaaS platform with 10 integrated modules.",
    version="2.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include All 10 Module Routers
app.include_router(dashboard_router)
app.include_router(chat_router)
app.include_router(rag_router)
app.include_router(copy_router)
app.include_router(vision_router)
app.include_router(audio_router)
app.include_router(code_router)
app.include_router(research_router)
app.include_router(widget_router)
app.include_router(settings_router)

def find_file(relative_path: str) -> str:
    search_paths = [
        os.path.join(CURRENT_DIR, relative_path),
        os.path.join(PARENT_DIR, relative_path),
        os.path.join(os.getcwd(), relative_path),
        f"/var/task/{relative_path}",
        f"/var/task/api/{relative_path}"
    ]
    for p in search_paths:
        if os.path.exists(p):
            try:
                with open(p, "r", encoding="utf-8") as f:
                    return f.read()
            except Exception:
                pass
    return ""

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "service": "NexusAI SaaS Engine", "version": "2.0.0"}

@app.get("/static/{file_path:path}")
async def serve_static_file(file_path: str):
    """Serves static files directly in serverless environment."""
    content = find_file(f"static/{file_path}")
    if file_path.endswith(".css"):
        media = "text/css"
    elif file_path.endswith(".js"):
        media = "application/javascript"
    elif file_path.endswith(".html"):
        media = "text/html"
    elif file_path.endswith(".json"):
        media = "application/json"
    else:
        media = "text/plain"
    return Response(content=content, media_type=media)

@app.get("/", response_class=HTMLResponse)
async def serve_index():
    """Serves the main AI SaaS Dashboard UI."""
    content = find_file("static/index.html")
    if content:
        return HTMLResponse(content=content)
    return HTMLResponse("<h1>NexusAI SaaS Dashboard is ready.</h1>")

@app.get("/demo-widget", response_class=HTMLResponse)
async def serve_demo_widget():
    """Demonstration page for the embeddable chatbot widget."""
    content = find_file("static/widget_demo.html")
    if content:
        return HTMLResponse(content=content)
    return HTMLResponse("<h1>Widget Demo Page</h1>")
