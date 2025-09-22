"""
Document API endpoints
"""
from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.database.models import Document
from app.services.document_service import document_service
from app.services.chroma_service import chroma_service
import logging
import os
import uuid
from datetime import datetime

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/upload", response_model=Dict[str, Any])
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Upload and process a document"""
    try:
        # Save uploaded file
        file_id = str(uuid.uuid4())
        file_extension = os.path.splitext(file.filename)[1]
        file_path = f"uploads/{file_id}{file_extension}"
        
        os.makedirs("uploads", exist_ok=True)
        
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Process document
        result = await document_service.process_document(file_path)
        
        if not result["success"]:
            # Clean up file if processing failed
            os.remove(file_path)
            raise HTTPException(status_code=400, detail=result["error"])
        
        # Save document metadata to database
        document = Document(
            filename=file.filename,
            file_path=file_path,
            file_size=len(content),
            file_type=file_extension,
            content_hash=result["metadata"]["content_hash"],
            processed_at=datetime.utcnow()
        )
        
        db.add(document)
        db.commit()
        db.refresh(document)
        
        # Chunk document for vector storage
        chunks = await document_service.chunk_document(result["content"])
        
        # Add chunks to ChromaDB
        chunk_texts = [chunk["text"] for chunk in chunks]
        chunk_metadatas = [
            {
                **chunk,
                "document_id": str(document.id),
                "filename": file.filename
            }
            for chunk in chunks
        ]
        chunk_ids = [f"{document.id}_{chunk['chunk_index']}" for chunk in chunks]
        
        chroma_result = await chroma_service.add_documents(
            documents=chunk_texts,
            metadatas=chunk_metadatas,
            ids=chunk_ids
        )
        
        logger.info(f"Uploaded and processed document: {document.id}")
        
        return {
            "success": True,
            "document_id": document.id,
            "filename": file.filename,
            "file_size": len(content),
            "chunks_created": len(chunks),
            "chroma_success": chroma_result["success"],
            "message": "Document uploaded and processed successfully"
        }
        
    except Exception as e:
        logger.error(f"Error uploading document: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[Dict[str, Any]])
async def list_documents(db: Session = Depends(get_db)):
    """List all documents"""
    try:
        documents = db.query(Document).all()
        
        return [
            {
                "id": document.id,
                "filename": document.filename,
                "file_size": document.file_size,
                "file_type": document.file_type,
                "processed_at": document.processed_at.isoformat(),
                "content_hash": document.content_hash
            }
            for document in documents
        ]
        
    except Exception as e:
        logger.error(f"Error listing documents: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{document_id}", response_model=Dict[str, Any])
async def get_document(document_id: str, db: Session = Depends(get_db)):
    """Get a specific document"""
    try:
        document = db.query(Document).filter(Document.id == document_id).first()
        
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")
        
        return {
            "id": document.id,
            "filename": document.filename,
            "file_path": document.file_path,
            "file_size": document.file_size,
            "file_type": document.file_type,
            "processed_at": document.processed_at.isoformat(),
            "content_hash": document.content_hash
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting document: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{document_id}", response_model=Dict[str, Any])
async def delete_document(document_id: str, db: Session = Depends(get_db)):
    """Delete a document"""
    try:
        document = db.query(Document).filter(Document.id == document_id).first()
        
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")
        
        # Delete from ChromaDB
        # Find all chunk IDs for this document
        stats = await chroma_service.get_collection_stats()
        if stats["success"]:
            # This is a simplified approach - in production you'd want to track chunk IDs
            pass
        
        # Delete file
        if os.path.exists(document.file_path):
            os.remove(document.file_path)
        
        # Delete from database
        db.delete(document)
        db.commit()
        
        logger.info(f"Deleted document: {document_id}")
        
        return {
            "success": True,
            "message": "Document deleted successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting document: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/search", response_model=Dict[str, Any])
async def search_documents(
    query: str,
    n_results: int = 5,
    similarity_threshold: float = 0.7
):
    """Search documents using vector similarity"""
    try:
        result = await chroma_service.search_documents(
            query=query,
            n_results=n_results,
            similarity_threshold=similarity_threshold
        )
        
        return result
        
    except Exception as e:
        logger.error(f"Error searching documents: {e}")
        raise HTTPException(status_code=500, detail=str(e))