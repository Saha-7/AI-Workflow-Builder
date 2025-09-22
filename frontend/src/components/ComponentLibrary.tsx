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
    type: 'llm_engine',
    label: 'LLM (OpenAI)',
    description: 'Generates responses using AI models',
    icon: 'Brain',
    color: 'bg-purple-500',
  },
  {
    type: 'knowledge_base',
    label: 'Knowledge Base',
    description: 'Processes and searches documents',
    icon: 'Database',
    color: 'bg-green-500',
  },
  {
    type: 'output',
    label: 'Output',
    description: 'Displays the final response',
    icon: 'MessageCircle',
    color: 'bg-orange-500',
  },
  {
    type: 'web_search',
    label: 'Web Search',
    description: 'Searches the web for information',
    icon: 'Search',
    color: 'bg-indigo-500',
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
    <div className="w-64 bg-gray-800 border-r border-gray-700 p-4">
      <div className="mb-6">
        <h2 className="text-lg font-semibold text-white mb-2">Chat With AI</h2>
        <h3 className="text-sm font-medium text-gray-400 mb-4">Components</h3>
      </div>
      
      <div className="space-y-2">
        {componentLibrary.map((component) => {
          const IconComponent = iconMap[component.icon as keyof typeof iconMap];
          
          return (
            <div
              key={component.type}
              draggable
              onDragStart={(e) => onDragStart(e, component)}
              className="flex items-center p-3 bg-gray-700 rounded-lg cursor-move hover:bg-gray-600 transition-colors"
            >
              <div className={`w-8 h-8 ${component.color} rounded-lg flex items-center justify-center mr-3`}>
                <IconComponent className="w-4 h-4 text-white" />
              </div>
              <div className="flex-1">
                <h3 className="font-medium text-white">{component.label}</h3>
                <p className="text-sm text-gray-400">{component.description}</p>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default ComponentLibrary;






