from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
from typing import Optional
from services.ocr_engine import ocr_engine
from services.token_tracker import token_tracker

router = APIRouter(prefix="/api/vision", tags=["AI Vision & OCR Studio"])

class ImageGenRequest(BaseModel):
    prompt: str
    style: str = "Cyberpunk / Futuristic"
    aspect_ratio: str = "1:1"

@router.post("/generate-image")
async def generate_image(request: ImageGenRequest):
    result = ocr_engine.generate_image(
        prompt=request.prompt,
        style=request.style,
        aspect_ratio=request.aspect_ratio
    )
    
    token_tracker.record_usage(
        service="Vision & OCR",
        action=f"Generated Image: '{request.prompt[:30]}...'",
        prompt_tokens=80,
        completion_tokens=400,
        latency_ms=490
    )
    
    return result

@router.post("/ocr-scan")
async def scan_document_ocr(
    file: Optional[UploadFile] = File(None),
    sample_type: Optional[str] = Form("invoice")
):
    filename = file.filename if file else f"Sample_{sample_type.title()}_Scan.png"
    size = len(await file.read()) if file else 45000
    
    result = ocr_engine.process_document_ocr(filename=filename, file_bytes_len=size)
    
    token_tracker.record_usage(
        service="Vision & OCR",
        action=f"OCR Extracted fields from '{filename}'",
        prompt_tokens=320,
        completion_tokens=280,
        latency_ms=380
    )
    
    return result
