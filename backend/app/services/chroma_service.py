"""
ChromaDB Service - Handles vector storage and similarity search
"""
import chromadb
from chromadb.config import Settings
from typing import List, Dict, Any, Optional
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

class ChromaService:
    def __init__(self):
        self.client = None
        self.collection = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize ChromaDB client"""
        try:
            self.client = chromadb.HttpClient(
                host=settings.chroma_host,
                port=settings.chroma_port
            )
            
            # Create or get collection
            self.collection = self.client.get_or_create_collection(
                name="genai_documents",
                metadata={"description": "GenAI Stack document embeddings"}
            )
            
            logger.info("ChromaDB client initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing ChromaDB client: {e}")
            # Fallback to in-memory client for development
            try:
                self.client = chromadb.Client()
                self.collection = self.client.get_or_create_collection(
                    name="genai_documents"
                )
                logger.info("ChromaDB fallback client initialized")
            except Exception as fallback_error:
                logger.error(f"ChromaDB fallback failed: {fallback_error}")
    
    async def add_documents(
        self,
        documents: List[str],
        metadatas: Optional[List[Dict[str, Any]]] = None,
        ids: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Add documents to the vector store
        
        Args:
            documents: List of document texts
            metadatas: List of metadata dicts for each document
            ids: List of unique IDs for each document
            
        Returns:
            Dict with operation results
        """
        try:
            if not self.collection:
                raise Exception("ChromaDB collection not initialized")
            
            # Generate IDs if not provided
            if not ids:
                ids = [f"doc_{i}_{hash(doc) % 10000}" for i, doc in enumerate(documents)]
            
            # Prepare metadata
            if not metadatas:
                metadatas = [{} for _ in documents]
            
            # Add documents to collection
            self.collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            
            logger.info(f"Added {len(documents)} documents to ChromaDB")
            
            return {
                "success": True,
                "documents_added": len(documents),
                "ids": ids
            }
            
        except Exception as e:
            logger.error(f"Error adding documents to ChromaDB: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def search_documents(
        self,
        query: str,
        n_results: int = 5,
        similarity_threshold: float = 0.7,
        filter_metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Search for similar documents
        
        Args:
            query: Search query text
            n_results: Number of results to return
            similarity_threshold: Minimum similarity score
            filter_metadata: Metadata filters
            
        Returns:
            Dict with search results
        """
        try:
            if not self.collection:
                raise Exception("ChromaDB collection not initialized")
            
            # Perform similarity search
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results,
                where=filter_metadata
            )
            
            # Process results
            search_results = []
            if results['documents'] and results['documents'][0]:
                for i, (doc, metadata, distance) in enumerate(zip(
                    results['documents'][0],
                    results['metadatas'][0],
                    results['distances'][0]
                )):
                    # Convert distance to similarity score
                    similarity_score = 1 - distance
                    
                    if similarity_score >= similarity_threshold:
                        search_results.append({
                            "document": doc,
                            "metadata": metadata,
                            "similarity_score": similarity_score,
                            "rank": i + 1
                        })
            
            logger.info(f"Found {len(search_results)} relevant documents")
            
            return {
                "success": True,
                "query": query,
                "results": search_results,
                "total_found": len(search_results)
            }
            
        except Exception as e:
            logger.error(f"Error searching documents: {e}")
            return {
                "success": False,
                "error": str(e),
                "results": []
            }
    
    async def get_document_by_id(self, doc_id: str) -> Dict[str, Any]:
        """Get a specific document by ID"""
        try:
            if not self.collection:
                raise Exception("ChromaDB collection not initialized")
            
            results = self.collection.get(ids=[doc_id])
            
            if results['documents'] and results['documents'][0]:
                return {
                    "success": True,
                    "document": results['documents'][0],
                    "metadata": results['metadatas'][0] if results['metadatas'] else {}
                }
            else:
                return {
                    "success": False,
                    "error": "Document not found"
                }
                
        except Exception as e:
            logger.error(f"Error getting document by ID: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def delete_documents(self, doc_ids: List[str]) -> Dict[str, Any]:
        """Delete documents by IDs"""
        try:
            if not self.collection:
                raise Exception("ChromaDB collection not initialized")
            
            self.collection.delete(ids=doc_ids)
            
            logger.info(f"Deleted {len(doc_ids)} documents")
            
            return {
                "success": True,
                "deleted_count": len(doc_ids)
            }
            
        except Exception as e:
            logger.error(f"Error deleting documents: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def get_collection_stats(self) -> Dict[str, Any]:
        """Get collection statistics"""
        try:
            if not self.collection:
                raise Exception("ChromaDB collection not initialized")
            
            count = self.collection.count()
            
            return {
                "success": True,
                "total_documents": count,
                "collection_name": self.collection.name
            }
            
        except Exception as e:
            logger.error(f"Error getting collection stats: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def is_connected(self) -> bool:
        """Check if ChromaDB is connected"""
        try:
            if self.collection:
                self.collection.count()
                return True
            return False
        except Exception:
            return False

# Global instance
chroma_service = ChromaService()