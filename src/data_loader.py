"""Data loading utilities for LegalRAG."""
import json
import logging
from pathlib import Path
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class DataLoader:
    """Load legal documents from various sources."""

    def __init__(self, data_path: str = "data/raw"):
        self.data_path = Path(data_path)
        self.data_path.mkdir(parents=True, exist_ok=True)

    def load_json_documents(self) -> List[Dict[str, Any]]:
        """Load documents from JSON files."""
        documents = []
        for json_file in self.data_path.glob("*.json"):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        documents.extend(data)
                    else:
                        documents.append(data)
            except Exception as e:
                logger.error(f"Error loading {json_file.name}: {e}")
        return documents

    def load_all_documents(self) -> List[Dict[str, Any]]:
        return self.load_json_documents()
