import { useState, useEffect, useCallback } from 'react';
import { Document } from '../types';
import { documentApi } from '../services/api';

export const useDocuments = (workflowId?: number) => {
  const [documents, setDocuments] = useState<Document[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const loadDocuments = useCallback(async () => {
    setLoading(true);
    setError(null);
    
    try {
      const data = await documentApi.getDocuments(workflowId);
      setDocuments(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load documents');
    } finally {
      setLoading(false);
    }
  }, [workflowId]);

  const uploadDocument = useCallback(async (file: File) => {
    setLoading(true);
    setError(null);
    
    try {
      const newDocument = await documentApi.uploadDocument(file, workflowId);
      setDocuments(prev => [...prev, newDocument]);
      return newDocument;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to upload document');
      return null;
    } finally {
      setLoading(false);
    }
  }, [workflowId]);

  const deleteDocument = useCallback(async (id: number) => {
    setLoading(true);
    setError(null);
    
    try {
      await documentApi.deleteDocument(id);
      setDocuments(prev => prev.filter(doc => doc.id !== id));
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to delete document');
    } finally {
      setLoading(false);
    }
  }, []);

  const processDocument = useCallback(async (id: number) => {
    setLoading(true);
    setError(null);
    
    try {
      const result = await documentApi.processDocument(id);
      // Update the document's processed status
      setDocuments(prev => 
        prev.map(doc => 
          doc.id === id ? { ...doc, processed: true } : doc
        )
      );
      return result;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to process document');
      return null;
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadDocuments();
  }, [loadDocuments]);

  return {
    documents,
    loading,
    error,
    loadDocuments,
    uploadDocument,
    deleteDocument,
    processDocument,
  };
};
