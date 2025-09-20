import React, { useCallback, useState } from 'react';
import ReactFlow, {
  Node,
  Edge,
  Connection,
  Controls,
  Background,
  MiniMap,
  NodeTypes,
  BackgroundVariant,
} from 'reactflow';
import 'reactflow/dist/style.css';
import { ComponentType, ComponentConfiguration } from '../types';
import WorkflowNode from './WorkflowNode';

const nodeTypes: NodeTypes = {
  workflowNode: WorkflowNode,
};


interface WorkflowCanvasProps {
  nodes: Node[];
  edges: Edge[];
  onNodesChange: (changes: any) => void;
  onEdgesChange: (changes: any) => void;
  onConnect: (connection: Connection) => void;
  onNodeClick: (nodeId: string) => void;
  selectedNodeId: string | null;
}

const WorkflowCanvas: React.FC<WorkflowCanvasProps> = ({
  nodes,
  edges,
  onNodesChange,
  onEdgesChange,
  onConnect,
  onNodeClick,
  selectedNodeId,
}) => {
  const [isDragging, setIsDragging] = useState(false);

  const handleDragOver = useCallback((event: React.DragEvent) => {
    event.preventDefault();
    setIsDragging(true);
  }, []);

  const handleDragLeave = useCallback((event: React.DragEvent) => {
    event.preventDefault();
    setIsDragging(false);
  }, []);

  const handleDrop = useCallback((event: React.DragEvent) => {
    event.preventDefault();
    setIsDragging(false);
    
    const componentType = event.dataTransfer.getData('application/reactflow');
    if (!componentType) return;

    const rect = event.currentTarget.getBoundingClientRect();
    const position = {
      x: event.clientX - rect.left,
      y: event.clientY - rect.top,
    };

    // Create new node
    const newNode: Node = {
      id: `${componentType}-${Date.now()}`,
      type: 'workflowNode',
      position,
      data: {
        type: componentType as ComponentType,
        configuration: getDefaultConfiguration(componentType as ComponentType),
        label: getComponentLabel(componentType as ComponentType),
        description: getComponentDescription(componentType as ComponentType),
      },
    };

    onNodesChange([{ type: 'add', item: newNode }]);
  }, [onNodesChange]);

  return (
    <div className="flex-1 relative">
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onConnect={onConnect}
        onNodeClick={(event, node) => onNodeClick(node.id)}
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        nodeTypes={nodeTypes}
        fitView
        className={isDragging ? 'bg-blue-50' : ''}
      >
        <Controls />
        <MiniMap />
        <Background variant={BackgroundVariant.Dots} gap={12} size={1} />
        
        {isDragging && (
          <div className="absolute inset-0 bg-blue-50 bg-opacity-50 flex items-center justify-center pointer-events-none">
            <div className="bg-blue-500 text-white px-4 py-2 rounded-lg shadow-lg">
              Drop component here
            </div>
          </div>
        )}
      </ReactFlow>
    </div>
  );
};

function getDefaultConfiguration(type: ComponentType): ComponentConfiguration {
  switch (type) {
    case 'user_query':
      return {
        placeholder: 'Enter your question...',
      };
    case 'knowledge_base':
      return {
        max_results: 5,
        similarity_threshold: 0.7,
      };
    case 'llm_engine':
      return {
        model: 'gpt-3.5-turbo',
        temperature: 0.7,
        max_tokens: 1000,
        prompt: 'You are a helpful AI assistant.',
        use_web_search: false,
      };
    case 'output':
      return {
        response_format: 'text',
      };
    default:
      return {};
  }
}

function getComponentLabel(type: ComponentType): string {
  switch (type) {
    case 'user_query':
      return 'User Query';
    case 'knowledge_base':
      return 'Knowledge Base';
    case 'llm_engine':
      return 'LLM Engine';
    case 'output':
      return 'Output';
    default:
      return 'Unknown';
  }
}

function getComponentDescription(type: ComponentType): string {
  switch (type) {
    case 'user_query':
      return 'Accepts user input and queries';
    case 'knowledge_base':
      return 'Processes and searches documents';
    case 'llm_engine':
      return 'Generates responses using AI models';
    case 'output':
      return 'Displays the final response';
    default:
      return 'Unknown component';
  }
}

export default WorkflowCanvas;