"""
Workflow Service - Orchestrates workflow execution
"""
from typing import Dict, Any, List, Optional
import logging
import asyncio
from datetime import datetime
import uuid

from app.services.llm_service import llm_service
from app.services.chroma_service import chroma_service
from app.services.search_service import search_service
from app.database.models import Workflow, Component, ChatSession, ChatMessage
from app.database.connection import get_db

logger = logging.getLogger(__name__)

class WorkflowService:
    def __init__(self):
        self.component_handlers = {
            "user_query": self._handle_user_query,
            "knowledge_base": self._handle_knowledge_base,
            "llm_engine": self._handle_llm_engine,
            "output": self._handle_output
        }
    
    async def execute_workflow(
        self,
        workflow_id: str,
        user_input: str,
        session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Execute a workflow with user input
        
        Args:
            workflow_id: ID of the workflow to execute
            user_input: User's input query
            session_id: Chat session ID
            
        Returns:
            Dict containing execution results
        """
        try:
            # Get workflow from database
            db = next(get_db())
            workflow = db.query(Workflow).filter(Workflow.id == workflow_id).first()
            
            if not workflow:
                return {
                    "success": False,
                    "error": "Workflow not found"
                }
            
            # Create or get chat session
            if not session_id:
                session_id = str(uuid.uuid4())
                chat_session = ChatSession(
                    id=session_id,
                    workflow_id=workflow_id,
                    created_at=datetime.utcnow()
                )
                db.add(chat_session)
                db.commit()
            
            # Parse workflow components
            components = self._parse_workflow_components(workflow.definition)
            
            # Execute workflow step by step
            execution_context = {
                "user_input": user_input,
                "session_id": session_id,
                "workflow_id": workflow_id,
                "intermediate_results": {},
                "final_result": None
            }
            
            for component in components:
                result = await self._execute_component(component, execution_context)
                execution_context["intermediate_results"][component["id"]] = result
                
                # If this is the output component, set final result
                if component["type"] == "output":
                    execution_context["final_result"] = result
            
            # Save chat message
            chat_message = ChatMessage(
                id=str(uuid.uuid4()),
                session_id=session_id,
                content=user_input,
                is_user=True,
                created_at=datetime.utcnow()
            )
            db.add(chat_message)
            
            response_message = ChatMessage(
                id=str(uuid.uuid4()),
                session_id=session_id,
                content=execution_context["final_result"].get("content", ""),
                is_user=False,
                created_at=datetime.utcnow()
            )
            db.add(response_message)
            db.commit()
            
            logger.info(f"Workflow {workflow_id} executed successfully")
            
            return {
                "success": True,
                "session_id": session_id,
                "result": execution_context["final_result"],
                "execution_context": execution_context
            }
            
        except Exception as e:
            logger.error(f"Error executing workflow: {e}")
            return {
                "success": False,
                "error": str(e)
            }
        finally:
            db.close()
    
    def _parse_workflow_components(self, workflow_definition: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Parse workflow definition to get ordered components"""
        # This would parse the React Flow nodes and edges to determine execution order
        # For now, return a simple ordered list
        components = []
        
        # Find user_query component (should be first)
        for node_id, node_data in workflow_definition.get("nodes", {}).items():
            if node_data.get("type") == "user_query":
                components.append({
                    "id": node_id,
                    "type": "user_query",
                    "config": node_data.get("data", {}).get("configuration", {})
                })
                break
        
        # Find knowledge_base component
        for node_id, node_data in workflow_definition.get("nodes", {}).items():
            if node_data.get("type") == "knowledge_base":
                components.append({
                    "id": node_id,
                    "type": "knowledge_base",
                    "config": node_data.get("data", {}).get("configuration", {})
                })
                break
        
        # Find llm_engine component
        for node_id, node_data in workflow_definition.get("nodes", {}).items():
            if node_data.get("type") == "llm_engine":
                components.append({
                    "id": node_id,
                    "type": "llm_engine",
                    "config": node_data.get("data", {}).get("configuration", {})
                })
                break
        
        # Find output component (should be last)
        for node_id, node_data in workflow_definition.get("nodes", {}).items():
            if node_data.get("type") == "output":
                components.append({
                    "id": node_id,
                    "type": "output",
                    "config": node_data.get("data", {}).get("configuration", {})
                })
                break
        
        return components
    
    async def _execute_component(
        self,
        component: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute a single workflow component"""
        component_type = component["type"]
        handler = self.component_handlers.get(component_type)
        
        if not handler:
            return {
                "success": False,
                "error": f"Unknown component type: {component_type}"
            }
        
        try:
            return await handler(component, context)
        except Exception as e:
            logger.error(f"Error executing component {component_type}: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def _handle_user_query(
        self,
        component: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Handle user query component"""
        return {
            "success": True,
            "content": context["user_input"],
            "type": "user_query"
        }
    
    async def _handle_knowledge_base(
        self,
        component: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Handle knowledge base component"""
        config = component["config"]
        user_input = context["user_input"]
        
        # Search for relevant documents
        search_result = await chroma_service.search_documents(
            query=user_input,
            n_results=config.get("max_results", 5),
            similarity_threshold=config.get("similarity_threshold", 0.7)
        )
        
        if search_result["success"]:
            # Combine search results into context
            context_text = "\n\n".join([
                f"Document {i+1}: {result['document']}"
                for i, result in enumerate(search_result["results"])
            ])
            
            return {
                "success": True,
                "content": context_text,
                "type": "knowledge_base",
                "search_results": search_result["results"]
            }
        else:
            return {
                "success": False,
                "error": "Knowledge base search failed",
                "content": ""
            }
    
    async def _handle_llm_engine(
        self,
        component: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Handle LLM engine component"""
        config = component["config"]
        user_input = context["user_input"]
        
        # Get knowledge base context if available
        knowledge_context = ""
        for comp_id, result in context["intermediate_results"].items():
            if result.get("type") == "knowledge_base" and result.get("success"):
                knowledge_context = result.get("content", "")
                break
        
        # Generate response using LLM
        llm_result = await llm_service.generate_response(
            prompt=user_input,
            model=config.get("model", "gpt-3.5-turbo"),
            temperature=config.get("temperature", 0.7),
            max_tokens=config.get("max_tokens", 1000),
            context=knowledge_context,
            use_web_search=config.get("use_web_search", False)
        )
        
        return {
            "success": True,
            "content": llm_result.get("response", ""),
            "type": "llm_engine",
            "model_used": llm_result.get("model", ""),
            "metadata": llm_result
        }
    
    async def _handle_output(
        self,
        component: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Handle output component"""
        config = component["config"]
        
        # Get LLM result
        llm_result = None
        for comp_id, result in context["intermediate_results"].items():
            if result.get("type") == "llm_engine" and result.get("success"):
                llm_result = result
                break
        
        if llm_result:
            output_format = config.get("response_format", "text")
            
            if output_format == "json":
                return {
                    "success": True,
                    "content": llm_result["content"],
                    "type": "output",
                    "format": "json"
                }
            else:
                return {
                    "success": True,
                    "content": llm_result["content"],
                    "type": "output",
                    "format": "text"
                }
        else:
            return {
                "success": False,
                "error": "No LLM result available for output",
                "content": ""
            }
    
    async def validate_workflow(self, workflow_definition: Dict[str, Any]) -> Dict[str, Any]:
        """Validate a workflow definition"""
        try:
            nodes = workflow_definition.get("nodes", {})
            edges = workflow_definition.get("edges", {})
            
            # Check for required components
            required_types = ["user_query", "llm_engine", "output"]
            found_types = set()
            
            for node_id, node_data in nodes.items():
                node_type = node_data.get("type")
                if node_type in required_types:
                    found_types.add(node_type)
            
            missing_types = set(required_types) - found_types
            
            if missing_types:
                return {
                    "valid": False,
                    "error": f"Missing required components: {', '.join(missing_types)}"
                }
            
            # Check for valid connections
            # This would validate that the workflow has proper connections
            
            return {
                "valid": True,
                "message": "Workflow is valid"
            }
            
        except Exception as e:
            return {
                "valid": False,
                "error": str(e)
            }

# Global instance
workflow_service = WorkflowService()