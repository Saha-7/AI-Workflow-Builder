import React, { useState } from 'react';
import { Plus, Edit3, ExternalLink, Code } from 'lucide-react';

interface Stack {
  id: string;
  name: string;
  description: string;
  type: 'chat' | 'content' | 'summarizer' | 'finder';
}

const MyStacks: React.FC = () => {
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [newStackName, setNewStackName] = useState('');
  const [newStackDescription, setNewStackDescription] = useState('');
  const [stacks, setStacks] = useState<Stack[]>([
    {
      id: '1',
      name: 'Chat With AI',
      description: 'Chat with a smart AI',
      type: 'chat'
    },
    {
      id: '2',
      name: 'Content Writer',
      description: 'Helps you write content',
      type: 'content'
    },
    {
      id: '3',
      name: 'Content Summarizer',
      description: 'Helps you summarize content',
      type: 'summarizer'
    },
    {
      id: '4',
      name: 'Information Finder',
      description: 'Helps you find relevant information',
      type: 'finder'
    }
  ]);

  const handleCreateStack = () => {
    if (newStackName.trim()) {
      const newStack: Stack = {
        id: Date.now().toString(),
        name: newStackName,
        description: newStackDescription,
        type: 'chat'
      };
      setStacks([...stacks, newStack]);
      setNewStackName('');
      setNewStackDescription('');
      setShowCreateModal(false);
      // Navigate to workflow builder
      window.location.href = `/workflow/${newStack.id}`;
    }
  };

  const handleEditStack = (stackId: string) => {
    window.location.href = `/workflow/${stackId}`;
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      {/* Header */}
      <div className="flex items-center justify-between p-6 border-b border-gray-700">
        <div className="flex items-center space-x-3">
          <div className="w-8 h-8 bg-green-500 rounded-full flex items-center justify-center">
            <span className="text-white font-bold text-sm">G</span>
          </div>
          <h1 className="text-2xl font-bold">GenAI Stack</h1>
        </div>
        <div className="flex items-center space-x-4">
          <div className="w-10 h-10 bg-purple-500 rounded-full flex items-center justify-center">
            <Code className="w-5 h-5 text-white" />
          </div>
          <button
            onClick={() => setShowCreateModal(true)}
            className="bg-green-500 hover:bg-green-600 text-white px-6 py-2 rounded-lg font-medium flex items-center space-x-2 transition-colors"
          >
            <Plus className="w-5 h-5" />
            <span>New Stack</span>
          </button>
        </div>
      </div>

      {/* Main Content */}
      <div className="p-6">
        <div className="bg-white rounded-lg p-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-8">My Stacks</h2>
          
          {/* Stacks Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {stacks.map((stack) => (
              <div key={stack.id} className="bg-white border border-gray-200 rounded-lg p-6 hover:shadow-lg transition-shadow">
                <div className="flex items-start justify-between mb-4">
                  <div className="flex-1">
                    <h3 className="text-lg font-semibold text-gray-900 mb-2">{stack.name}</h3>
                    <p className="text-gray-600 text-sm">{stack.description}</p>
                  </div>
                  <ExternalLink className="w-4 h-4 text-gray-400" />
                </div>
                <button
                  onClick={() => handleEditStack(stack.id)}
                  className="w-full bg-gray-100 hover:bg-gray-200 text-gray-700 py-2 px-4 rounded-lg font-medium transition-colors flex items-center justify-center space-x-2"
                >
                  <Edit3 className="w-4 h-4" />
                  <span>Edit Stack</span>
                </button>
              </div>
            ))}
            
            {/* Create New Stack Card */}
            <div className="bg-gray-50 border-2 border-dashed border-gray-300 rounded-lg p-6 flex flex-col items-center justify-center hover:border-green-400 transition-colors cursor-pointer"
                 onClick={() => setShowCreateModal(true)}>
              <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center mb-4">
                <Plus className="w-6 h-6 text-green-500" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">Create New Stack</h3>
              <p className="text-gray-600 text-sm text-center mb-4">
                Start building your generative AI apps with our essential tools and frameworks
              </p>
              <button className="bg-green-500 hover:bg-green-600 text-white px-6 py-2 rounded-lg font-medium transition-colors flex items-center space-x-2">
                <Plus className="w-4 h-4" />
                <span>New Stack</span>
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Create Stack Modal */}
      {showCreateModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md mx-4">
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-xl font-semibold text-gray-900">Create New Stack</h3>
              <button
                onClick={() => setShowCreateModal(false)}
                className="text-gray-400 hover:text-gray-600"
              >
                <span className="text-2xl">&times;</span>
              </button>
            </div>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Name</label>
                <input
                  type="text"
                  value={newStackName}
                  onChange={(e) => setNewStackName(e.target.value)}
                  placeholder="Enter stack name"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Description</label>
                <textarea
                  value={newStackDescription}
                  onChange={(e) => setNewStackDescription(e.target.value)}
                  placeholder="Enter stack description"
                  rows={3}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
                />
              </div>
            </div>
            
            <div className="flex justify-end space-x-3 mt-6">
              <button
                onClick={() => setShowCreateModal(false)}
                className="px-4 py-2 text-gray-600 hover:text-gray-800 transition-colors"
              >
                Cancel
              </button>
              <button
                onClick={handleCreateStack}
                className="bg-green-500 hover:bg-green-600 text-white px-6 py-2 rounded-lg font-medium transition-colors"
              >
                Create
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default MyStacks;

