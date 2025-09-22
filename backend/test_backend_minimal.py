"""
Minimal FastAPI test server to verify backend functionality
"""
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import os
from typing import Dict, Any, Optional
import json

app = FastAPI(
    title="GenAI Stack API - Test Mode",
    description="Minimal test version without heavy dependencies",
    version="1.0.0-test"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": f"Internal server error: {str(exc)}"}
    )

@app.get("/")
async def root():
    return {
        "message": "GenAI Stack API is running in TEST MODE!",
        "version": "1.0.0-test",
        "docs": "/docs",
        "status": "healthy"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "mode": "test",
        "database": "not_connected",
        "chromadb": "not_connected"
    }

@app.get("/api/workflows/")
async def list_workflows():
    """List workflows - test endpoint"""
    return {
        "success": True,
        "workflows": [
            {
                "id": "test-workflow-1",
                "name": "Test Workflow",
                "description": "This is a test workflow",
                "created_at": "2024-01-01T00:00:00Z"
            }
        ]
    }

@app.post("/api/workflows/")
async def create_workflow(workflow_data: Dict[str, Any]):
    """Create workflow - test endpoint"""
    return {
        "success": True,
        "workflow_id": "test-workflow-" + str(len(workflow_data)),
        "message": "Test workflow created successfully"
    }

@app.post("/api/documents/upload")
async def upload_document(file: UploadFile = File(...)):
    """Test file upload endpoint"""
    try:
        # Read file content
        content = await file.read()
        
        return {
            "success": True,
            "message": f"File '{file.filename}' uploaded successfully",
            "file_size": len(content),
            "content_type": file.content_type,
            "filename": file.filename
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@app.get("/api/documents/")
async def list_documents():
    """List documents - test endpoint"""
    return {
        "success": True,
        "documents": [
            {
                "id": "test-doc-1",
                "filename": "test.pdf",
                "size": 1024,
                "uploaded_at": "2024-01-01T00:00:00Z"
            }
        ]
    }

@app.post("/api/llm/generate")
async def generate_text(request: Dict[str, Any]):
    """Test LLM endpoint"""
    return {
        "success": True,
        "response": f"Test response for prompt: {request.get('prompt', 'No prompt provided')}"
    }

@app.post("/api/search/web")
async def web_search(request: Dict[str, Any]):
    """Test search endpoint"""
    return {
        "success": True,
        "results": [
            {
                "title": f"Test result for: {request.get('query', 'No query')}",
                "url": "https://example.com",
                "snippet": "This is a test search result"
            }
        ]
    }

@app.post("/api/chat/sessions")
async def create_chat_session(session_data: Dict[str, Any]):
    """Test chat session creation"""
    return {
        "success": True,
        "session_id": "test-session-123",
        "title": session_data.get("title", "Test Chat Session")
    }

@app.get("/api/chat/sessions")
async def list_chat_sessions():
    """Test chat sessions list"""
    return {
        "success": True,
        "sessions": [
            {
                "id": "test-session-123",
                "workflow_id": "test-workflow-1",
                "title": "Test Chat Session",
                "created_at": "2024-01-01T00:00:00Z"
            }
        ]
    }

if __name__ == "__main__":
    print("🚀 Starting GenAI Stack API in TEST MODE...")
    print("📝 This is a minimal version for testing basic functionality")
    print("🌐 API will be available at: http://localhost:8000")
    print("📖 API docs will be available at: http://localhost:8000/docs")
    
    uvicorn.run(
        "test_backend_minimal:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )




