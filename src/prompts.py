"""System prompts and prompt templates."""
from typing import List, Dict, Any
from enum import Enum

class PromptTemplate(Enum):
    """Available prompt templates."""
    LEGAL = "legal"
    QA = "qa"
    SUMMARIZATION = "summarization"

SYSTEM_PROMPTS = {
    "legal": """You are an expert legal document analysis assistant. Your role is to help users understand and analyze legal documents.

IMPORTANT RULES:
1. Base your answers ONLY on the provided document excerpts. Do not use external knowledge about laws or regulations.
2. If the answer is not found in the provided context, respond clearly: "The provided documents do not contain information about this topic."
3. Always cite the source document when providing information.
4. Be precise and avoid speculation.
5. If there are conflicting statements in different documents, note this explicitly.
6. Structure your response clearly with:
   - Direct answer to the question
   - Supporting details from the documents
   - Source references (document name and excerpt location)

Remember: It's better to say "I don't know" than to provide incorrect legal information.""",

    "qa": """You are a helpful document analysis assistant. Answer questions based on the provided document excerpts.

INSTRUCTIONS:
1. Answer only based on the provided context.
2. If information is not available, say so clearly.
3. Cite sources for all claims.
4. Be concise but complete.
5. Organize your answer logically.""",

    "summarization": """You are a document summarization expert. Summarize the provided document excerpts.

INSTRUCTIONS:
1. Capture the main points.
2. Maintain accuracy.
3. Keep summary concise but informative.
4. Use clear structure."""
}

def create_rag_prompt(
    question: str,
    retrieved_chunks: List[Dict[str, Any]],
    template: str = "legal"
) -> str:
    """Create RAG prompt with question and context."""
    
    system_prompt = SYSTEM_PROMPTS.get(template, SYSTEM_PROMPTS["legal"])
    
    # Format context
    context_text = "\n\n---\n\n".join([
        f"**Document: {chunk['source_title']}** (Chunk {chunk['chunk_index']})\n\n{chunk['content']}"
        for chunk in retrieved_chunks
    ])
    
    user_message = f"""Based on the following document excerpts, answer the question:

QUESTION: {question}

DOCUMENT EXCERPTS:
{context_text}

ANSWER:"""
    
    return system_prompt, user_message

def create_simple_prompt(question: str, template: str = "qa") -> str:
    """Create simple prompt without context (for comparison)."""
    system_prompt = SYSTEM_PROMPTS.get(template, SYSTEM_PROMPTS["qa"])
    user_message = f"Question: {question}\n\nAnswer:"
    return system_prompt, user_message
