"""Document processing: chunking, cleaning, tokenization."""
import re
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

@dataclass
class Chunk:
    """Represents a document chunk."""
    chunk_id: str
    content: str
    source_doc_id: str
    source_title: str
    chunk_index: int
    start_char: int
    end_char: int
    metadata: Dict[str, Any] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'chunk_id': self.chunk_id,
            'content': self.content,
            'source_doc_id': self.source_doc_id,
            'source_title': self.source_title,
            'chunk_index': self.chunk_index,
            'start_char': self.start_char,
            'end_char': self.end_char,
            'metadata': self.metadata or {}
        }

class TextCleaner:
    """Cleans and normalizes text."""
    
    @staticmethod
    def clean(text: str) -> str:
        """Apply cleaning pipeline."""
        # Remove multiple spaces
        text = re.sub(r' +', ' ', text)
        # Remove leading/trailing whitespace
        text = text.strip()
        # Normalize line breaks
        text = re.sub(r'\n\s*\n', '\n\n', text)
        return text
    
    @staticmethod
    def remove_special_chars(text: str, keep_punctuation: bool = True) -> str:
        """Remove special characters (optionally keep punctuation)."""
        if keep_punctuation:
            # Keep letters, digits, punctuation, spaces, newlines
            text = re.sub(r'[^\w\s\.\,\!\?\:\;\-\(\)\"\']', '', text, flags=re.UNICODE)
        else:
            text = re.sub(r'[^\w\s]', '', text, flags=re.UNICODE)
        return text

class DocumentChunker:
    """Splits documents into overlapping chunks."""
    
    def __init__(self, chunk_size: int = 512, chunk_overlap: int = 100):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        assert chunk_overlap < chunk_size, "Overlap must be smaller than chunk size"
    
    def chunk_document(self, doc_id: str, title: str, content: str) -> List[Chunk]:
        """Split document into chunks with overlap."""
        chunks = []
        words = content.split()
        
        current_pos = 0
        chunk_index = 0
        
        while current_pos < len(words):
            # Extract chunk of words
            chunk_words = words[current_pos:current_pos + self.chunk_size]
            chunk_text = ' '.join(chunk_words)
            
            # Find start and end character positions (approximate)
            start_char = sum(len(w) + 1 for w in words[:current_pos])
            end_char = start_char + len(chunk_text)
            
            chunk = Chunk(
                chunk_id=f"{doc_id}_chunk_{chunk_index}",
                content=chunk_text,
                source_doc_id=doc_id,
                source_title=title,
                chunk_index=chunk_index,
                start_char=start_char,
                end_char=end_char
            )
            chunks.append(chunk)
            
            # Move position with overlap
            current_pos += (self.chunk_size - self.chunk_overlap)
            chunk_index += 1
        
        return chunks if chunks else [
            Chunk(
                chunk_id=f"{doc_id}_chunk_0",
                content=content,
                source_doc_id=doc_id,
                source_title=title,
                chunk_index=0,
                start_char=0,
                end_char=len(content)
            )
        ]

class DocumentProcessor:
    """Main document processing pipeline."""
    
    def __init__(self, chunk_size: int = 512, chunk_overlap: int = 100):
        self.chunker = DocumentChunker(chunk_size, chunk_overlap)
        self.cleaner = TextCleaner()
    
    def process_documents(self, documents: List) -> List[Chunk]:
        """Process list of documents into chunks."""
        chunks = []
        
        for doc in documents:
            # Clean text
            cleaned_content = self.cleaner.clean(doc.content)
            
            # Chunk
            doc_chunks = self.chunker.chunk_document(
                doc.doc_id,
                doc.title,
                cleaned_content
            )
            
            chunks.extend(doc_chunks)
        
        logger.info(f"Processed {len(documents)} documents into {len(chunks)} chunks")
        return chunks
