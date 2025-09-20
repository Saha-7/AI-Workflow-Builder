import React from 'react';
import { Toaster } from 'react-hot-toast';
import WorkflowBuilder from './pages/WorkflowBuilder';
import TestPage from './pages/TestPage';

function App() {
  // Simple routing based on URL path
  const path = window.location.pathname;
  
  return (
    <div className="App">
      {path === '/test' ? <TestPage /> : <WorkflowBuilder />}
      <Toaster position="top-right" />
    </div>
  );
}

export default App;



