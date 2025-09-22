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
    <div className="flex-1 relative bg-white">
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
        className={isDragging ? 'bg-green-50' : ''}
      >
        <Controls className="bg-white border border-gray-300 rounded-lg shadow-lg" />
        <MiniMap className="bg-gray-100 border border-gray-300 rounded-lg" />
        <Background variant={BackgroundVariant.Dots} gap={12} size={1} color="#e5e7eb" />
        
        {nodes.length === 0 && !isDragging && (
          <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
            <div className="text-center">
              <div className="w-16 h-16 bg-green-500 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16l-4-4m0 0l4-4m-4 4h18" />
                </svg>
              </div>
              <p className="text-gray-500 text-lg font-medium">Drag & drop to get started</p>
            </div>
          </div>
        )}
        
        {isDragging && (
          <div className="absolute inset-0 bg-green-50 bg-opacity-50 flex items-center justify-center pointer-events-none">
            <div className="bg-green-500 text-white px-4 py-2 rounded-lg shadow-lg">
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