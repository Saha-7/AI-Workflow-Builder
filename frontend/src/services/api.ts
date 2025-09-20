import axios from 'axios';
import { Workflow, Document, ChatMessage, ChatSession, ComponentConfiguration } from '../types';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Workflow API
export const workflowApi = {
  // Get all workflows
  getWorkflows: async (): Promise<Workflow[]> => {
    const response = await api.get('/api/workflows');
    return response.data;
  },

  // Get workflow by ID
  getWorkflow: async (id: number): Promise<Workflow> => {
    const response = await api.get(`/api/workflows/${id}`);
    return response.data;
  },

  // Create new workflow
  createWorkflow: async (workflow: Partial<Workflow>): Promise<Workflow> => {
    const response = await api.post('/api/workflows', workflow);
    return response.data;
  },

  // Update workflow
  updateWorkflow: async (id: number, workflow: Partial<Workflow>): Promise<Workflow> => {
    const response = await api.put(`/api/workflows/${id}`, workflow);
    return response.data;
  },

  // Delete workflow
  deleteWorkflow: async (id: number): Promise<void> => {
    await api.delete(`/api/workflows/${id}`);
  },

  // Execute workflow
  executeWorkflow: async (id: number, query: string): Promise<any> => {
    const response = await api.post(`/api/workflows/${id}/execute`, { query });
    return response.data;
  },
};

// Document API
export const documentApi = {
  // Get all documents
  getDocuments: async (workflowId?: number): Promise<Document[]> => {
    const params = workflowId ? { workflow_id: workflowId } : {};
    const response = await api.get('/api/documents', { params });
    return response.data;
  },

  // Get document by ID
  getDocument: async (id: number): Promise<Document> => {
    const response = await api.get(`/api/documents/${id}`);
    return response.data;
  },

  // Upload document
  uploadDocument: async (file: File, workflowId?: number): Promise<Document> => {
    const formData = new FormData();
    formData.append('file', file);
    if (workflowId) {
      formData.append('workflow_id', workflowId.toString());
    }

    const response = await api.post('/api/documents/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  // Delete document
  deleteDocument: async (id: number): Promise<void> => {
    await api.delete(`/api/documents/${id}`);
  },

  // Process document
  processDocument: async (id: number): Promise<any> => {
    const response = await api.post(`/api/documents/${id}/process`);
    return response.data;
  },
};

// LLM API
export const llmApi = {
  // Generate response
  generateResponse: async (request: {
    query: string;
    context?: string;
    model?: string;
    temperature?: number;
    max_tokens?: number;
    prompt?: string;
    use_web_search?: boolean;
  }): Promise<any> => {
    const response = await api.post('/api/llm/generate', request);
    return response.data;
  },

  // Chat with LLM
  chatWithLLM: async (request: {
    query: string;
    context?: string;
    model?: string;
    temperature?: number;
    max_tokens?: number;
    prompt?: string;
    use_web_search?: boolean;
  }): Promise<any> => {
    const response = await api.post('/api/llm/chat', request);
    return response.data;
  },

  // Get available models
  getModels: async (): Promise<any> => {
    const response = await api.get('/api/llm/models');
    return response.data;
  },
};

// Search API
export const searchApi = {
  // Web search
  webSearch: async (query: string, numResults?: number, searchEngine?: string): Promise<any> => {
    const response = await api.post('/api/search/web', {
      query,
      num_results: numResults || 10,
      search_engine: searchEngine || 'google',
    });
    return response.data;
  },

  // Get search suggestions
  getSuggestions: async (query: string): Promise<string[]> => {
    const response = await api.get('/api/search/suggestions', {
      params: { query },
    });
    return response.data;
  },
};

export default api;
