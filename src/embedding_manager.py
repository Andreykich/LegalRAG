"""Embedding management using sentence-transformers."""
import logging
import numpy as np
from typing import List, Dict, Any
import faiss

logger = logging.getLogger(__name__)

class EmbeddingManager:
    """Manage embeddings and vector database."""

    def __init__(self, model_name: str = "sentence-transformers/multilingual-MiniLM-L6-v2"):
        self.model_name = model_name
        self.embeddings = None
        self.index = None
        self.documents = []

        try:
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer(model_name)
        except ImportError:
            self.model = None

    def embed_texts(self, texts: List[str]) -> np.ndarray:
        """Generate embeddings for texts."""
        if self.model is None:
            return np.random.randn(len(texts), 384).astype('float32')
        embeddings = self.model.encode(texts, convert_to_numpy=True)
        return embeddings.astype('float32')

    def build_index(self, documents: List[Dict[str, Any]]) -> None:
        """Build FAISS index from documents."""
        texts = [doc.get("content", "") for doc in documents]
        embeddings = self.embed_texts(texts)
        self.index = faiss.IndexFlatL2(embeddings.shape[1])
        self.index.add(embeddings)
        self.documents = documents

    def search(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """Search for similar documents."""
        if self.index is None:
            return []
        query_embedding = self.embed_texts([query])
        distances, indices = self.index.search(query_embedding, min(k, len(self.documents)))
        results = []
        for idx, distance in zip(indices[0], distances[0]):
            if idx < len(self.documents):
                doc = self.documents[idx].copy()
                doc["score"] = float(distance)
                results.append(doc)
        return results
