# GenAI Stack - No-Code Workflow Builder

## Project Overview
A No-Code/Low-Code web application that enables users to visually create and interact with intelligent workflows using drag-and-drop components for document processing, LLM integration, and chat interfaces.

## Tech Stack
- **Frontend**: React.js with React Flow for drag-and-drop
- **Backend**: FastAPI
- **Database**: PostgreSQL
- **Vector Store**: ChromaDB
- **Embedding Model**: OpenAI Embeddings
- **LLM**: OpenAI GPT, Gemini
- **Web Search**: SerpAPI/Brave
- **Text Extraction**: PyMuPDF
- **Containerization**: Docker

## Core Components

### 1. User Query Component
- [ ] Accepts user queries via simple interface
- [ ] Serves as workflow entry point
- [ ] Forwards query to connected components

### 2. Knowledge Base Component
- [ ] Document upload and processing (PDFs)
- [ ] Text extraction using PyMuPDF
- [ ] Embedding generation with OpenAI/Gemini
- [ ] Vector storage in ChromaDB
- [ ] Context retrieval based on queries
- [ ] Optional context passing to LLM

### 3. LLM Engine Component
- [ ] Accepts query from User Query Component
- [ ] Optional context from Knowledge Base
- [ ] Custom prompt configuration
- [ ] LLM integration (OpenAI GPT, Gemini)
- [ ] Optional web search via SerpAPI
- [ ] Response generation and forwarding

### 4. Output Component
- [ ] Chat interface for displaying responses
- [ ] Support for follow-up questions
- [ ] Workflow re-execution capability

## Implementation Plan

### Phase 1: Project Setup
- [ ] Create project structure (frontend/, backend/, docs/)
- [ ] Set up package.json and requirements.txt
- [ ] Initialize Git repository
- [ ] Create basic README

### Phase 2: Backend Development
- [ ] Set up FastAPI application structure
- [ ] Configure PostgreSQL database
- [ ] Set up ChromaDB for vector storage
- [ ] Create database models and migrations
- [ ] Implement API endpoints for:
  - [ ] Document upload and processing
  - [ ] Embedding generation and storage
  - [ ] Workflow execution
  - [ ] LLM integration
  - [ ] Web search integration

### Phase 3: Frontend Development
- [ ] Set up React application with TypeScript
- [ ] Install and configure React Flow
- [ ] Create component library panel
- [ ] Implement drag-and-drop workspace
- [ ] Build component configuration panels
- [ ] Create chat interface
- [ ] Implement workflow validation

### Phase 4: Integration & Testing
- [ ] Connect frontend to backend APIs
- [ ] Implement workflow execution logic
- [ ] Test component interactions
- [ ] Validate end-to-end workflows
- [ ] Error handling and validation

### Phase 5: Deployment & Documentation
- [ ] Create Dockerfiles for frontend and backend
- [ ] Set up docker-compose.yml
- [ ] Create deployment documentation
- [ ] Write comprehensive README
- [ ] Create architecture diagram

## API Endpoints (Backend)

### Document Management
- `POST /api/documents/upload` - Upload and process documents
- `GET /api/documents` - List uploaded documents
- `DELETE /api/documents/{id}` - Delete document

### Knowledge Base
- `POST /api/knowledge-base/process` - Process document for embeddings
- `GET /api/knowledge-base/search` - Search for relevant context
- `POST /api/knowledge-base/query` - Query knowledge base

### Workflow Management
- `POST /api/workflows` - Create new workflow
- `GET /api/workflows` - List workflows
- `GET /api/workflows/{id}` - Get workflow details
- `PUT /api/workflows/{id}` - Update workflow
- `DELETE /api/workflows/{id}` - Delete workflow

### LLM Integration
- `POST /api/llm/generate` - Generate response using LLM
- `POST /api/llm/chat` - Chat with LLM
- `GET /api/llm/models` - List available models

### Web Search
- `POST /api/search/web` - Perform web search
- `GET /api/search/suggestions` - Get search suggestions

## Database Schema

### Tables
- `workflows` - Store workflow definitions
- `components` - Store component configurations
- `documents` - Store document metadata
- `embeddings` - Store embedding metadata
- `chat_sessions` - Store chat history
- `chat_messages` - Store individual messages

## Environment Variables Required

### Backend
- `DATABASE_URL` - PostgreSQL connection string
- `OPENAI_API_KEY` - OpenAI API key
- `GEMINI_API_KEY` - Google Gemini API key
- `SERPAPI_KEY` - SerpAPI key for web search
- `CHROMA_HOST` - ChromaDB host
- `CHROMA_PORT` - ChromaDB port

### Frontend
- `REACT_APP_API_URL` - Backend API URL
- `REACT_APP_WS_URL` - WebSocket URL for real-time updates

## Questions for User Input

1. **API Keys**: Do you have the required API keys (OpenAI, Gemini, SerpAPI)?
2. **Database Setup**: Do you have PostgreSQL and ChromaDB running locally, or should we use Docker?
3. **Deployment**: Do you want to deploy this locally or on a cloud platform?
4. **Additional Features**: Are there any specific features from the optional list you'd like to prioritize?

## File Structure
```
genai-stack/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── hooks/
│   │   ├── services/
│   │   └── types/
│   ├── public/
│   └── package.json
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── models/
│   │   └── services/
│   ├── requirements.txt
│   └── Dockerfile
├── docs/
│   ├── README.md
│   └── architecture.md
├── docker-compose.yml
└── README.md
```

## Success Criteria
- [ ] Users can drag and drop components to create workflows
- [ ] Workflows can process documents and generate embeddings
- [ ] LLM integration works with multiple providers
- [ ] Chat interface allows interaction with workflows
- [ ] Application is fully containerized and deployable
- [ ] Code is well-documented and modular
- [ ] All core requirements are met

## Next Steps
1. Set up the project structure
2. Begin with backend API development
3. Create basic frontend components
4. Integrate and test the workflow execution
5. Add advanced features and polish
