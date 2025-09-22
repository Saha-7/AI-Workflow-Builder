import openai
from app.core.config import settings
from typing import List, Dict, Any
import asyncio
import aiohttp

class EmbeddingService:
    def __init__(self):
        openai.api_key = settings.openai_api_key
        self.model = "text-embedding-3-small"

    async def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for a list of texts"""
        try:
            response = await openai.Embedding.acreate(
                model=self.model,
                input=texts
            )
            return [embedding["embedding"] for embedding in response["data"]]
        except Exception as e:
            print(f"Error generating embeddings: {e}")
            return []

    async def generate_single_embedding(self, text: str) -> List[float]:
        """Generate embedding for a single text"""
        embeddings = await self.generate_embeddings([text])
        return embeddings[0] if embeddings else []

    def chunk_text(self, text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
        """Split text into overlapping chunks"""
        if len(text) <= chunk_size:
            return [text]
        
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]
            
            # Try to break at sentence boundary
            if end < len(text):
                last_period = chunk.rfind('.')
                last_newline = chunk.rfind('\n')
                break_point = max(last_period, last_newline)
                
                if break_point > start + chunk_size // 2:  # Only break if it's not too short
                    chunk = chunk[:break_point + 1]
                    end = start + break_point + 1
            
            chunks.append(chunk.strip())
            start = end - overlap
            
            if start >= len(text):
                break
        
        return chunks

    async def process_document_for_embeddings(self, content: str, metadata: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Process a document and return chunks with embeddings"""
        chunks = self.chunk_text(content)
        embeddings = await self.generate_embeddings(chunks)
        
        processed_chunks = []
        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            processed_chunks.append({
                "text": chunk,
                "embedding": embedding,
                "metadata": {
                    **metadata,
                    "chunk_index": i,
                    "total_chunks": len(chunks)
                }
            })
        
        return processed_chunks






