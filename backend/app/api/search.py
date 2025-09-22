"""
Search API endpoints
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List
from pydantic import BaseModel
from app.services.search_service import search_service
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

class SearchRequest(BaseModel):
    query: str
    num_results: int = 10
    language: str = "en"
    country: str = "us"

@router.post("/web", response_model=Dict[str, Any])
async def search_web(request: SearchRequest):
    """Perform web search"""
    try:
        result = await search_service.search_web(
            query=request.query,
            num_results=request.num_results,
            language=request.language,
            country=request.country
        )
        
        return result
        
    except Exception as e:
        logger.error(f"Error performing web search: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/news", response_model=Dict[str, Any])
async def search_news(request: SearchRequest):
    """Search for news articles"""
    try:
        result = await search_service.search_news(
            query=request.query,
            num_results=request.num_results,
            language=request.language,
            country=request.country
        )
        
        return result
        
    except Exception as e:
        logger.error(f"Error searching news: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/suggestions", response_model=Dict[str, Any])
async def get_search_suggestions(query: str):
    """Get search suggestions"""
    try:
        suggestions = await search_service.get_search_suggestions(query)
        
        return {
            "success": True,
            "query": query,
            "suggestions": suggestions
        }
        
    except Exception as e:
        logger.error(f"Error getting search suggestions: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/status", response_model=Dict[str, Any])
async def get_search_status():
    """Get search service status"""
    try:
        is_configured = search_service.is_configured()
        
        return {
            "success": True,
            "configured": is_configured,
            "service": "SerpAPI"
        }
        
    except Exception as e:
        logger.error(f"Error getting search status: {e}")
        raise HTTPException(status_code=500, detail=str(e))