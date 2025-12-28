"""FastAPI application."""
import logging
import time
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from api.models import QueryRequest, QueryResponse, HealthResponse, ErrorResponse, SourceReference
from api.startup import initialize_pipeline
from src.utils import setup_logging

# Setup logging
setup_logging("INFO")
logger = logging.getLogger(__name__)

# Create app
app = FastAPI(
    title="LegalRAG API",
    description="RAG-based legal document assistant",
    version="0.1.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state
STATE = {
    "pipeline": None,
    "initialized": False,
    "error": None
}

@app.on_event("startup")
async def startup_event():
    """Initialize pipeline on startup."""
    try:
        logger.info("Initializing RAG pipeline...")
        STATE["pipeline"] = initialize_pipeline(use_mock=True)  # use_mock=True for demo
        STATE["initialized"] = True
        logger.info("Pipeline initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize pipeline: {e}")
        STATE["error"] = str(e)
        STATE["initialized"] = False

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="ok" if STATE["initialized"] else "error",
        model_loaded=STATE["initialized"],
        index_loaded=STATE["initialized"]
    )

@app.post("/ask", response_model=QueryResponse)
async def ask_question(request: QueryRequest):
    """Main query endpoint."""
    
    if not STATE["initialized"]:
        raise HTTPException(
            status_code=503,
            detail="Pipeline not initialized. Check /health endpoint."
        )
    
    try:
        start_time = time.time()
        
        # Execute query
        result = STATE["pipeline"].query(
            question=request.question,
            top_k=request.top_k,
            use_rag=request.use_rag
        )
        
        # Format response
        sources = [
            SourceReference(
                document=source['document'],
                chunk_id=source['chunk_id'],
                similarity=source['similarity']
            )
            for source in result.sources
        ]
        
        response = QueryResponse(
            question=result.question,
            answer=result.answer,
            sources=sources,
            latency_ms=result.latency_ms,
            confidence_score=result.confidence_score,
            status="success"
        )
        
        logger.info(f"Query processed: {request.question[:50]}... (latency: {result.latency_ms:.0f}ms)")
        
        return response
    
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": "LegalRAG API",
        "version": "0.1.0",
        "endpoints": {
            "health": "/health",
            "query": "/ask",
            "docs": "/docs"
        }
    }
