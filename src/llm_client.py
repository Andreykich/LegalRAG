"""LLM client for inference."""
import logging
import torch
from typing import Optional
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

logger = logging.getLogger(__name__)

class LocalLLMClient:
    """Local LLM inference client."""
    
    def __init__(
        self,
        model_name: str = "mistralai/Mistral-7B-Instruct-v0.2",
        device: str = "cpu",
        quantize: bool = False,
        max_tokens: int = 512,
        temperature: float = 0.3,
        top_p: float = 0.9
    ):
        self.model_name = model_name
        self.device = device
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.top_p = top_p
        
        logger.info(f"Loading model: {model_name}")
        
        # Load tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
        
        # Load model
        model_kwargs = {
            "device_map": "auto" if device == "cuda" else None,
            "torch_dtype": torch.float16 if device == "cuda" else torch.float32,
        }
        
        if quantize and device == "cuda":
            model_kwargs["load_in_8bit"] = True
        
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            **model_kwargs
        )
        
        logger.info(f"Model loaded successfully. Device: {self.device}")
    
    def generate(
        self,
        system_prompt: str,
        user_message: str,
        max_tokens: Optional[int] = None
    ) -> str:
        """Generate response."""
        
        max_tokens = max_tokens or self.max_tokens
        
        # Format message (Mistral format)
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
        
        # Encode
        input_ids = self.tokenizer.apply_chat_template(
            messages,
            tokenize=True,
            add_generation_prompt=True,
            return_tensors="pt"
        ).to(self.device)
        
        # Generate
        with torch.no_grad():
            output_ids = self.model.generate(
                input_ids,
                max_new_tokens=max_tokens,
                temperature=self.temperature,
                top_p=self.top_p,
                do_sample=True,
                eos_token_id=self.tokenizer.eos_token_id,
            )
        
        # Decode
        response = self.tokenizer.decode(
            output_ids[0][input_ids.shape[1]:],
            skip_special_tokens=True
        ).strip()
        
        return response

class MockLLMClient:
    """Mock LLM client for testing (doesn't require model download)."""
    
    def __init__(self, **kwargs):
        logger.info("Using MockLLMClient (for testing/demo purposes)")
    
    def generate(self, system_prompt: str, user_message: str, max_tokens: Optional[int] = None) -> str:
        """Return mock response."""
        # Simple mock response
        if "what" in user_message.lower():
            return "Based on the provided documents, this question pertains to key information that is outlined in the source materials. The documents indicate that proper understanding requires careful review of the excerpts provided above."
        elif "how" in user_message.lower():
            return "According to the documents, the process involves several important steps and considerations as detailed in the relevant sections of the source material."
        else:
            return "The provided documents contain relevant information on this topic. Please refer to the specific excerpts highlighted in the sources above for detailed information."
