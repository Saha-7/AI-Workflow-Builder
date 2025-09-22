from pydantic import BaseModel
from typing import Optional, Dict, Any

class LLMRequest(BaseModel):
    query: str
    context: Optional[str] = None
    model: Optional[str] = "gpt-3.5-turbo"
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = 1000
    prompt: Optional[str] = None
    use_web_search: Optional[bool] = False

class LLMResponse(BaseModel):
    response: str
    model_used: str
    tokens_used: Optional[int] = None
    processing_time: Optional[float] = None







