"""
Search Service - Handles web search using SerpAPI
"""
import httpx
from typing import Dict, Any, List, Optional
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

class SearchService:
    def __init__(self):
        self.api_key = settings.serpapi_key
        self.base_url = "https://serpapi.com/search"
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def search_web(
        self,
        query: str,
        num_results: int = 10,
        language: str = "en",
        country: str = "us"
    ) -> Dict[str, Any]:
        """
        Perform web search using SerpAPI
        
        Args:
            query: Search query
            num_results: Number of results to return
            language: Search language
            country: Search country
            
        Returns:
            Dict containing search results
        """
        try:
            if not self.api_key:
                return {
                    "success": False,
                    "error": "SerpAPI key not configured",
                    "results": []
                }
            
            params = {
                "q": query,
                "api_key": self.api_key,
                "num": num_results,
                "hl": language,
                "gl": country,
                "engine": "google"
            }
            
            response = await self.client.get(self.base_url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            # Extract search results
            search_results = []
            if "organic_results" in data:
                for result in data["organic_results"]:
                    search_results.append({
                        "title": result.get("title", ""),
                        "link": result.get("link", ""),
                        "snippet": result.get("snippet", ""),
                        "position": result.get("position", 0)
                    })
            
            # Extract answer box if available
            answer_box = None
            if "answer_box" in data:
                answer_box = {
                    "answer": data["answer_box"].get("answer", ""),
                    "type": data["answer_box"].get("type", ""),
                    "source": data["answer_box"].get("source", {})
                }
            
            logger.info(f"Found {len(search_results)} web search results")
            
            return {
                "success": True,
                "query": query,
                "results": search_results,
                "answer_box": answer_box,
                "total_results": len(search_results)
            }
            
        except httpx.HTTPError as e:
            logger.error(f"HTTP error during web search: {e}")
            return {
                "success": False,
                "error": f"HTTP error: {str(e)}",
                "results": []
            }
        except Exception as e:
            logger.error(f"Error performing web search: {e}")
            return {
                "success": False,
                "error": str(e),
                "results": []
            }
    
    async def search_news(
        self,
        query: str,
        num_results: int = 10,
        language: str = "en",
        country: str = "us"
    ) -> Dict[str, Any]:
        """
        Search for news articles
        
        Args:
            query: Search query
            num_results: Number of results to return
            language: Search language
            country: Search country
            
        Returns:
            Dict containing news results
        """
        try:
            if not self.api_key:
                return {
                    "success": False,
                    "error": "SerpAPI key not configured",
                    "results": []
                }
            
            params = {
                "q": query,
                "api_key": self.api_key,
                "num": num_results,
                "hl": language,
                "gl": country,
                "engine": "google",
                "tbm": "nws"  # News search
            }
            
            response = await self.client.get(self.base_url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            # Extract news results
            news_results = []
            if "news_results" in data:
                for result in data["news_results"]:
                    news_results.append({
                        "title": result.get("title", ""),
                        "link": result.get("link", ""),
                        "snippet": result.get("snippet", ""),
                        "date": result.get("date", ""),
                        "source": result.get("source", "")
                    })
            
            logger.info(f"Found {len(news_results)} news results")
            
            return {
                "success": True,
                "query": query,
                "results": news_results,
                "total_results": len(news_results)
            }
            
        except Exception as e:
            logger.error(f"Error searching news: {e}")
            return {
                "success": False,
                "error": str(e),
                "results": []
            }
    
    async def get_search_suggestions(self, query: str) -> List[str]:
        """
        Get search suggestions for a query
        
        Args:
            query: Partial query string
            
        Returns:
            List of suggested queries
        """
        try:
            if not self.api_key:
                return []
            
            params = {
                "q": query,
                "api_key": self.api_key,
                "engine": "google_autocomplete"
            }
            
            response = await self.client.get(self.base_url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            suggestions = []
            if "suggestions" in data:
                suggestions = [s.get("value", "") for s in data["suggestions"]]
            
            return suggestions
            
        except Exception as e:
            logger.error(f"Error getting search suggestions: {e}")
            return []
    
    def is_configured(self) -> bool:
        """Check if SerpAPI is properly configured"""
        return bool(self.api_key)
    
    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()

# Global instance
search_service = SearchService()