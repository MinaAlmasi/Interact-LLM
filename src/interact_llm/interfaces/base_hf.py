"""
Chat Model
"""

from datetime import datetime
from typing import List, Optional

from transformers import AutoModelForCausalLM, AutoTokenizer

from .chat import ChatMessage


class ChatHF:
    """
    Model wrapper for loading and using a HuggingFace causal language model
    """

    def __init__(
        self,
        model_id: str,
        device: Optional[str] = None,
        device_map: Optional[str] = None,
    ):
        self.model_id = model_id
        self.tokenizer = None
        self.model = None
        self.device = device
        self.device_map = device_map

    def load(self) -> None:
        """
        Lazy-loading (loads model and tokenizer if not already loaded)
        """
        if self.tokenizer is None:
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_id)

        if self.model is None:
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_id, device_map=self.device_map if self.device_map else None
            )

    def generate(self, chat: List[ChatMessage]):
        ds = datetime.today().strftime("%Y-%m-%d")
        prompt = self.tokenizer.apply_chat_template(
            chat, tokenize=False, add_generation_prompt=True, date_string=ds
        )

        inputs = self.tokenizer.encode(
            prompt, add_special_tokens=False, return_tensors="pt"
        )
        outputs = self.model.generate(
            input_ids=inputs.to(self.model.device), max_new_tokens=200
        )

        return outputs
