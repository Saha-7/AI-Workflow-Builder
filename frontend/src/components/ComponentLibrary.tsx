import React from 'react';
import { ComponentLibraryItem } from '../types';
import { 
  MessageSquare, 
  Database, 
  Brain, 
  MessageCircle,
  Upload,
  Search,
  Settings
} from 'lucide-react';

const componentLibrary: ComponentLibraryItem[] = [
  {
    type: 'user_query',
    label: 'User Query',
    description: 'Accepts user input and queries',
    icon: 'MessageSquare',
    color: 'bg-blue-500',
  },
  {
    type: 'knowledge_base',
    label: 'Knowledge Base',
    description: 'Processes and searches documents',
    icon: 'Database',
    color: 'bg-green-500',
  },
  {
    type: 'llm_engine',
    label: 'LLM Engine',
    description: 'Generates responses using AI models',
    icon: 'Brain',
    color: 'bg-purple-500',
  },
  {
    type: 'output',
    label: 'Output',
    description: 'Displays the final response',
    icon: 'MessageCircle',
    color: 'bg-orange-500',
  },
];

const iconMap = {
  MessageSquare,
  Database,
  Brain,
  MessageCircle,
  Upload,
  Search,
  Settings,
};

interface ComponentLibraryProps {
  onDragStart: (event: React.DragEvent, component: ComponentLibraryItem) => void;
}

const ComponentLibrary: React.FC<ComponentLibraryProps> = ({ onDragStart }) => {
  return (
    <div className="w-64 bg-white border-r border-gray-200 p-4">
      <h2 className="text-lg font-semibold text-gray-900 mb-4">Components</h2>
      <div className="space-y-2">
        {componentLibrary.map((component) => {
          const IconComponent = iconMap[component.icon as keyof typeof iconMap];
          
          return (
            <div
              key={component.type}
              draggable
              onDragStart={(e) => onDragStart(e, component)}
              className="flex items-center p-3 bg-gray-50 rounded-lg cursor-move hover:bg-gray-100 transition-colors"
            >
              <div className={`w-8 h-8 ${component.color} rounded-lg flex items-center justify-center mr-3`}>
                <IconComponent className="w-4 h-4 text-white" />
              </div>
              <div className="flex-1">
                <h3 className="font-medium text-gray-900">{component.label}</h3>
                <p className="text-sm text-gray-500">{component.description}</p>
              </div>
            </div>
          );
        })}
      </div>
      
      <div className="mt-6">
        <h3 className="text-sm font-medium text-gray-700 mb-2">Quick Actions</h3>
        <div className="space-y-1">
          <button className="w-full text-left px-3 py-2 text-sm text-gray-600 hover:bg-gray-100 rounded">
            <Upload className="w-4 h-4 inline mr-2" />
            Upload Document
          </button>
          <button className="w-full text-left px-3 py-2 text-sm text-gray-600 hover:bg-gray-100 rounded">
            <Search className="w-4 h-4 inline mr-2" />
            Search Workflows
          </button>
          <button className="w-full text-left px-3 py-2 text-sm text-gray-600 hover:bg-gray-100 rounded">
            <Settings className="w-4 h-4 inline mr-2" />
            Settings
          </button>
        </div>
      </div>
    </div>
  );
};

export default ComponentLibrary;
