"""Configuration module for LegalRAG system."""
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional
import yaml

PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
MODELS_DIR = PROJECT_ROOT / "models"
CONFIGS_DIR = PROJECT_ROOT / "configs"

@dataclass
class ModelConfig:
    """Configuration for LLM and embedding models."""
    embedding_model_name: str = "sentence-transformers/all-MiniLM-L6-v2"
    embedding_dim: int = 384
    
    llm_model_name: str = "mistralai/Mistral-7B-Instruct-v0.2"
    llm_max_tokens: int = 512
    llm_temperature: float = 0.3
    llm_top_p: float = 0.9
    
    device: str = "cpu"  # "cpu" or "cuda"
    quantization: bool = False  # Use 8-bit quantization for memory efficiency

@dataclass
class RAGConfig:
    """Configuration for RAG pipeline."""
    # Retrieval
    chunk_size: int = 512
    chunk_overlap: int = 100
    top_k: int = 3
    similarity_threshold: float = 0.5
    
    # Indexing
    index_type: str = "faiss"  # "faiss" or "chroma"
    metric_type: str = "l2"
    
    # Generation
    max_source_tokens: int = 2000
    system_prompt_template: str = "legal"  # Шаблон промпта
    
    # Safety
    enable_safety_checks: bool = True
    check_hallucination: bool = True
    max_refusal_rate: float = 0.1

@dataclass
class DataConfig:
    """Configuration for data handling."""
    raw_data_path: Path = DATA_DIR / "raw" / "sample_legal_docs.json"
    processed_data_path: Path = DATA_DIR / "processed" / "chunks.jsonl"
    index_path: Path = DATA_DIR / "indices" / "faiss_index.bin"
    metadata_path: Path = DATA_DIR / "indices" / "metadata.json"
    
    test_split: float = 0.1
    val_split: float = 0.1
    random_seed: int = 42

@dataclass
class APIConfig:
    """Configuration for FastAPI server."""
    host: str = "0.0.0.0"
    port: int = 8000
    reload: bool = True
    workers: int = 1
    timeout: float = 30.0

@dataclass
class EvaluationConfig:
    """Configuration for evaluation."""
    num_eval_samples: int = 20
    metrics: list = None
    
    def __post_init__(self):
        if self.metrics is None:
            self.metrics = ["retrieval_recall@3", "retrieval_precision@3", "generation_quality"]

class AppConfig:
    """Main application configuration."""
    
    def __init__(self, config_path: Optional[str] = None):
        self.model = ModelConfig()
        self.rag = RAGConfig()
        self.data = DataConfig()
        self.api = APIConfig()
        self.evaluation = EvaluationConfig()
        
        if config_path:
            self.load_from_yaml(config_path)
    
    def load_from_yaml(self, config_path: str):
        """Load configuration from YAML file."""
        with open(config_path, 'r') as f:
            config_dict = yaml.safe_load(f)
        
        if 'model' in config_dict:
            self.__dict__['model'] = ModelConfig(**config_dict['model'])
        if 'rag' in config_dict:
            self.__dict__['rag'] = RAGConfig(**config_dict['rag'])
        if 'data' in config_dict:
            self.__dict__['data'] = DataConfig(**config_dict['data'])
        if 'api' in config_dict:
            self.__dict__['api'] = APIConfig(**config_dict['api'])
        if 'evaluation' in config_dict:
            self.__dict__['evaluation'] = EvaluationConfig(**config_dict['evaluation'])

def get_config(config_path: Optional[str] = None) -> AppConfig:
    """Get application configuration."""
    return AppConfig(config_path)
