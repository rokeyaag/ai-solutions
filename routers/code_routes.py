from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
from typing import Optional
from services.code_engine import code_engine
from services.token_tracker import token_tracker

router = APIRouter(prefix="/api/code", tags=["Code Copilot & CSV Visualizer"])

class CodeConvertRequest(BaseModel):
    source_code: str
    from_lang: str = "JavaScript"
    to_lang: str = "Python"

class SQLGenRequest(BaseModel):
    prompt: str
    dialect: str = "PostgreSQL"

@router.post("/convert")
async def convert_code_snippet(request: CodeConvertRequest):
    result = code_engine.convert_code(
        source_code=request.source_code,
        from_lang=request.from_lang,
        to_lang=request.to_lang
    )
    
    token_tracker.record_usage(
        service="Code Copilot",
        action=f"Converted code from {request.from_lang} to {request.to_lang}",
        prompt_tokens=len(request.source_code) // 4 + 20,
        completion_tokens=len(result["converted_code"]) // 4 + 20,
        latency_ms=270
    )
    
    return result

@router.post("/sql-generator")
async def generate_sql_query(request: SQLGenRequest):
    result = code_engine.generate_sql(
        natural_query=request.prompt,
        dialect=request.dialect
    )
    
    token_tracker.record_usage(
        service="Code Copilot",
        action=f"Generated {request.dialect} SQL for query",
        prompt_tokens=60,
        completion_tokens=140,
        latency_ms=190
    )
    
    return result

@router.post("/csv-visualize")
async def visualize_csv_data(
    file: Optional[UploadFile] = File(None),
    csv_text: Optional[str] = Form(None)
):
    if file:
        file_bytes = await file.read()
        text = file_bytes.decode("utf-8", errors="ignore")
    elif csv_text:
        text = csv_text
    else:
        # Default sample dataset
        text = (
            "Month,ActiveUsers,RevenueUSD,ServerCosts\n"
            "Jan,1200,14500,2100\n"
            "Feb,1850,19200,2300\n"
            "Mar,2400,26800,2800\n"
            "Apr,3100,34500,3200\n"
            "May,4200,46000,3900\n"
            "Jun,5600,62500,4600\n"
            "Jul,7100,78000,5200\n"
            "Aug,8900,98400,6100\n"
        )
        
    analysis = code_engine.analyze_csv_data(text)
    
    token_tracker.record_usage(
        service="Code Copilot",
        action=f"Visualized CSV Dataset ({analysis.get('total_rows', 0)} rows)",
        prompt_tokens=150,
        completion_tokens=50,
        latency_ms=150
    )
    
    return analysis
