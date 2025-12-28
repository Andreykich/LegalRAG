"""FastAPI application for LegalRAG."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="LegalRAG API", version="1.0.0")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.get("/")
async def root():
    return {"name": "LegalRAG API", "status": "running"}

@app.get("/health")
async def health():
    return {"status": "healthy"}
