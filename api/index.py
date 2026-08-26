import os
import sys

# Add root directory to sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

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

# Include All 10 Routers
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
        os.path.join(BASE_DIR, relative_path),
        os.path.join(os.path.dirname(__file__), relative_path),
        os.path.join(os.getcwd(), relative_path),
        f"/var/task/{relative_path}"
    ]
    for p in search_paths:
        if os.path.exists(p):
            try:
                with open(p, "r", encoding="utf-8") as f:
                    return f.read()
            except Exception:
                pass
    return ""

# Static file endpoints for Vercel Serverless
@app.get("/static/css/custom.css")
async def serve_custom_css():
    content = find_file("static/css/custom.css")
    return Response(content=content, media_type="text/css")

@app.get("/static/js/app.js")
async def serve_app_js():
    content = find_file("static/js/app.js")
    return Response(content=content, media_type="application/javascript")

@app.get("/static/widget.js")
async def serve_widget_js():
    content = find_file("static/widget.js")
    return Response(content=content, media_type="application/javascript")

# Mount static folder if available
static_dir = os.path.join(BASE_DIR, "static")
if os.path.exists(static_dir):
    try:
        app.mount("/static", StaticFiles(directory=static_dir), name="static")
    except Exception:
        pass

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
