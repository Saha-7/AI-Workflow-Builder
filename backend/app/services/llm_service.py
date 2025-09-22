"""
LLM Service - Handles interactions with OpenAI and Google Gemini
"""
import openai
import google.generativeai as genai
from typing import Dict, Any, Optional, List
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self):
        self.openai_client = None
        self.gemini_model = None
        self._initialize_clients()
    
    def _initialize_clients(self):
        """Initialize LLM clients"""
        try:
            if settings.openai_api_key:
                openai.api_key = settings.openai_api_key
                self.openai_client = openai
                logger.info("OpenAI client initialized")
            
            if settings.gemini_api_key:
                genai.configure(api_key=settings.gemini_api_key)
                self.gemini_model = genai.GenerativeModel('gemini-pro')
                logger.info("Gemini client initialized")
                
        except Exception as e:
            logger.error(f"Error initializing LLM clients: {e}")
    
    async def generate_response(
        self,
        prompt: str,
        model: str = "gpt-3.5-turbo",
        temperature: float = 0.7,
        max_tokens: int = 1000,
        context: Optional[str] = None,
        use_web_search: bool = False
    ) -> Dict[str, Any]:
        """
        Generate response using specified LLM
        
        Args:
            prompt: The input prompt
            model: LLM model to use (gpt-3.5-turbo, gpt-4, gemini-pro)
            temperature: Response randomness (0.0 to 1.0)
            max_tokens: Maximum tokens in response
            context: Additional context for the prompt
            use_web_search: Whether to include web search results
            
        Returns:
            Dict containing response and metadata
        """
        try:
            # Prepare the full prompt with context
            full_prompt = prompt
            if context:
                full_prompt = f"Context: {context}\n\nQuestion: {prompt}"
            
            if use_web_search:
                # TODO: Integrate web search results
                full_prompt += "\n\nPlease provide up-to-date information."
            
            # Route to appropriate LLM
            if model.startswith("gpt") and self.openai_client:
                return await self._generate_openai_response(
                    full_prompt, model, temperature, max_tokens
                )
            elif model == "gemini-pro" and self.gemini_model:
                return await self._generate_gemini_response(
                    full_prompt, temperature, max_tokens
                )
            else:
                raise ValueError(f"Unsupported model: {model}")
                
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return {
                "response": "Sorry, I encountered an error generating a response.",
                "error": str(e),
                "model": model
            }
    
    async def _generate_openai_response(
        self, prompt: str, model: str, temperature: float, max_tokens: int
    ) -> Dict[str, Any]:
        """Generate response using OpenAI"""
        try:
            response = await self.openai_client.ChatCompletion.acreate(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            return {
                "response": response.choices[0].message.content,
                "model": model,
                "tokens_used": response.usage.total_tokens,
                "provider": "openai"
            }
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            raise e
    
    async def _generate_gemini_response(
        self, prompt: str, temperature: float, max_tokens: int
    ) -> Dict[str, Any]:
        """Generate response using Google Gemini"""
        try:
            generation_config = genai.types.GenerationConfig(
                temperature=temperature,
                max_output_tokens=max_tokens
            )
            
            response = await self.gemini_model.generate_content_async(
                prompt,
                generation_config=generation_config
            )
            
            return {
                "response": response.text,
                "model": "gemini-pro",
                "provider": "gemini"
            }
        except Exception as e:
            logger.error(f"Gemini API error: {e}")
            raise e
    
    def get_available_models(self) -> List[str]:
        """Get list of available models"""
        models = []
        if self.openai_client:
            models.extend(["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo"])
        if self.gemini_model:
            models.append("gemini-pro")
        return models
    
    def validate_model(self, model: str) -> bool:
        """Validate if model is available"""
        return model in self.get_available_models()

# Global instance
llm_service = LLMService()