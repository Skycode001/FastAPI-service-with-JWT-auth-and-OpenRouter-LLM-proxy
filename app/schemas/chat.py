from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ChatRequest(BaseModel):
    prompt: str
    system: Optional[str] = None
    max_history: Optional[int] = 10
    temperature: Optional[float] = 0.7

class ChatResponse(BaseModel):
    answer: str

class ChatMessageResponse(BaseModel):
    id: int
    role: str
    content: str
    created_at: datetime
    
    model_config = {
        "from_attributes": True
    }