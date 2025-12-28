"""Generate synthetic legal documents."""
import json
from pathlib import Path

documents = [
    {
        "id": "contract_001",
        "title": "Service Agreement",
        "content": "SERVICE AGREEMENT - This is a sample contract...",
        "type": "contract"
    }
]

data_dir = Path("data/raw")
data_dir.mkdir(parents=True, exist_ok=True)

with open(data_dir / "sample_documents.json", 'w') as f:
    json.dump(documents, f)

print(f"Generated {len(documents)} documents")
