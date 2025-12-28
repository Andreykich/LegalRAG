# LegalRAG: Legal Document RAG Assistant

A RAG-based system for analyzing and searching legal documents using semantic search and LLM generation.

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Generate synthetic data:**
   ```bash
   python scripts/generate_synthetic_data.py
   ```

3. **Build index:**
   ```bash
   python scripts/build_index.py
   ```

4. **Run tests:**
   ```bash
   pytest tests/ -v
   ```

5. **Start API server:**
   ```bash
   python scripts/run_server.py
   ```

6. **Test the API:**
   ```bash
   curl -X POST http://localhost:8000/ask \
     -H "Content-Type: application/json" \
     -d '{"question": "What is NDA?", "top_k": 3}'
   ```

## Documentation

- See `docs/ARCHITECTURE.md` for system architecture
- See `docs/MODEL_CARD.md` for model details
- See `docs/SYSTEM_CARD.md` for risks and limitations
- See `report.md` for full project report
- See `presentation.md` for slide deck

## Project Structure

```
legalrag/
├── src/               # Source code
├── api/               # FastAPI application
├── data/              # Datasets and indices
├── configs/           # Configuration files
├── notebooks/         # Jupyter notebooks
├── tests/             # Unit and integration tests
├── scripts/           # Utility scripts
├── docs/              # Documentation
└── reports/           # Reports and results
```

## Configuration

All configuration is in `configs/default.yaml`. Key settings:
- Embedding model: `sentence-transformers/all-MiniLM-L6-v2`
- LLM model: `mistralai/Mistral-7B-Instruct-v0.2`
- Chunk size: 512 words
- Top-k retrieval: 3
- Device: CPU (set to CUDA if available)

## API Endpoints

- `GET /` - API info
- `GET /health` - Health check
- `POST /ask` - Query endpoint
- `GET /docs` - Interactive documentation (Swagger UI)

## Requirements

- Python 3.11+
- PyTorch
- HuggingFace Transformers
- Sentence Transformers
- FAISS
- FastAPI
- See `requirements.txt` for full list

## License

MIT License - see LICENSE file

## Contact

For questions or issues, contact: your.email@example.com
