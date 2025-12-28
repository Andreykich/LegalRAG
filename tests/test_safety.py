"""Tests for safety checks."""
import pytest
from src.safety import SafetyChecker

def test_detect_refusal():
    """Test refusal detection."""
    
    # Should detect refusal
    refused, msg = SafetyChecker.detect_refusal("I don't know about this topic.")
    assert refused is True
    
    # Should not detect refusal
    refused, msg = SafetyChecker.detect_refusal("Based on the documents, the answer is...")
    assert refused is False

def test_check_appropriate_length():
    """Test length validation."""
    
    # Too short
    ok, msg = SafetyChecker.check_appropriate_length("Hi", 500)
    assert ok is False
    
    # Appropriate
    ok, msg = SafetyChecker.check_appropriate_length(
        "Based on the documents, the clause states that all parties must comply with regulations.",
        500
    )
    assert ok is True

def test_validate_response():
    """Test full response validation."""
    
    answer = "According to the contract, clause A requires all parties to comply."
    chunks = [
        {
            'content': 'This is clause A content.' * 20,
            'source_title': 'Contract'
        }
    ]
    
    checks = SafetyChecker.validate_response(answer, chunks, "What is clause A?")
    
    assert 'refusal' in checks
    assert 'length' in checks
    assert 'source_grounding' in checks
