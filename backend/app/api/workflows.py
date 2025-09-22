"""
Workflow API endpoints
"""
from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.database.models import Workflow, Component
from app.services.workflow_service import workflow_service
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

class WorkflowCreate(BaseModel):
    name: str
    description: Optional[str] = None
    definition: Dict[str, Any]

class WorkflowUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    definition: Optional[Dict[str, Any]] = None

class WorkflowExecute(BaseModel):
    user_input: str
    session_id: Optional[str] = None

@router.post("/", response_model=Dict[str, Any])
async def create_workflow(
    workflow_data: WorkflowCreate,
    db: Session = Depends(get_db)
):
    """Create a new workflow"""
    try:
        # Validate workflow definition
        validation_result = await workflow_service.validate_workflow(workflow_data.definition)
        if not validation_result["valid"]:
            raise HTTPException(status_code=400, detail=validation_result["error"])
        
        # Create workflow in database
        workflow = Workflow(
            name=workflow_data.name,
            description=workflow_data.description,
            definition=workflow_data.definition
        )
        
        db.add(workflow)
        db.commit()
        db.refresh(workflow)
        
        logger.info(f"Created workflow: {workflow.id}")
        
        return {
            "success": True,
            "workflow_id": workflow.id,
            "message": "Workflow created successfully"
        }
        
    except Exception as e:
        logger.error(f"Error creating workflow: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[Dict[str, Any]])
async def list_workflows(db: Session = Depends(get_db)):
    """List all workflows"""
    try:
        workflows = db.query(Workflow).all()
        
        return [
            {
                "id": workflow.id,
                "name": workflow.name,
                "description": workflow.description,
                "created_at": workflow.created_at.isoformat(),
                "updated_at": workflow.updated_at.isoformat()
            }
            for workflow in workflows
        ]
        
    except Exception as e:
        logger.error(f"Error listing workflows: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{workflow_id}", response_model=Dict[str, Any])
async def get_workflow(workflow_id: str, db: Session = Depends(get_db)):
    """Get a specific workflow"""
    try:
        workflow = db.query(Workflow).filter(Workflow.id == workflow_id).first()
        
        if not workflow:
            raise HTTPException(status_code=404, detail="Workflow not found")
        
        return {
            "id": workflow.id,
            "name": workflow.name,
            "description": workflow.description,
            "definition": workflow.definition,
            "created_at": workflow.created_at.isoformat(),
            "updated_at": workflow.updated_at.isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting workflow: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{workflow_id}", response_model=Dict[str, Any])
async def update_workflow(
    workflow_id: str,
    workflow_data: WorkflowUpdate,
    db: Session = Depends(get_db)
):
    """Update a workflow"""
    try:
        workflow = db.query(Workflow).filter(Workflow.id == workflow_id).first()
        
        if not workflow:
            raise HTTPException(status_code=404, detail="Workflow not found")
        
        # Update fields
        if workflow_data.name is not None:
            workflow.name = workflow_data.name
        if workflow_data.description is not None:
            workflow.description = workflow_data.description
        if workflow_data.definition is not None:
            # Validate workflow definition
            validation_result = await workflow_service.validate_workflow(workflow_data.definition)
            if not validation_result["valid"]:
                raise HTTPException(status_code=400, detail=validation_result["error"])
            workflow.definition = workflow_data.definition
        
        db.commit()
        db.refresh(workflow)
        
        logger.info(f"Updated workflow: {workflow_id}")
        
        return {
            "success": True,
            "message": "Workflow updated successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating workflow: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{workflow_id}", response_model=Dict[str, Any])
async def delete_workflow(workflow_id: str, db: Session = Depends(get_db)):
    """Delete a workflow"""
    try:
        workflow = db.query(Workflow).filter(Workflow.id == workflow_id).first()
        
        if not workflow:
            raise HTTPException(status_code=404, detail="Workflow not found")
        
        db.delete(workflow)
        db.commit()
        
        logger.info(f"Deleted workflow: {workflow_id}")
        
        return {
            "success": True,
            "message": "Workflow deleted successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting workflow: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{workflow_id}/execute", response_model=Dict[str, Any])
async def execute_workflow(
    workflow_id: str,
    execution_data: WorkflowExecute,
    db: Session = Depends(get_db)
):
    """Execute a workflow"""
    try:
        result = await workflow_service.execute_workflow(
            workflow_id=workflow_id,
            user_input=execution_data.user_input,
            session_id=execution_data.session_id
        )
        
        if not result["success"]:
            raise HTTPException(status_code=400, detail=result["error"])
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error executing workflow: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/validate", response_model=Dict[str, Any])
async def validate_workflow_definition(definition: Dict[str, Any]):
    """Validate a workflow definition"""
    try:
        result = await workflow_service.validate_workflow(definition)
        return result
        
    except Exception as e:
        logger.error(f"Error validating workflow: {e}")
        raise HTTPException(status_code=500, detail=str(e))




