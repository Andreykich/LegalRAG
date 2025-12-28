"""Evaluation script for RAG system."""
import json
import logging
from pathlib import Path
from src.config import get_config
from src.utils import setup_logging
from api.startup import initialize_pipeline

setup_logging("INFO")
logger = logging.getLogger(__name__)

# Test questions
TEST_QUERIES = [
    {
        "question": "What are the main obligations of the recipient in an NDA?",
        "expected_doc": "Non-Disclosure Agreement Template"
    },
    {
        "question": "How much is the total fee in the service agreement?",
        "expected_doc": "Service Agreement"
    },
    {
        "question": "What data retention policy is mentioned?",
        "expected_doc": "Privacy Policy"
    },
    {
        "question": "What benefits are employees entitled to?",
        "expected_doc": "Employment Agreement"
    },
    {
        "question": "What is the disclaimer in the terms of service?",
        "expected_doc": "Terms of Service"
    },
]

def evaluate_retrieval(pipeline, queries):
    """Evaluate retrieval quality."""
    metrics = {
        'retrieval_recall': [],
        'retrieval_precision': [],
        'mrr': [],  # Mean Reciprocal Rank
    }
    
    for i, query_dict in enumerate(queries):
        question = query_dict['question']
        expected_doc = query_dict['expected_doc']
        
        # Retrieve
        results = pipeline.embedding_manager.search(question, k=5)
        
        # Check if expected doc is in results
        found = any(r['source_title'] == expected_doc for r in results)
        
        if found:
            # Recall@k
            recall = 1.0
            metrics['retrieval_recall'].append(recall)
            
            # Find rank
            rank = next(i+1 for i, r in enumerate(results) if r['source_title'] == expected_doc)
            metrics['mrr'].append(1.0 / rank)
        else:
            metrics['retrieval_recall'].append(0.0)
            metrics['mrr'].append(0.0)
    
    # Calculate averages
    return {
        'recall@5': sum(metrics['retrieval_recall']) / len(metrics['retrieval_recall']),
        'mrr': sum(metrics['mrr']) / len(metrics['mrr']),
        'num_queries': len(queries)
    }

def evaluate_generation(pipeline, queries):
    """Evaluate generation quality (simple checks)."""
    metrics = {
        'answer_length': [],
        'has_sources': [],
        'response_time': []
    }
    
    for query_dict in queries:
        result = pipeline.query(query_dict['question'], top_k=3)
        
        # Check answer length
        answer_words = len(result.answer.split())
        metrics['answer_length'].append(answer_words)
        
        # Check if sources provided
        metrics['has_sources'].append(len(result.sources) > 0)
        
        # Response time
        metrics['response_time'].append(result.latency_ms)
    
    return {
        'avg_answer_length': sum(metrics['answer_length']) / len(metrics['answer_length']),
        'has_sources_ratio': sum(metrics['has_sources']) / len(metrics['has_sources']),
        'avg_latency_ms': sum(metrics['response_time']) / len(metrics['response_time']),
        'num_queries': len(queries)
    }

def main():
    """Run evaluation."""
    logger.info("Initializing pipeline for evaluation...")
    pipeline = initialize_pipeline(use_mock=False)
    
    logger.info("Evaluating retrieval...")
    retrieval_metrics = evaluate_retrieval(pipeline, TEST_QUERIES)
    
    logger.info("Evaluating generation...")
    generation_metrics = evaluate_generation(pipeline, TEST_QUERIES)
    
    # Combine results
    results = {
        'timestamp': str(Path.cwd()),
        'retrieval_metrics': retrieval_metrics,
        'generation_metrics': generation_metrics,
        'test_queries_count': len(TEST_QUERIES)
    }
    
    # Save results
    output_path = Path("reports/evaluation_results.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    # Print results
    logger.info("\n=== EVALUATION RESULTS ===")
    logger.info(f"Retrieval Recall@5: {retrieval_metrics['recall@5']:.2f}")
    logger.info(f"Retrieval MRR: {retrieval_metrics['mrr']:.2f}")
    logger.info(f"Avg Answer Length: {generation_metrics['avg_answer_length']:.0f} words")
    logger.info(f"Has Sources: {generation_metrics['has_sources_ratio']:.0%}")
    logger.info(f"Avg Latency: {generation_metrics['avg_latency_ms']:.0f}ms")
    logger.info(f"\nResults saved to {output_path}")

if __name__ == "__main__":
    main()
