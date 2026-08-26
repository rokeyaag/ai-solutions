# 🚀 NexusAI - Comprehensive AI SaaS Dashboard Platform

An enterprise-ready, multi-tenant AI SaaS Dashboard platform built with **FastAPI**, **Tailwind CSS**, **Chart.js**, and modern AI pipelines.

---

## 🌟 10 Core Modules

1. 📊 **AI Overview & Token Dashboard**: Real-time token telemetry (prompt vs completion), estimated cost calculations ($ USD), latency tracking, and live activity pipeline streams.
2. 💬 **Multi-Persona AI Chatbot**: Switchable roles (Software Architect, Business Consultant, SEO Copywriter, Legal & Compliance Advisor, Senior AI Engineer) with custom system prompts and temperature adjustments.
3. 📄 **Document RAG Studio**: Document uploading, text indexing, chunking, and semantic vector similarity retrieval with verified citations and page references.
4. ✍️ **Copywriting & SEO Suite**: Instant generators for SEO blog articles, B2B cold emails, viral LinkedIn posts, and multi-variant digital ad copy.
5. 🎨 **AI Vision & OCR Studio**: Prompt-based image generator and commercial invoice & document OCR scanner with structured entity extraction.
6. 🎙️ **Voice & Audio AI**: Whisper speech-to-text audio transcription with timestamps, plus Text-to-Speech (TTS) natural voiceover playback.
7. 💻 **Code Copilot & CSV Data Visualizer**: Polyglot code language converter, natural language to SQL query builder, and automatic CSV dataset visualizer using dynamic Chart.js.
8. 🤖 **Autonomous Research Agent**: 4-step autonomous research pipeline (Decomposition $\to$ Source Crawling $\to$ Synthesis $\to$ Executive Report).
9. 🧩 **Embeddable Website Widget**: Standalone 1-line `<script>` tag allowing clients to embed your AI chatbot onto any external website with customizable theme.
10. ⚙️ **API Settings & Multi-Model Engine**: Support for Groq (Llama-3.3 70B), Google Gemini 1.5 Flash, OpenAI GPT-4o mini, plus an intelligent **Smart Demo Mode** for offline/instant evaluation.

---

## 🛠️ Quick Start & Running the Project

### 1. Install Dependencies
```bash
cd C:\Users\HP\.gemini\antigravity\scratch\ai-saas-dashboard
pip install -r requirements.txt
```

### 2. Launch the Application
```bash
python main.py
```
*Or using uvicorn:*
```bash
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

### 3. Open in Browser
* **Main Dashboard:** [http://127.0.0.1:8000](http://127.0.0.1:8000)
* **Interactive API Docs (Swagger):** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* **Embeddable Widget Live Demo:** [http://127.0.0.1:8000/demo-widget](http://127.0.0.1:8000/demo-widget)

---

## 📁 Project Structure

```
ai-saas-dashboard/
├── main.py                      # FastAPI App entrypoint
├── config.py                    # Environment settings & API keys
├── requirements.txt             # Dependencies
├── .env.example                 # Environment variables
├── README.md                    # Documentation
├── services/                    # Core AI business logic services
│   ├── ai_engine.py             # Multi-model connector
│   ├── token_tracker.py         # Usage analytics & cost tracker
│   ├── rag_engine.py            # RAG parser, chunker & citations
│   ├── ocr_engine.py            # OCR & Image generator
│   ├── code_engine.py           # Code converter & SQL builder
│   ├── research_engine.py       # Autonomous research pipeline
│   └── audio_engine.py          # Whisper transcription & TTS
├── routers/                     # REST API endpoints for each module
│   ├── dashboard_routes.py
│   ├── chat_routes.py
│   ├── rag_routes.py
│   ├── copy_routes.py
│   ├── vision_routes.py
│   ├── audio_routes.py
│   ├── code_routes.py
│   ├── research_routes.py
│   ├── widget_routes.py
│   └── settings_routes.py
└── static/                      # Modern Dark SaaS Frontend
    ├── index.html               # Main dashboard UI
    ├── widget_demo.html         # External client site demo
    ├── widget.js                # 1-line embeddable script
    ├── css/custom.css           # Styling & animations
    └── js/app.js                # Frontend application logic
```
