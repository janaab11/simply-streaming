import os
from typing import List, Optional, Dict
from .context import ChatMessage

from pydantic import BaseModel
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class ChatGPT(BaseModel):
    model: str = "gpt-3.5-turbo"
    prompt: str = "You are a helpful assistant"
    messages: Optional[List] = None
    roles: Optional[Dict] = None

    def __init__(self):
        super().__init__()
        self.messages = [{"role": "system", "content": self.prompt}]
        self.roles = {
            "user": "user",
            "bot": "assistant"
        }

    def add_history(self, history: List[ChatMessage]):
        for message in history:
            self.messages.append(
                {
                    "role": self.roles.get(message.role),
                    "content": message.content
                }
            )

    def __call__(self, usr_message: str, history: List[ChatMessage]):
        self.add_history(history)
        response = client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            stream=False,
        )
        return response.choices[0].message.content
