"""Pydantic models for API."""
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class QueryRequest(BaseModel):
    """Query request model."""
    question: str = Field(..., description="User question")
    top_k: int = Field(3, description="Number of documents to retrieve")
    use_rag: bool = Field(True, description="Use RAG or zero-shot generation")
    temperature: float = Field(0.3, ge=0.0, le=1.0, description="LLM temperature")

class SourceReference(BaseModel):
    """Source reference."""
    document: str
    chunk_id: str
    similarity: float

class QueryResponse(BaseModel):
    """Query response model."""
    question: str
    answer: str
    sources: List[SourceReference]
    latency_ms: float
    confidence_score: float
    status: str = "success"

class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    model_loaded: bool
    index_loaded: bool

class ErrorResponse(BaseModel):
    """Error response."""
    status: str = "error"
    message: str
    details: Optional[Dict[str, Any]] = None
