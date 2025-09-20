import React from 'react';
import { Handle, Position, NodeProps } from 'reactflow';
import { ComponentType } from '../types';
import { MessageSquare, Database, Brain, MessageCircle } from 'lucide-react';

const iconMap = {
  user_query: MessageSquare,
  knowledge_base: Database,
  llm_engine: Brain,
  output: MessageCircle,
};

const colorMap = {
  user_query: 'bg-blue-500',
  knowledge_base: 'bg-green-500',
  llm_engine: 'bg-purple-500',
  output: 'bg-orange-500',
};

const WorkflowNode: React.FC<NodeProps> = ({ data, selected }) => {
  const { type, label, description } = data;
  const IconComponent = iconMap[type as ComponentType];
  const colorClass = colorMap[type as ComponentType];

  return (
    <div className={`px-4 py-2 shadow-md rounded-md bg-white border-2 ${
      selected ? 'border-blue-500' : 'border-gray-200'
    }`}>
      <Handle
        type="target"
        position={Position.Top}
        className="w-3 h-3 bg-gray-400"
      />
      
      <div className="flex items-center">
        <div className={`w-8 h-8 ${colorClass} rounded-lg flex items-center justify-center mr-3`}>
          <IconComponent className="w-4 h-4 text-white" />
        </div>
        <div className="flex-1">
          <div className="text-sm font-medium text-gray-900">{label}</div>
          <div className="text-xs text-gray-500">{description}</div>
        </div>
      </div>
      
      <Handle
        type="source"
        position={Position.Bottom}
        className="w-3 h-3 bg-gray-400"
      />
    </div>
  );
};

export default WorkflowNode;
