import os
import sys

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

# Locate and Mount Static Assets
static_candidates = [
    os.path.join(BASE_DIR, "static"),
    os.path.join(os.path.dirname(BASE_DIR), "static"),
    "/var/task/static"
]

static_path = next((p for p in static_candidates if os.path.exists(p)), None)
if static_path:
    try:
        app.mount("/static", StaticFiles(directory=static_path), name="static")
    except Exception:
        pass

def get_static_file_content(filename: str) -> str:
    for candidate in static_candidates:
        file_path = os.path.join(candidate, filename)
        if os.path.exists(file_path):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    return f.read()
            except Exception:
                pass
    return ""

@app.get("/", response_class=HTMLResponse)
async def serve_index():
    """Serves the main AI SaaS Dashboard single-page application."""
    content = get_static_file_content("index.html")
    if content:
        return HTMLResponse(content=content)
    return HTMLResponse("<h1>NexusAI SaaS Dashboard is ready.</h1>")

@app.get("/demo-widget", response_class=HTMLResponse)
async def serve_demo_widget():
    """Demonstration webpage showing the embeddable chatbot widget in action."""
    content = get_static_file_content("widget_demo.html")
    if content:
        return HTMLResponse(content=content)
    return HTMLResponse("<h1>Widget Demo Page</h1>")

if __name__ == "__main__":
    import uvicorn
    print(f"🚀 Starting AI SaaS Dashboard at http://{config.HOST}:{config.PORT}")
    uvicorn.run("main:app", host=config.HOST, port=config.PORT, reload=config.DEBUG)
