"""Data loading and document parsing module."""
import json
from pathlib import Path
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class Document:
    """Represents a single document."""
    
    def __init__(self, doc_id: str, title: str, content: str, source: str, metadata: Dict[str, Any] = None):
        self.doc_id = doc_id
        self.title = title
        self.content = content
        self.source = source
        self.metadata = metadata or {}
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'doc_id': self.doc_id,
            'title': self.title,
            'content': self.content,
            'source': self.source,
            'metadata': self.metadata
        }

class DocumentLoader:
    """Loads documents from various sources."""
    
    @staticmethod
    def load_from_json(filepath: Path) -> List[Document]:
        """Load documents from JSON file."""
        logger.info(f"Loading documents from {filepath}")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        documents = []
        for item in data:
            doc = Document(
                doc_id=item.get('id', str(len(documents))),
                title=item.get('title', 'Untitled'),
                content=item.get('content', ''),
                source=item.get('source', 'unknown'),
                metadata=item.get('metadata', {})
            )
            documents.append(doc)
        
        logger.info(f"Loaded {len(documents)} documents")
        return documents
    
    @staticmethod
    def load_from_jsonl(filepath: Path) -> List[Document]:
        """Load documents from JSONL file."""
        logger.info(f"Loading documents from {filepath}")
        documents = []
        
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                item = json.loads(line)
                doc = Document(
                    doc_id=item.get('id', str(len(documents))),
                    title=item.get('title', 'Untitled'),
                    content=item.get('content', ''),
                    source=item.get('source', 'unknown'),
                    metadata=item.get('metadata', {})
                )
                documents.append(doc)
        
        logger.info(f"Loaded {len(documents)} documents")
        return documents

class DataValidator:
    """Validates data quality."""
    
    @staticmethod
    def check_empty_content(documents: List[Document]) -> Dict[str, Any]:
        """Check for documents with empty content."""
        empty_docs = [d for d in documents if not d.content or len(d.content.strip()) == 0]
        return {
            'check': 'empty_content',
            'passed': len(empty_docs) == 0,
            'count': len(empty_docs),
            'details': f"{len(empty_docs)}/{len(documents)} documents have empty content"
        }
    
    @staticmethod
    def check_duplicates(documents: List[Document]) -> Dict[str, Any]:
        """Check for duplicate documents."""
        seen_content = set()
        duplicates = []
        
        for doc in documents:
            content_hash = hash(doc.content[:100])
            if content_hash in seen_content:
                duplicates.append(doc.doc_id)
            seen_content.add(content_hash)
        
        return {
            'check': 'duplicates',
            'passed': len(duplicates) == 0,
            'count': len(duplicates),
            'details': f"Found {len(duplicates)} potential duplicates"
        }
    
    @staticmethod
    def check_min_length(documents: List[Document], min_length: int = 100) -> Dict[str, Any]:
        """Check for documents below minimum length."""
        short_docs = [d for d in documents if len(d.content) < min_length]
        return {
            'check': 'min_length',
            'passed': len(short_docs) == 0,
            'count': len(short_docs),
            'details': f"{len(short_docs)}/{len(documents)} documents shorter than {min_length} chars"
        }
    
    @staticmethod
    def validate_all(documents: List[Document]) -> List[Dict[str, Any]]:
        """Run all validation checks."""
        return [
            DataValidator.check_empty_content(documents),
            DataValidator.check_duplicates(documents),
            DataValidator.check_min_length(documents),
        ]
