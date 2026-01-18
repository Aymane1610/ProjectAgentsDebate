import os
import shutil
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

from core.rag import rag_engine
from core.agents import debate_manager

app = FastAPI(title="DEBATE CORE RAG API")

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str

@app.post("/query")
async def process_query(request: QueryRequest):
    # 1. Search knowledge base
    context_chunks = rag_engine.search(request.query)
    
    if not context_chunks:
        return {"error": "No relevant information found in the knowledge base."}
    
    # 2. Conduct debate
    debate_results = await debate_manager.conduct_debate(request.query, context_chunks)
    
    return {
        "query": request.query,
        "debate_rounds": debate_results,
        "sources": list(set([c['source'] for c in context_chunks]))
    }

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")
    
    target_path = os.path.join("knowledge_base", file.filename)
    with open(target_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Refresh index
    rag_engine.refresh_index()
    
    return {"message": f"File '{file.filename}' uploaded and indexed successfully."}

@app.get("/status")
async def get_status():
    return {
        "index_ready": rag_engine.index is not None,
        "chunk_count": len(rag_engine.chunks),
        "files_indexed": list(set([c['source'] for c in rag_engine.chunk_metadata])) if rag_engine.chunk_metadata else []
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
