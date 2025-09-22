import React from 'react';
import { Toaster } from 'react-hot-toast';
import WorkflowBuilder from './pages/WorkflowBuilder';
import MyStacks from './pages/MyStacks';

function App() {
  // Simple routing based on URL path
  const path = window.location.pathname;
  
  return (
    <div className="App bg-gray-900 min-h-screen">
      {path.startsWith('/workflow') ? <WorkflowBuilder /> : <MyStacks />}
      <Toaster position="top-right" />
    </div>
  );
}

export default App;



