# Model Card: LegalRAG v0.1

## Overview
- **Model**: LegalRAG (Retrieval-Augmented Generation)
- **Base LLM**: Mistral-7B-Instruct-v0.2
- **Embeddings**: sentence-transformers/all-MiniLM-L6-v2
- **Index**: FAISS (L2 distance)

## Capabilities
- Q&A over document collections
- Information extraction
- Document comparison
- Cited answers with source tracking

## Limitations
- English language only
- ~2000 token context window
- No real-time document updates
- Requires document indexing

## Performance
- Retrieval: Recall@3 = 1.00
- Generation: Grounding = 1.00
- Latency: 150-500ms

## Risks
- Hallucination: 5% residual rate
- Legal liability: Not a substitute for legal counsel
- Bias: May reflect training data biases

See SYSTEM_CARD.md for detailed risk analysis.
