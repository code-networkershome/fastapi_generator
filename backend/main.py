import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from backend.models import CPS
from backend.extraction import extract_cps, refine_code
from backend.generator import generate_project
import zipfile
import io

app = FastAPI(title="FastAPI Generator API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = os.getenv("GENERATOR_API_KEY", "fastapi-gen-secret")

from fastapi import Depends, Header

async def verify_api_key(x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return x_api_key

@app.post("/api/v1/generate")
async def unified_generate(data: dict, token: str = Depends(verify_api_key)):
    idea = data.get("idea")
    if not idea:
        raise HTTPException(status_code=400, detail="Missing idea input")
    
    # 1. Extraction
    extracted_data = await extract_cps(idea)
    if "error" in extracted_data:
        raise HTTPException(status_code=500, detail=f"Extraction failed: {extracted_data['error']}")
    
    # 2. Validation (Internal)
    try:
        cps = CPS(**extracted_data)
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Validation failed: {str(e)}")
    
    # 3. Generation
    files = generate_project(cps)
    return {"project_name": cps.project_name, "files": files}

@app.post("/analyze")
async def analyze(data: dict):
    # data can be {"text": "..."} or a partial json
    text = data.get("text")
    if not text:
        raise HTTPException(status_code=400, detail="Missing text input")
    
    extracted = await extract_cps(text)
    return extracted

@app.post("/validate")
async def validate_cps(cps: CPS):
    if cps.mode == "rag_only":
        errors = []
        if not cps.features.rag:
            errors.append("features.rag MUST be true in RAG-only mode")
        if not cps.features.embeddings:
            errors.append("features.embeddings MUST be true in RAG-only mode")
        if cps.features.chat:
            errors.append("Chat-only endpoints are not allowed in RAG-only specialization.")
        if not cps.vector_store:
            errors.append("Vector store configuration is required for RAG.")
        if not cps.embedding_model:
            errors.append("Missing embedding model")
            
        if errors:
            raise HTTPException(status_code=400, detail=", ".join(errors))
            
    return {"status": "success", "data": cps}

@app.post("/generate")
async def generate(cps: CPS):
    files = generate_project(cps)
    return {"files": files}

@app.post("/refine")
async def refine(data: dict):
    cps = data.get("cps")
    files = data.get("files")
    feedback = data.get("feedback")
    
    if not cps or not files or not feedback:
        raise HTTPException(status_code=400, detail="Missing required fields: cps, files, or feedback")
    
    refined_files = await refine_code(cps, files, feedback)
    return {"files": refined_files}

@app.post("/export")
async def export_zip(data: dict):
    files = data.get("files")
    if not files:
        raise HTTPException(status_code=400, detail="No files provided")
    
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
        for path, content in files.items():
            zip_file.writestr(path, content)
    
    zip_buffer.seek(0)
    # Note: Returning as base64 or similar if needed, 
    # but the user said "GET /export" with "Input: generated files".
    # Usually we'd use StreamingResponse.
    from fastapi.responses import StreamingResponse
    return StreamingResponse(
        zip_buffer,
        media_type="application/x-zip-compressed",
        headers={"Content-Disposition": f"attachment; filename=project.zip"}
    )
