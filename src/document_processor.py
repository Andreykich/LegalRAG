"""Document processing utilities."""
import re
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class DocumentProcessor:
    """Process legal documents for RAG."""

    def __init__(self, chunk_size: int = 512, overlap: int = 100):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def clean_text(self, text: str) -> str:
        """Clean text by removing extra whitespace."""
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    def chunk_document(self, text: str, doc_id: str = "") -> List[Dict[str, Any]]:
        """Split document into chunks."""
        chunks = []
        text = self.clean_text(text)

        for i in range(0, len(text), self.chunk_size - self.overlap):
            chunk_text = text[i:i + self.chunk_size]
            if len(chunk_text) > 50:
                chunks.append({
                    "id": f"{doc_id}_chunk_{len(chunks)}",
                    "content": chunk_text,
                    "doc_id": doc_id
                })
        return chunks

    def process_documents(self, documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Process multiple documents."""
        processed = []
        for doc in documents:
            content = doc.get("content", "")
            doc_id = doc.get("id", "unknown")
            chunks = self.chunk_document(content, doc_id)
            processed.extend(chunks)
        return processed
