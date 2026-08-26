from fastapi import APIRouter, UploadFile, File, Form
from pydantic import BaseModel
from typing import Optional
from services.audio_engine import audio_engine
from services.token_tracker import token_tracker

router = APIRouter(prefix="/api/audio", tags=["Voice & Audio AI"])

class TTSRequest(BaseModel):
    text: str
    voice: str = "alloy"  # alloy, echo, fable, onyx, nova, shimmer
    speed: float = 1.0

@router.post("/transcribe")
async def transcribe_audio(
    file: Optional[UploadFile] = File(None),
    demo_audio: Optional[str] = Form("meeting_recording.mp3")
):
    filename = file.filename if file else demo_audio
    result = audio_engine.transcribe_audio(filename=filename)
    
    token_tracker.record_usage(
        service="Voice & Audio",
        action=f"Transcribed audio file '{filename}'",
        prompt_tokens=420,
        completion_tokens=180,
        latency_ms=510
    )
    
    return result

@router.post("/tts")
async def generate_speech(request: TTSRequest):
    result = audio_engine.generate_speech(
        text=request.text,
        voice=request.voice,
        speed=request.speed
    )
    
    token_tracker.record_usage(
        service="Voice & Audio",
        action=f"Generated TTS Voice ({request.voice}) for {len(request.text)} chars",
        prompt_tokens=len(request.text) // 4,
        completion_tokens=60,
        latency_ms=220
    )
    
    return result
