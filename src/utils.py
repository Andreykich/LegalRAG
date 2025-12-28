"""Utility functions."""
import json
import logging
from pathlib import Path
from typing import List, Dict, Any
import numpy as np

def setup_logging(log_level: str = "INFO") -> logging.Logger:
    """Setup logging configuration."""
    logging.basicConfig(
        level=getattr(logging, log_level),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__)

def save_json(data: Any, path: Path, indent: int = 2) -> None:
    """Save data to JSON file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=indent, ensure_ascii=False)

def load_json(path: Path) -> Any:
    """Load data from JSON file."""
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_jsonl(data: List[Dict], path: Path) -> None:
    """Save data to JSONL file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        for item in data:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')

def load_jsonl(path: Path) -> List[Dict]:
    """Load data from JSONL file."""
    data = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                data.append(json.loads(line))
    return data

def calculate_metrics(predictions: List[str], references: List[str]) -> Dict[str, float]:
    """Calculate basic text similarity metrics."""
    metrics = {}
    
    # Simple word overlap metric
    overlaps = []
    for pred, ref in zip(predictions, references):
        pred_words = set(pred.lower().split())
        ref_words = set(ref.lower().split())
        
        if pred_words and ref_words:
            overlap = len(pred_words & ref_words) / len(pred_words | ref_words)
            overlaps.append(overlap)
    
    if overlaps:
        metrics['avg_overlap'] = np.mean(overlaps)
    
    return metrics

class RangeAccumulator:
    """Accumulates values for calculation of statistics."""
    
    def __init__(self):
        self.values = []
    
    def add(self, value: float):
        self.values.append(value)
    
    def mean(self) -> float:
        return np.mean(self.values) if self.values else 0.0
    
    def std(self) -> float:
        return np.std(self.values) if self.values else 0.0
    
    def min(self) -> float:
        return np.min(self.values) if self.values else 0.0
    
    def max(self) -> float:
        return np.max(self.values) if self.values else 0.0
    
    def summary(self) -> Dict[str, float]:
        return {
            'mean': self.mean(),
            'std': self.std(),
            'min': self.min(),
            'max': self.max(),
            'count': len(self.values)
        }
