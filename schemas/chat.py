from pydantic import BaseModel
from typing import List

class Message(BaseModel):
    role: str      # "user" or "assistant"
    content: str

class ChatInput(BaseModel):
    messages: List[Message]   # poori conversation history