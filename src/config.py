"""Configuration management for LegalRAG."""
import os
from dataclasses import dataclass
from typing import Optional

@dataclass
class RAGConfig:
    """RAG Pipeline Configuration."""
    embedding_model: str = "sentence-transformers/multilingual-MiniLM-L6-v2"
    llm_model_name: str = "gpt-3.5-turbo"
    llm_api_key: Optional[str] = None
    vector_db_type: str = "faiss"
    vector_db_path: str = "data/vector_db"
    data_path: str = "data/raw"
    processed_data_path: str = "data/processed"
    chunk_size: int = 512
    chunk_overlap: int = 100
    top_k: int = 5
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    enable_safety_check: bool = True

def load_config():
    config = RAGConfig()
    if os.getenv("LLM_API_KEY"):
        config.llm_api_key = os.getenv("LLM_API_KEY")
    return config
