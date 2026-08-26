from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
from typing import Optional
from services.rag_engine import rag_engine
from services.token_tracker import token_tracker

router = APIRouter(prefix="/api/rag", tags=["Document RAG Studio"])

class RAGQueryRequest(BaseModel):
    query: str
    top_k: int = 3

@router.get("/documents")
async def get_documents():
    return {"documents": rag_engine.list_documents()}

@router.post("/upload")
async def upload_document(
    file: Optional[UploadFile] = File(None),
    filename: Optional[str] = Form(None),
    content_text: Optional[str] = Form(None)
):
    if file:
        file_bytes = await file.read()
        text = file_bytes.decode("utf-8", errors="ignore")
        name = file.filename
        size = len(file_bytes)
    elif content_text and filename:
        text = content_text
        name = filename
        size = len(content_text.encode("utf-8"))
    else:
        raise HTTPException(status_code=400, detail="Must provide either file or content_text + filename")
        
    doc_info = rag_engine.add_document(filename=name, content=text, file_size=size)
    
    token_tracker.record_usage(
        service="Document RAG",
        action=f"Indexed document '{name}' ({doc_info['chunks_count']} chunks)",
        prompt_tokens=doc_info['chunks_count'] * 120,
        completion_tokens=20,
        latency_ms=210
    )
    
    return {"status": "success", "document": doc_info}

@router.delete("/documents/{doc_id}")
async def delete_document(doc_id: str):
    success = rag_engine.delete_document(doc_id)
    if not success:
        raise HTTPException(status_code=404, detail="Document not found")
    return {"status": "deleted", "doc_id": doc_id}

@router.post("/query")
async def query_rag(request: RAGQueryRequest):
    result = rag_engine.query(request.query, top_k=request.top_k)
    
    token_tracker.record_usage(
        service="Document RAG",
        action=f"RAG Query: '{request.query[:30]}...'",
        prompt_tokens=340,
        completion_tokens=260,
        latency_ms=310
    )
    
    return result
