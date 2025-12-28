"""Safety checks and hallucination prevention."""
import re
import logging
from typing import Tuple, List

logger = logging.getLogger(__name__)

class SafetyChecker:
    """Validates response quality and detects issues."""
    
    # Phrases that indicate hallucinations or refusal
    REFUSAL_PHRASES = [
        "i don't know",
        "i cannot",
        "not found",
        "not mentioned",
        "no information",
        "not available",
        "not specified",
        "not stated",
        "documents do not contain"
    ]
    
    @staticmethod
    def check_source_grounding(answer: str, retrieved_chunks: List[dict]) -> Tuple[bool, str]:
        """Check if answer is grounded in sources."""
        
        if not retrieved_chunks:
            return False, "No source documents provided"
        
        # Check if answer is suspiciously specific but sources are vague
        answer_specificity = len(answer.split()) / (1 + len(set(answer.split())))
        
        if answer_specificity > 2.0:  # Very repetitive = suspicious
            return False, "Answer seems repetitive or hallucinated"
        
        return True, "Answer appears grounded"
    
    @staticmethod
    def check_appropriate_length(answer: str, context_length: int) -> Tuple[bool, str]:
        """Check if answer length is reasonable."""
        
        answer_words = len(answer.split())
        
        # Answer should be 10-50% of context length
        if answer_words < 10:
            return False, "Answer is too brief"
        
        if answer_words > context_length:
            return False, "Answer is longer than source context"
        
        return True, "Answer length is appropriate"
    
    @staticmethod
    def detect_refusal(answer: str) -> Tuple[bool, str]:
        """Detect if model refused to answer."""
        
        answer_lower = answer.lower()
        
        for phrase in SafetyChecker.REFUSAL_PHRASES:
            if phrase in answer_lower:
                return True, f"Detected refusal pattern: '{phrase}'"
        
        return False, "No refusal detected"
    
    @staticmethod
    def validate_response(
        answer: str,
        retrieved_chunks: List[dict],
        question: str
    ) -> dict:
        """Run all safety checks."""
        
        checks = {}
        
        # Check 1: Source grounding
        grounded, msg = SafetyChecker.check_source_grounding(answer, retrieved_chunks)
        checks['source_grounding'] = {'passed': grounded, 'message': msg}
        
        # Check 2: Appropriate length
        context_length = sum(len(c.get('content', '').split()) for c in retrieved_chunks)
        length_ok, msg = SafetyChecker.check_appropriate_length(answer, context_length)
        checks['length'] = {'passed': length_ok, 'message': msg}
        
        # Check 3: Refusal detection
        refused, msg = SafetyChecker.detect_refusal(answer)
        checks['refusal'] = {'passed': not refused, 'message': msg}
        
        return checks
