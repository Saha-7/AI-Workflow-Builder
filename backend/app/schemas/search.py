from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class SearchRequest(BaseModel):
    query: str
    num_results: Optional[int] = 10
    search_engine: Optional[str] = "google"

class SearchResult(BaseModel):
    title: str
    url: str
    snippet: str
    position: int

class SearchResponse(BaseModel):
    query: str
    results: List[SearchResult]
    total_results: int
    search_engine: str







