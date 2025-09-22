"""
Chat API endpoints
"""
from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.database.models import ChatSession, ChatMessage, Workflow
from app.services.workflow_service import workflow_service
import logging
import uuid
from datetime import datetime

logger = logging.getLogger(__name__)

router = APIRouter()

class ChatMessageCreate(BaseModel):
    content: str
    workflow_id: str

class ChatSessionResponse(BaseModel):
    id: str
    workflow_id: str
    created_at: str
    message_count: int

class ChatMessageResponse(BaseModel):
    id: str
    session_id: str
    content: str
    is_user: bool
    created_at: str

@router.post("/sessions", response_model=Dict[str, Any])
async def create_chat_session(
    workflow_id: str,
    db: Session = Depends(get_db)
):
    """Create a new chat session"""
    try:
        # Verify workflow exists
        workflow = db.query(Workflow).filter(Workflow.id == workflow_id).first()
        if not workflow:
            raise HTTPException(status_code=404, detail="Workflow not found")
        
        # Create new chat session
        session_id = str(uuid.uuid4())
        chat_session = ChatSession(
            id=session_id,
            workflow_id=workflow_id,
            created_at=datetime.utcnow()
        )
        
        db.add(chat_session)
        db.commit()
        db.refresh(chat_session)
        
        logger.info(f"Created chat session: {session_id}")
        
        return {
            "success": True,
            "session_id": session_id,
            "workflow_id": workflow_id,
            "created_at": chat_session.created_at.isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating chat session: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/sessions", response_model=List[Dict[str, Any]])
async def list_chat_sessions(db: Session = Depends(get_db)):
    """List all chat sessions"""
    try:
        sessions = db.query(ChatSession).all()
        
        result = []
        for session in sessions:
            message_count = db.query(ChatMessage).filter(
                ChatMessage.session_id == session.id
            ).count()
            
            result.append({
                "id": session.id,
                "workflow_id": session.workflow_id,
                "created_at": session.created_at.isoformat(),
                "message_count": message_count
            })
        
        return result
        
    except Exception as e:
        logger.error(f"Error listing chat sessions: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/sessions/{session_id}", response_model=Dict[str, Any])
async def get_chat_session(session_id: str, db: Session = Depends(get_db)):
    """Get a specific chat session with messages"""
    try:
        session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
        
        if not session:
            raise HTTPException(status_code=404, detail="Chat session not found")
        
        # Get messages for this session
        messages = db.query(ChatMessage).filter(
            ChatMessage.session_id == session_id
        ).order_by(ChatMessage.created_at).all()
        
        message_list = [
            {
                "id": msg.id,
                "content": msg.content,
                "is_user": msg.is_user,
                "created_at": msg.created_at.isoformat()
            }
            for msg in messages
        ]
        
        return {
            "id": session.id,
            "workflow_id": session.workflow_id,
            "created_at": session.created_at.isoformat(),
            "messages": message_list,
            "message_count": len(message_list)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting chat session: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/sessions/{session_id}/messages", response_model=Dict[str, Any])
async def send_message(
    session_id: str,
    message_data: ChatMessageCreate,
    db: Session = Depends(get_db)
):
    """Send a message in a chat session"""
    try:
        # Verify session exists
        session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
        if not session:
            raise HTTPException(status_code=404, detail="Chat session not found")
        
        # Save user message
        user_message = ChatMessage(
            id=str(uuid.uuid4()),
            session_id=session_id,
            content=message_data.content,
            is_user=True,
            created_at=datetime.utcnow()
        )
        
        db.add(user_message)
        db.commit()
        
        # Execute workflow to get response
        workflow_result = await workflow_service.execute_workflow(
            workflow_id=message_data.workflow_id,
            user_input=message_data.content,
            session_id=session_id
        )
        
        if not workflow_result["success"]:
            # Save error message
            error_message = ChatMessage(
                id=str(uuid.uuid4()),
                session_id=session_id,
                content=f"Error: {workflow_result['error']}",
                is_user=False,
                created_at=datetime.utcnow()
            )
            db.add(error_message)
            db.commit()
            
            return {
                "success": False,
                "error": workflow_result["error"],
                "user_message_id": user_message.id,
                "error_message_id": error_message.id
            }
        
        # Get the response from workflow execution
        response_content = workflow_result.get("result", {}).get("content", "No response generated")
        
        # Save bot response
        bot_message = ChatMessage(
            id=str(uuid.uuid4()),
            session_id=session_id,
            content=response_content,
            is_user=False,
            created_at=datetime.utcnow()
        )
        
        db.add(bot_message)
        db.commit()
        
        logger.info(f"Processed message in session: {session_id}")
        
        return {
            "success": True,
            "user_message_id": user_message.id,
            "bot_message_id": bot_message.id,
            "response": response_content,
            "execution_context": workflow_result.get("execution_context", {})
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error sending message: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/sessions/{session_id}/messages", response_model=List[Dict[str, Any]])
async def get_session_messages(session_id: str, db: Session = Depends(get_db)):
    """Get all messages for a chat session"""
    try:
        # Verify session exists
        session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
        if not session:
            raise HTTPException(status_code=404, detail="Chat session not found")
        
        messages = db.query(ChatMessage).filter(
            ChatMessage.session_id == session_id
        ).order_by(ChatMessage.created_at).all()
        
        return [
            {
                "id": msg.id,
                "content": msg.content,
                "is_user": msg.is_user,
                "created_at": msg.created_at.isoformat()
            }
            for msg in messages
        ]
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting session messages: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/sessions/{session_id}", response_model=Dict[str, Any])
async def delete_chat_session(session_id: str, db: Session = Depends(get_db)):
    """Delete a chat session and all its messages"""
    try:
        session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
        
        if not session:
            raise HTTPException(status_code=404, detail="Chat session not found")
        
        # Delete all messages first
        db.query(ChatMessage).filter(ChatMessage.session_id == session_id).delete()
        
        # Delete session
        db.delete(session)
        db.commit()
        
        logger.info(f"Deleted chat session: {session_id}")
        
        return {
            "success": True,
            "message": "Chat session deleted successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting chat session: {e}")
        raise HTTPException(status_code=500, detail=str(e))




