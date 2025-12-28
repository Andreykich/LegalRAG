"""Embedding generation and FAISS index management."""
import json
import numpy as np
import logging
from pathlib import Path
from typing import List, Tuple, Dict, Any
import faiss
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)

class EmbeddingGenerator:
    """Generates embeddings using sentence-transformers."""
    
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2", device: str = "cpu"):
        logger.info(f"Loading embedding model: {model_name}")
        self.model = SentenceTransformer(model_name, device=device)
        self.embedding_dim = self.model.get_sentence_embedding_dimension()
        logger.info(f"Embedding dimension: {self.embedding_dim}")
    
    def encode(self, texts: List[str]) -> np.ndarray:
        """Encode texts to embeddings."""
        embeddings = self.model.encode(texts, convert_to_numpy=True, show_progress_bar=True)
        return embeddings

class FAISSIndex:
    """FAISS index for fast similarity search."""
    
    def __init__(self, embedding_dim: int, metric: str = "l2"):
        self.embedding_dim = embedding_dim
        self.metric = metric
        
        if metric == "l2":
            self.index = faiss.IndexFlatL2(embedding_dim)
        elif metric == "cosine":
            # For cosine, normalize vectors
            self.index = faiss.IndexFlatIP(embedding_dim)
        else:
            raise ValueError(f"Unknown metric: {metric}")
        
        self.chunk_metadata = []
    
    def add(self, embeddings: np.ndarray, metadata: List[Dict[str, Any]]):
        """Add embeddings and metadata to index."""
        if isinstance(embeddings, list):
            embeddings = np.array(embeddings, dtype=np.float32)
        
        # Ensure correct dtype and shape
        embeddings = np.asarray(embeddings, dtype=np.float32)
        if embeddings.ndim == 1:
            embeddings = embeddings.reshape(1, -1)
        
        # Normalize for cosine similarity if needed
        if self.metric == "cosine":
            faiss.normalize_L2(embeddings)
        
        self.index.add(embeddings)
        self.chunk_metadata.extend(metadata)
        
        logger.info(f"Added {len(embeddings)} embeddings. Total: {self.index.ntotal}")
    
    def search(self, query_embedding: np.ndarray, k: int = 5) -> Tuple[np.ndarray, np.ndarray]:
        """Search for k nearest neighbors."""
        if query_embedding.ndim == 1:
            query_embedding = query_embedding.reshape(1, -1)
        
        query_embedding = np.asarray(query_embedding, dtype=np.float32)
        
        if self.metric == "cosine":
            faiss.normalize_L2(query_embedding)
        
        distances, indices = self.index.search(query_embedding, k)
        return distances[0], indices[0]
    
    def save(self, path: Path):
        """Save index to disk."""
        path.parent.mkdir(parents=True, exist_ok=True)
        faiss.write_index(self.index, str(path))
        
        # Save metadata separately
        metadata_path = path.parent / (path.stem + "_metadata.json")
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(self.chunk_metadata, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Saved index to {path} and metadata to {metadata_path}")
    
    @classmethod
    def load(cls, path: Path, metric: str = "l2") -> 'FAISSIndex':
        """Load index from disk."""
        index = faiss.read_index(str(path))
        embedding_dim = index.d
        
        obj = cls(embedding_dim, metric)
        obj.index = index
        
        # Load metadata
        metadata_path = path.parent / (path.stem + "_metadata.json")
        if metadata_path.exists():
            with open(metadata_path, 'r', encoding='utf-8') as f:
                obj.chunk_metadata = json.load(f)
        
        logger.info(f"Loaded index from {path} with {index.ntotal} embeddings")
        return obj

class EmbeddingManager:
    """Manages embedding generation and indexing."""
    
    def __init__(self, embedding_model: str, device: str = "cpu", metric: str = "l2"):
        self.embedding_generator = EmbeddingGenerator(embedding_model, device)
        self.index = None
        self.metric = metric
    
    def build_index(self, chunks: List) -> FAISSIndex:
        """Build FAISS index from chunks."""
        logger.info(f"Building index from {len(chunks)} chunks")
        
        # Generate embeddings
        chunk_texts = [chunk.content for chunk in chunks]
        embeddings = self.embedding_generator.encode(chunk_texts)
        
        # Create index
        self.index = FAISSIndex(
            embedding_dim=embeddings.shape[1],
            metric=self.metric
        )
        
        # Prepare metadata
        metadata = [chunk.to_dict() for chunk in chunks]
        
        # Add to index
        self.index.add(embeddings, metadata)
        
        return self.index
    
    def search(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """Search for similar chunks."""
        query_embedding = self.embedding_generator.encode([query])
        distances, indices = self.index.search(query_embedding[0], k)
        
        results = []
        for distance, idx in zip(distances, indices):
            if idx < len(self.index.chunk_metadata):
                chunk_meta = self.index.chunk_metadata[int(idx)]
                results.append({
                    **chunk_meta,
                    'similarity_score': float(1 / (1 + distance)) if self.metric == "l2" else float(distance)
                })
        
        return results
