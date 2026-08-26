import os
import sys

# Ensure root directory is in sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
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

# Initialize FastAPI Application
app = FastAPI(
    title="NexusAI - Comprehensive AI SaaS Dashboard Platform",
    description="Enterprise-ready multi-feature AI SaaS platform with 10 integrated modules.",
    version="2.0.0"
)

# Enable CORS for external embeddable widget & cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Routers for all 10 modules
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

# Mount Static Assets
static_path = os.path.join(BASE_DIR, "static")
if os.path.exists(static_path):
    app.mount("/static", StaticFiles(directory=static_path), name="static")

@app.get("/", response_class=HTMLResponse)
async def serve_index():
    """Serves the main AI SaaS Dashboard single-page application."""
    index_file = os.path.join(BASE_DIR, "static", "index.html")
    if os.path.exists(index_file):
        with open(index_file, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse("<h1>NexusAI SaaS Dashboard is ready.</h1>")

@app.get("/demo-widget", response_class=HTMLResponse)
async def serve_demo_widget():
    """Demonstration webpage showing the embeddable chatbot widget in action."""
    demo_file = os.path.join(BASE_DIR, "static", "widget_demo.html")
    if os.path.exists(demo_file):
        with open(demo_file, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse("<h1>Widget Demo Page</h1>")

if __name__ == "__main__":
    import uvicorn
    print(f"🚀 Starting AI SaaS Dashboard at http://{config.HOST}:{config.PORT}")
    uvicorn.run("main:app", host=config.HOST, port=config.PORT, reload=config.DEBUG)
