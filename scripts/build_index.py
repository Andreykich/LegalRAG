"""Build FAISS index from documents."""
import logging
from pathlib import Path
from src.config import get_config
from src.data_loader import DocumentLoader, DataValidator
from src.document_processor import DocumentProcessor
from src.embedding_manager import EmbeddingManager
from src.utils import setup_logging, save_jsonl

setup_logging("INFO")
logger = logging.getLogger(__name__)

def main():
    """Build index."""
    config = get_config()
    
    # Load documents
    logger.info("Loading documents...")
    loader = DocumentLoader()
    documents = loader.load_from_json(config.data.raw_data_path)
    
    # Validate
    logger.info("Validating data...")
    checks = DataValidator.validate_all(documents)
    for check in checks:
        logger.info(f"  {check['check']}: {check['details']}")
    
    # Process
    logger.info("Processing documents...")
    processor = DocumentProcessor(
        chunk_size=config.rag.chunk_size,
        chunk_overlap=config.rag.chunk_overlap
    )
    chunks = processor.process_documents(documents)
    
    # Save chunks
    logger.info(f"Saving {len(chunks)} chunks...")
    chunk_dicts = [c.to_dict() for c in chunks]
    save_jsonl(chunk_dicts, config.data.processed_data_path)
    
    # Build embeddings and index
    logger.info("Building embedding index...")
    embedding_manager = EmbeddingManager(
        embedding_model=config.model.embedding_model_name,
        device=config.model.device,
        metric=config.rag.metric_type
    )
    
    index = embedding_manager.build_index(chunks)
    index.save(config.data.index_path)
    
    logger.info("Index built successfully!")
    logger.info(f"  Documents: {len(documents)}")
    logger.info(f"  Chunks: {len(chunks)}")
    logger.info(f"  Index path: {config.data.index_path}")

if __name__ == "__main__":
    main()
