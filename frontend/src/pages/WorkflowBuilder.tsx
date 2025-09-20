import React, { useState, useCallback, useMemo } from 'react';
import { addEdge, Connection, useNodesState, useEdgesState } from 'reactflow';
import { ComponentConfiguration, ComponentLibraryItem } from '../types';
import ComponentLibrary from '../components/ComponentLibrary';
import WorkflowCanvas from '../components/WorkflowCanvas';
import ComponentConfigPanel from '../components/ComponentConfigPanel';
import ChatInterface from '../components/ChatInterface';
import { Play, Save, MessageSquare, X } from 'lucide-react';
import toast from 'react-hot-toast';

const WorkflowBuilder: React.FC = () => {
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const [selectedNodeId, setSelectedNodeId] = useState<string | null>(null);
  const [isExecuting, setIsExecuting] = useState(false);
  const [isChatOpen, setIsChatOpen] = useState(false);
  const [executionResult, setExecutionResult] = useState<any>(null);

  const selectedNode = useMemo(() => {
    return nodes.find(node => node.id === selectedNodeId);
  }, [nodes, selectedNodeId]);

  const handleDragStart = useCallback((event: React.DragEvent, component: ComponentLibraryItem) => {
    event.dataTransfer.setData('application/reactflow', component.type);
    event.dataTransfer.effectAllowed = 'move';
  }, []);

  const handleConnect = useCallback((params: Connection) => {
    const newEdge = {
      id: `edge-${params.source}-${params.target}`,
      source: params.source!,
      target: params.target!,
      sourceHandle: params.sourceHandle,
      targetHandle: params.targetHandle,
    };
    setEdges((eds) => addEdge(newEdge, eds));
  }, [setEdges]);

  const handleNodeClick = useCallback((nodeId: string) => {
    setSelectedNodeId(nodeId);
  }, []);

  const handleConfigurationChange = useCallback((config: ComponentConfiguration) => {
    if (!selectedNodeId) return;
    
    setNodes((nds) =>
      nds.map((node) =>
        node.id === selectedNodeId
          ? { ...node, data: { ...node.data, configuration: config } }
          : node
      )
    );
  }, [selectedNodeId, setNodes]);

  const handleSaveWorkflow = useCallback(() => {
    // TODO: Implement save workflow
    toast.success('Workflow saved successfully!');
  }, []);

  const handleExecuteWorkflow = useCallback(async () => {
    if (nodes.length === 0) {
      toast.error('Please add components to your workflow');
      return;
    }

    setIsExecuting(true);
    try {
      // TODO: Implement workflow execution
      await new Promise(resolve => setTimeout(resolve, 2000)); // Simulate execution
      setExecutionResult({ response: 'Workflow executed successfully!' });
      toast.success('Workflow executed successfully!');
    } catch (error) {
      toast.error('Failed to execute workflow');
    } finally {
      setIsExecuting(false);
    }
  }, [nodes]);

  const handleSendMessage = useCallback(async (message: string) => {
    // TODO: Implement chat with workflow
    await new Promise(resolve => setTimeout(resolve, 1000)); // Simulate API call
    return { response: `Echo: ${message}` };
  }, []);

  const handleCloseConfig = useCallback(() => {
    setSelectedNodeId(null);
  }, []);

  const handleTestComponent = useCallback(() => {
    // TODO: Implement component testing
    toast.success('Component test completed!');
  }, []);

  return (
    <div className="h-screen flex flex-col bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 px-6 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <h1 className="text-2xl font-bold text-gray-900">GenAI Stack</h1>
            <span className="text-sm text-gray-500">Workflow Builder</span>
          </div>
          
          <div className="flex items-center space-x-2">
            <button
              onClick={handleSaveWorkflow}
              className="flex items-center px-4 py-2 text-gray-600 hover:bg-gray-100 rounded-lg"
            >
              <Save className="w-4 h-4 mr-2" />
              Save
            </button>
            
            <button
              onClick={handleExecuteWorkflow}
              disabled={isExecuting}
              className="flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
            >
              <Play className="w-4 h-4 mr-2" />
              {isExecuting ? 'Executing...' : 'Execute'}
            </button>
            
            <button
              onClick={() => setIsChatOpen(true)}
              className="flex items-center px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700"
            >
              <MessageSquare className="w-4 h-4 mr-2" />
              Chat
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div className="flex-1 flex overflow-hidden">
        {/* Component Library */}
        <ComponentLibrary onDragStart={handleDragStart} />
        
        {/* Workflow Canvas */}
        <WorkflowCanvas
          nodes={nodes}
          edges={edges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          onConnect={handleConnect}
          onNodeClick={handleNodeClick}
          selectedNodeId={selectedNodeId}
        />
        
        {/* Configuration Panel */}
        <ComponentConfigPanel
          nodeId={selectedNodeId}
          componentType={selectedNode?.data?.type || null}
          configuration={selectedNode?.data?.configuration || {}}
          onConfigurationChange={handleConfigurationChange}
          onClose={handleCloseConfig}
          onSave={handleSaveWorkflow}
          onTest={handleTestComponent}
        />
      </div>

      {/* Chat Interface */}
      <ChatInterface
        isOpen={isChatOpen}
        onClose={() => setIsChatOpen(false)}
        onSendMessage={handleSendMessage}
        isExecuting={isExecuting}
      />

      {/* Execution Result */}
      {executionResult && (
        <div className="fixed bottom-4 right-4 bg-white border border-gray-200 rounded-lg shadow-lg p-4 max-w-md">
          <div className="flex items-center justify-between mb-2">
            <h3 className="font-semibold text-gray-900">Execution Result</h3>
            <button
              onClick={() => setExecutionResult(null)}
              className="text-gray-400 hover:text-gray-600"
            >
              <X className="w-4 h-4" />
            </button>
          </div>
          <p className="text-sm text-gray-600">{executionResult.response}</p>
        </div>
      )}
    </div>
  );
};

export default WorkflowBuilder;
