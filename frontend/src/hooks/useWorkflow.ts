import { useState, useEffect, useCallback } from 'react';
import { Workflow, Component, Connection } from '../types';
import { workflowApi } from '../services/api';

export const useWorkflow = (workflowId?: number) => {
  const [workflow, setWorkflow] = useState<Workflow | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const loadWorkflow = useCallback(async () => {
    if (!workflowId) return;
    
    setLoading(true);
    setError(null);
    
    try {
      const data = await workflowApi.getWorkflow(workflowId);
      setWorkflow(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load workflow');
    } finally {
      setLoading(false);
    }
  }, [workflowId]);

  const saveWorkflow = useCallback(async (workflowData: Partial<Workflow>) => {
    if (!workflow) return;
    
    setLoading(true);
    setError(null);
    
    try {
      const updatedWorkflow = await workflowApi.updateWorkflow(workflow.id, workflowData);
      setWorkflow(updatedWorkflow);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to save workflow');
    } finally {
      setLoading(false);
    }
  }, [workflow]);

  const executeWorkflow = useCallback(async (query: string) => {
    if (!workflow) return null;
    
    setLoading(true);
    setError(null);
    
    try {
      const result = await workflowApi.executeWorkflow(workflow.id, query);
      return result;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to execute workflow');
      return null;
    } finally {
      setLoading(false);
    }
  }, [workflow]);

  useEffect(() => {
    loadWorkflow();
  }, [loadWorkflow]);

  return {
    workflow,
    loading,
    error,
    loadWorkflow,
    saveWorkflow,
    executeWorkflow,
  };
};
