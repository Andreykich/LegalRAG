"""Tests for RAG pipeline."""
import pytest
from unittest.mock import Mock, MagicMock
from src.rag_pipeline import RAGPipeline, RAGResult

@pytest.fixture
def mock_embedding_manager():
    """Mock embedding manager."""
    mock = Mock()
    mock.search.return_value = [
        {
            'chunk_id': 'doc1_chunk_0',
            'content': 'This is a test contract.',
            'source_title': 'Test Contract',
            'similarity_score': 0.95
        }
    ]
    return mock

@pytest.fixture
def mock_llm_client():
    """Mock LLM client."""
    mock = Mock()
    mock.generate.return_value = "Based on the contract, clause A states..."
    return mock

@pytest.fixture
def pipeline(mock_embedding_manager, mock_llm_client):
    """Create test pipeline."""
    return RAGPipeline(
        embedding_manager=mock_embedding_manager,
        llm_client=mock_llm_client,
        retriever_config={'top_k': 3},
        prompt_template='legal'
    )

def test_retrieve(pipeline, mock_embedding_manager):
    """Test retrieval."""
    results = pipeline.retrieve("What is clause A?", top_k=3)
    
    assert len(results) == 1
    assert results[0]['source_title'] == 'Test Contract'
    mock_embedding_manager.search.assert_called_once()

def test_generate(pipeline, mock_llm_client):
    """Test generation."""
    chunks = [{
        'content': 'Test content',
        'source_title': 'Test Doc',
        'chunk_index': 0
    }]
    
    answer, confidence = pipeline.generate("Test question?", chunks)
    
    assert isinstance(answer, str)
    assert isinstance(confidence, float)
    mock_llm_client.generate.assert_called_once()

def test_query_with_rag(pipeline):
    """Test full RAG query."""
    result = pipeline.query("Test question?", use_rag=True)
    
    assert isinstance(result, RAGResult)
    assert result.question == "Test question?"
    assert len(result.sources) > 0
    assert result.latency_ms > 0

def test_query_without_rag(pipeline):
    """Test zero-shot query."""
    result = pipeline.query("Test question?", use_rag=False)
    
    assert isinstance(result, RAGResult)
    assert len(result.sources) == 0

def test_empty_retrieval(pipeline, mock_embedding_manager):
    """Test handling of empty retrieval results."""
    mock_embedding_manager.search.return_value = []
    
    result = pipeline.query("Unknown topic?", use_rag=True)
    
    assert "do not contain" in result.answer.lower() or result.answer != ""
