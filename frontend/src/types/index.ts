// Core workflow types
export interface Workflow {
  id: number;
  name: string;
  description?: string;
  components: Component[];
  connections: Connection[];
  is_active: boolean;
  created_at: string;
  updated_at?: string;
}

export interface Component {
  id: string;
  type: ComponentType;
  position: { x: number; y: number };
  configuration: ComponentConfiguration;
}

export interface Connection {
  id: string;
  source: string;
  target: string;
  sourceHandle?: string;
  targetHandle?: string;
}

export type ComponentType = 
  | 'user_query' 
  | 'knowledge_base' 
  | 'llm_engine' 
  | 'output';

export interface ComponentConfiguration {
  // User Query Component
  placeholder?: string;
  
  // Knowledge Base Component
  max_results?: number;
  similarity_threshold?: number;
  
  // LLM Engine Component
  model?: string;
  temperature?: number;
  max_tokens?: number;
  prompt?: string;
  use_web_search?: boolean;
  
  // Output Component
  response_format?: 'text' | 'markdown' | 'json';
}

// API types
export interface ApiResponse<T> {
  data: T;
  message?: string;
  error?: string;
}

export interface Document {
  id: number;
  filename: string;
  file_path: string;
  file_size?: number;
  file_type?: string;
  content?: string;
  processed: boolean;
  workflow_id?: number;
  created_at: string;
  updated_at?: string;
}

export interface ChatMessage {
  id: number;
  content: string;
  is_user: boolean;
  created_at: string;
}

export interface ChatSession {
  id: number;
  workflow_id: number;
  session_name?: string;
  messages: ChatMessage[];
  created_at: string;
  updated_at?: string;
}

// React Flow types
export interface NodeData {
  type: ComponentType;
  configuration: ComponentConfiguration;
  label: string;
  description: string;
}

// UI types
export interface WorkflowBuilderState {
  nodes: any[];
  edges: any[];
  selectedNode: string | null;
  isExecuting: boolean;
  executionResult: any;
}

export interface ComponentLibraryItem {
  type: ComponentType;
  label: string;
  description: string;
  icon: string;
  color: string;
}
