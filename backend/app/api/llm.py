"""
LLM API endpoints
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any, Optional
from pydantic import BaseModel
from app.services.llm_service import llm_service
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

class LLMRequest(BaseModel):
    prompt: str
    model: str = "gpt-3.5-turbo"
    temperature: float = 0.7
    max_tokens: int = 1000
    context: Optional[str] = None
    use_web_search: bool = False

@router.post("/generate", response_model=Dict[str, Any])
async def generate_response(request: LLMRequest):
    """Generate response using LLM"""
    try:
        result = await llm_service.generate_response(
            prompt=request.prompt,
            model=request.model,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            context=request.context,
            use_web_search=request.use_web_search
        )
        
        return result
        
    except Exception as e:
        logger.error(f"Error generating LLM response: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/models", response_model=Dict[str, Any])
async def get_available_models():
    """Get list of available LLM models"""
    try:
        models = llm_service.get_available_models()
        
        return {
            "success": True,
            "models": models,
            "total_count": len(models)
        }
        
    except Exception as e:
        logger.error(f"Error getting available models: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/validate-model", response_model=Dict[str, Any])
async def validate_model(model: str):
    """Validate if a model is available"""
    try:
        is_valid = llm_service.validate_model(model)
        
        return {
            "success": True,
            "model": model,
            "is_valid": is_valid
        }
        
    except Exception as e:
        logger.error(f"Error validating model: {e}")
        raise HTTPException(status_code=500, detail=str(e))