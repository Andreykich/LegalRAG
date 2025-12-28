"""Main RAG pipeline."""
import time
import logging
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass
from src.embedding_manager import EmbeddingManager
from src.prompts import create_rag_prompt

logger = logging.getLogger(__name__)

@dataclass
class RAGResult:
    """Result of RAG query."""
    question: str
    answer: str
    retrieved_chunks: List[Dict[str, Any]]
    sources: List[Dict[str, str]]
    latency_ms: float
    confidence_score: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'question': self.question,
            'answer': self.answer,
            'retrieved_chunks': self.retrieved_chunks,
            'sources': self.sources,
            'latency_ms': self.latency_ms,
            'confidence_score': self.confidence_score
        }

class RAGPipeline:
    """Orchestrates RAG: retrieval + generation."""
    
    def __init__(
        self,
        embedding_manager: EmbeddingManager,
        llm_client,
        retriever_config: Dict[str, Any],
        prompt_template: str = "legal"
    ):
        self.embedding_manager = embedding_manager
        self.llm_client = llm_client
        self.retriever_config = retriever_config
        self.prompt_template = prompt_template
    
    def retrieve(self, query: str, top_k: int = None) -> List[Dict[str, Any]]:
        """Retrieve relevant chunks."""
        if top_k is None:
            top_k = self.retriever_config.get('top_k', 3)
        
        results = self.embedding_manager.search(query, k=top_k)
        return results
    
    def generate(
        self,
        question: str,
        retrieved_chunks: List[Dict[str, Any]]
    ) -> Tuple[str, float]:
        """Generate answer based on retrieved context."""
        
        if not retrieved_chunks:
            return "The provided documents do not contain information about this topic.", 0.0
        
        # Create prompt
        system_prompt, user_message = create_rag_prompt(
            question,
            retrieved_chunks,
            self.prompt_template
        )
        
        # Generate response
        answer = self.llm_client.generate(system_prompt, user_message)
        
        # Estimate confidence (simple heuristic)
        avg_similarity = sum(c.get('similarity_score', 0) for c in retrieved_chunks) / len(retrieved_chunks)
        confidence = float(avg_similarity)
        
        return answer, confidence
    
    def query(self, question: str, top_k: int = None, use_rag: bool = True) -> RAGResult:
        """Execute full RAG pipeline."""
        start_time = time.time()
        
        if use_rag:
            # Retrieve
            retrieved_chunks = self.retrieve(question, top_k)
            
            # Generate
            answer, confidence = self.generate(question, retrieved_chunks)
            
            # Extract sources
            sources = []
            for chunk in retrieved_chunks:
                sources.append({
                    'document': chunk['source_title'],
                    'chunk_id': chunk['chunk_id'],
                    'similarity': chunk.get('similarity_score', 0.0)
                })
        else:
            # Zero-shot: generate without retrieval
            from src.prompts import create_simple_prompt
            system_prompt, user_message = create_simple_prompt(question, self.prompt_template)
            answer = self.llm_client.generate(system_prompt, user_message)
            retrieved_chunks = []
            sources = []
            confidence = 0.0
        
        latency_ms = (time.time() - start_time) * 1000
        
        result = RAGResult(
            question=question,
            answer=answer,
            retrieved_chunks=retrieved_chunks,
            sources=sources,
            latency_ms=latency_ms,
            confidence_score=confidence
        )
        
        return result
