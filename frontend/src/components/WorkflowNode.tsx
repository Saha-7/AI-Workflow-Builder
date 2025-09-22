import React from 'react';
import { Handle, Position, NodeProps } from 'reactflow';
import { ComponentType } from '../types';
import { MessageSquare, Database, Brain, MessageCircle, Search } from 'lucide-react';

const iconMap = {
  user_query: MessageSquare,
  knowledge_base: Database,
  llm_engine: Brain,
  output: MessageCircle,
  web_search: Search,
};

const colorMap = {
  user_query: 'bg-blue-500',
  knowledge_base: 'bg-green-500',
  llm_engine: 'bg-purple-500',
  output: 'bg-orange-500',
  web_search: 'bg-indigo-500',
};

const WorkflowNode: React.FC<NodeProps> = ({ data, selected }) => {
  const { type, label, configuration } = data;
  const IconComponent = iconMap[type as ComponentType];
  const colorClass = colorMap[type as ComponentType];

  const renderNodeContent = () => {
    switch (type) {
      case 'user_query':
        return (
          <div className="w-80">
            <div className="flex items-center mb-3">
              <div className={`w-8 h-8 ${colorClass} rounded-lg flex items-center justify-center mr-3`}>
                <IconComponent className="w-4 h-4 text-white" />
              </div>
              <h3 className="text-sm font-semibold text-gray-900">User Query</h3>
            </div>
            <input
              type="text"
              placeholder="Write your query here"
              className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm"
              defaultValue={configuration?.placeholder || ''}
            />
            <Handle
              type="source"
              position={Position.Right}
              id="query"
              className="w-3 h-3 bg-blue-500"
              style={{ top: '50%', right: -6 }}
            />
          </div>
        );

      case 'knowledge_base':
        return (
          <div className="w-80">
            <div className="flex items-center mb-3">
              <div className={`w-8 h-8 ${colorClass} rounded-lg flex items-center justify-center mr-3`}>
                <IconComponent className="w-4 h-4 text-white" />
              </div>
              <h3 className="text-sm font-semibold text-gray-900">Knowledge Base</h3>
            </div>
            <div className="space-y-3">
              <div className="flex items-center">
                <input type="checkbox" className="mr-2" />
                <span className="text-sm text-gray-700">Let LLM search info in your File</span>
              </div>
              <div>
                <label className="block text-xs text-gray-600 mb-1">File for Knowledge Base</label>
                <button className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm text-left hover:bg-gray-50">
                  Upload File
                </button>
              </div>
              <div>
                <label className="block text-xs text-gray-600 mb-1">Embedding Model</label>
                <select className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm">
                  <option>text-embedding-3-large</option>
                </select>
              </div>
              <div>
                <label className="block text-xs text-gray-600 mb-1">API Key</label>
                <input
                  type="password"
                  placeholder="Enter API key"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm"
                />
              </div>
            </div>
            <Handle
              type="target"
              position={Position.Left}
              id="query"
              className="w-3 h-3 bg-blue-500"
              style={{ top: '30%', left: -6 }}
            />
            <Handle
              type="source"
              position={Position.Right}
              id="context"
              className="w-3 h-3 bg-green-500"
              style={{ top: '70%', right: -6 }}
            />
          </div>
        );

      case 'llm_engine':
        return (
          <div className="w-80">
            <div className="flex items-center mb-3">
              <div className={`w-8 h-8 ${colorClass} rounded-lg flex items-center justify-center mr-3`}>
                <IconComponent className="w-4 h-4 text-white" />
              </div>
              <h3 className="text-sm font-semibold text-gray-900">LLM (OpenAI)</h3>
            </div>
            <div className="space-y-3">
              <div>
                <label className="block text-xs text-gray-600 mb-1">Model</label>
                <select className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm">
                  <option>GPT-4o-Mini</option>
                  <option>GPT-4</option>
                  <option>GPT-3.5-turbo</option>
                </select>
              </div>
              <div>
                <label className="block text-xs text-gray-600 mb-1">API Key</label>
                <input
                  type="password"
                  placeholder="Enter API key"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm"
                />
              </div>
              <div>
                <label className="block text-xs text-gray-600 mb-1">Prompt</label>
                <textarea
                  placeholder="You are a helpful PDF assistant. Use web search if the PDF lacks context. CONTEXT: {context} User Query: {query}"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm h-20 resize-none"
                  defaultValue={configuration?.prompt || ''}
                />
              </div>
              <div>
                <label className="block text-xs text-gray-600 mb-1">Temperature: {configuration?.temperature || 0.75}</label>
                <input
                  type="range"
                  min="0"
                  max="1"
                  step="0.1"
                  className="w-full"
                  defaultValue={configuration?.temperature || 0.75}
                />
              </div>
              <div className="flex items-center">
                <input type="checkbox" className="mr-2" defaultChecked={configuration?.use_web_search} />
                <span className="text-sm text-gray-700">WebSearch Tool</span>
              </div>
              <div>
                <label className="block text-xs text-gray-600 mb-1">SERP API</label>
                <input
                  type="password"
                  placeholder="Enter SERP API key"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm"
                />
              </div>
            </div>
            <Handle
              type="target"
              position={Position.Left}
              id="context"
              className="w-3 h-3 bg-green-500"
              style={{ top: '50%', left: -6 }}
            />
            <Handle
              type="source"
              position={Position.Right}
              id="output"
              className="w-3 h-3 bg-purple-500"
              style={{ top: '50%', right: -6 }}
            />
          </div>
        );

      case 'output':
        return (
          <div className="w-80">
            <div className="flex items-center mb-3">
              <div className={`w-8 h-8 ${colorClass} rounded-lg flex items-center justify-center mr-3`}>
                <IconComponent className="w-4 h-4 text-white" />
              </div>
              <h3 className="text-sm font-semibold text-gray-900">Output</h3>
            </div>
            <div>
              <label className="block text-xs text-gray-600 mb-1">Output Text</label>
              <textarea
                placeholder="Output will appear here..."
                className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm h-20 resize-none"
                readOnly
              />
            </div>
            <Handle
              type="target"
              position={Position.Left}
              id="output"
              className="w-3 h-3 bg-purple-500"
              style={{ top: '50%', left: -6 }}
            />
          </div>
        );

      default:
        return (
          <div className="px-4 py-2 shadow-md rounded-md bg-white border-2 border-gray-200">
            <div className="flex items-center">
              <div className={`w-8 h-8 ${colorClass} rounded-lg flex items-center justify-center mr-3`}>
                <IconComponent className="w-4 h-4 text-white" />
              </div>
              <div className="flex-1">
                <div className="text-sm font-medium text-gray-900">{label}</div>
              </div>
            </div>
          </div>
        );
    }
  };

  return (
    <div className={`${selected ? 'ring-2 ring-blue-500' : ''}`}>
      {renderNodeContent()}
    </div>
  );
};

export default WorkflowNode;






