"""Startup and initialization logic."""
import logging
from pathlib import Path
from src.config import get_config
from src.data_loader import DocumentLoader
from src.document_processor import DocumentProcessor
from src.embedding_manager import EmbeddingManager
from src.llm_client import LocalLLMClient, MockLLMClient
from src.rag_pipeline import RAGPipeline

logger = logging.getLogger(__name__)

def initialize_pipeline(use_mock: bool = False):
    """Initialize RAG pipeline."""
    
    config = get_config()
    
    # Load documents (or use mock)
    if config.data.raw_data_path.exists():
        logger.info("Loading real documents...")
        loader = DocumentLoader()
        documents = loader.load_from_json(config.data.raw_data_path)
    else:
        logger.info("Using mock documents for demo...")
        from scripts.generate_synthetic_data import generate_mock_documents
        documents = generate_mock_documents(5)
    
    # Process documents
    logger.info("Processing documents...")
    processor = DocumentProcessor(
        chunk_size=config.rag.chunk_size,
        chunk_overlap=config.rag.chunk_overlap
    )
    chunks = processor.process_documents(documents)
    
    # Build index
    logger.info("Building embedding index...")
    embedding_manager = EmbeddingManager(
        embedding_model=config.model.embedding_model_name,
        device=config.model.device,
        metric=config.rag.metric_type
    )
    embedding_manager.build_index(chunks)
    
    # Initialize LLM
    if use_mock:
        logger.info("Using MockLLMClient for demo...")
        llm_client = MockLLMClient()
    else:
        logger.info("Loading LLM model...")
        llm_client = LocalLLMClient(
            model_name=config.model.llm_model_name,
            device=config.model.device,
            quantize=config.model.quantization,
            max_tokens=config.model.llm_max_tokens,
            temperature=config.model.llm_temperature,
            top_p=config.model.llm_top_p
        )
    
    # Create pipeline
    pipeline = RAGPipeline(
        embedding_manager=embedding_manager,
        llm_client=llm_client,
        retriever_config={
            'top_k': config.rag.top_k,
            'similarity_threshold': config.rag.similarity_threshold
        },
        prompt_template=config.rag.system_prompt_template
    )
    
    logger.info("Pipeline initialized successfully")
    return pipeline
