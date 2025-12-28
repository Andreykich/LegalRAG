# LegalRAG System Architecture

## Overview

LegalRAG is a Retrieval-Augmented Generation (RAG) system that combines semantic search with LLM generation to answer questions about legal documents.

## Components

### 1. Data Loading & Processing
- **DataLoader**: Reads JSON/JSONL documents
- **DocumentProcessor**: Chunks documents (512 words, 100-word overlap)
- **TextCleaner**: Normalizes text content

### 2. Embedding & Indexing
- **EmbeddingGenerator**: Creates embeddings using sentence-transformers
- **FAISSIndex**: Fast semantic search using FAISS
- **EmbeddingManager**: Orchestrates embedding and indexing

### 3. Retrieval & Generation
- **RAGPipeline**: Main orchestration class
- **LLMClient**: Interfaces with Mistral-7B
- **PromptManager**: Handles system prompts and templates

### 4. Safety & Validation
- **SafetyChecker**: Validates responses for hallucinations
- **ResponseValidator**: Checks grounding in sources

### 5. API Layer
- **FastAPI**: REST endpoints
- **Pydantic**: Request/response validation

## Data Flow

```
Document → Chunk → Embed → Index → Store
                                     ↓
Query → Embed → Search → Retrieve → Generate → Validate → Response
```

## Performance Targets

- Retrieval Recall@3: ≥ 0.80
- Generation Grounding: ≥ 0.90
- Latency: ≤ 500ms (GPU), ≤ 1000ms (CPU)
- Memory: ≤ 8GB

See README.md for detailed documentation.
