import React from 'react';
import { ComponentType, ComponentConfiguration } from '../types';
import { X, Save, TestTube, Settings } from 'lucide-react';

interface ComponentConfigPanelProps {
  nodeId: string | null;
  componentType: ComponentType | null;
  configuration: ComponentConfiguration;
  onConfigurationChange: (config: ComponentConfiguration) => void;
  onClose: () => void;
  onSave: () => void;
  onTest: () => void;
}

const ComponentConfigPanel: React.FC<ComponentConfigPanelProps> = ({
  nodeId,
  componentType,
  configuration,
  onConfigurationChange,
  onClose,
  onSave,
  onTest,
}) => {
  if (!nodeId || !componentType) {
    return (
      <div className="w-80 bg-white border-l border-gray-200 p-4">
        <div className="text-center text-gray-500">
          <Settings className="w-12 h-12 mx-auto mb-4 text-gray-300" />
          <p>Select a component to configure</p>
        </div>
      </div>
    );
  }

  const renderConfigurationFields = () => {
    switch (componentType) {
      case 'user_query':
        return (
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Placeholder Text
              </label>
              <input
                type="text"
                value={configuration.placeholder || ''}
                onChange={(e) => onConfigurationChange({
                  ...configuration,
                  placeholder: e.target.value
                })}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Enter placeholder text..."
              />
            </div>
          </div>
        );

      case 'knowledge_base':
        return (
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Max Results
              </label>
              <input
                type="number"
                value={configuration.max_results || 5}
                onChange={(e) => onConfigurationChange({
                  ...configuration,
                  max_results: parseInt(e.target.value) || 5
                })}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                min="1"
                max="20"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Similarity Threshold
              </label>
              <input
                type="range"
                value={configuration.similarity_threshold || 0.7}
                onChange={(e) => onConfigurationChange({
                  ...configuration,
                  similarity_threshold: parseFloat(e.target.value)
                })}
                className="w-full"
                min="0"
                max="1"
                step="0.1"
              />
              <div className="text-sm text-gray-500">
                {((configuration.similarity_threshold || 0.7) * 100).toFixed(0)}%
              </div>
            </div>
          </div>
        );

      case 'llm_engine':
        return (
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Model
              </label>
              <select
                value={configuration.model || 'gpt-3.5-turbo'}
                onChange={(e) => onConfigurationChange({
                  ...configuration,
                  model: e.target.value
                })}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="gpt-3.5-turbo">GPT-3.5 Turbo</option>
                <option value="gpt-4">GPT-4</option>
                <option value="gpt-4-turbo">GPT-4 Turbo</option>
                <option value="gemini-pro">Gemini Pro</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Temperature
              </label>
              <input
                type="range"
                value={configuration.temperature || 0.7}
                onChange={(e) => onConfigurationChange({
                  ...configuration,
                  temperature: parseFloat(e.target.value)
                })}
                className="w-full"
                min="0"
                max="2"
                step="0.1"
              />
              <div className="text-sm text-gray-500">
                {configuration.temperature || 0.7}
              </div>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Max Tokens
              </label>
              <input
                type="number"
                value={configuration.max_tokens || 1000}
                onChange={(e) => onConfigurationChange({
                  ...configuration,
                  max_tokens: parseInt(e.target.value) || 1000
                })}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                min="100"
                max="4000"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                System Prompt
              </label>
              <textarea
                value={configuration.prompt || ''}
                onChange={(e) => onConfigurationChange({
                  ...configuration,
                  prompt: e.target.value
                })}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                rows={3}
                placeholder="Enter system prompt..."
              />
            </div>
            <div className="flex items-center">
              <input
                type="checkbox"
                id="use_web_search"
                checked={configuration.use_web_search || false}
                onChange={(e) => onConfigurationChange({
                  ...configuration,
                  use_web_search: e.target.checked
                })}
                className="mr-2"
              />
              <label htmlFor="use_web_search" className="text-sm font-medium text-gray-700">
                Enable Web Search
              </label>
            </div>
          </div>
        );

      case 'output':
        return (
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Response Format
              </label>
              <select
                value={configuration.response_format || 'text'}
                onChange={(e) => onConfigurationChange({
                  ...configuration,
                  response_format: e.target.value as 'text' | 'markdown' | 'json'
                })}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="text">Plain Text</option>
                <option value="markdown">Markdown</option>
                <option value="json">JSON</option>
              </select>
            </div>
          </div>
        );

      default:
        return (
          <div className="text-center text-gray-500">
            <p>No configuration options available</p>
          </div>
        );
    }
  };

  return (
    <div className="w-80 bg-white border-l border-gray-200 p-4">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-gray-900">Configuration</h3>
        <button
          onClick={onClose}
          className="text-gray-400 hover:text-gray-600"
        >
          <X className="w-5 h-5" />
        </button>
      </div>
      
      <div className="mb-4">
        <div className="text-sm text-gray-600 mb-2">Component: {nodeId}</div>
        <div className="text-sm text-gray-500">{componentType}</div>
      </div>

      <div className="mb-6">
        {renderConfigurationFields()}
      </div>

      <div className="flex space-x-2">
        <button
          onClick={onSave}
          className="flex-1 bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 flex items-center justify-center"
        >
          <Save className="w-4 h-4 mr-2" />
          Save
        </button>
        <button
          onClick={onTest}
          className="flex-1 bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700 flex items-center justify-center"
        >
          <TestTube className="w-4 h-4 mr-2" />
          Test
        </button>
      </div>
    </div>
  );
};

export default ComponentConfigPanel;
