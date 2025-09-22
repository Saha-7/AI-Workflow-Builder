# GenAI Stack - No-Code Workflow Builder

A No-Code/Low-Code web application that enables users to visually create and interact with intelligent workflows using drag-and-drop components for document processing, LLM integration, and chat interfaces.

## 🚀 Features

- **Visual Workflow Builder**: Drag-and-drop interface for creating AI workflows
- **Core Components**: User Query, Knowledge Base, LLM Engine, and Output components
- **Document Processing**: Upload and process PDFs with automatic text extraction
- **LLM Integration**: Support for OpenAI GPT and Google Gemini models
- **Web Search**: Integration with SerpAPI for real-time information retrieval
- **Chat Interface**: Interactive chat interface for workflow execution
- **Vector Storage**: ChromaDB integration for document embeddings

## 🛠️ Tech Stack

### Frontend
- React.js with TypeScript
- React Flow for drag-and-drop workflows
- Tailwind CSS for styling
- Axios for API communication

### Backend
- FastAPI (Python)
- PostgreSQL database
- ChromaDB for vector storage
- SQLAlchemy ORM

### AI & ML
- OpenAI GPT models
- Google Gemini
- OpenAI Embeddings
- PyMuPDF for document processing

### Infrastructure
- Docker & Docker Compose
- SerpAPI for web search

## 📁 Project Structure

```
genai-stack/
├── frontend/                 # React frontend application
│   ├── src/
│   │   ├── components/      # Reusable UI components
│   │   ├── pages/          # Page components
│   │   ├── hooks/          # Custom React hooks
│   │   ├── services/       # API service functions
│   │   ├── types/          # TypeScript type definitions
│   │   └── utils/          # Utility functions
│   ├── public/             # Static assets
│   └── package.json
├── backend/                 # FastAPI backend application
│   ├── app/
│   │   ├── api/            # API route handlers
│   │   ├── core/           # Core configuration
│   │   ├── models/         # Database models
│   │   ├── services/       # Business logic
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── utils/          # Utility functions
│   │   └── database/       # Database configuration
│   ├── requirements.txt
│   └── Dockerfile
├── docs/                   # Documentation
├── docker-compose.yml      # Docker orchestration
├── env.example            # Environment variables template
└── README.md
```

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- Node.js 18+ (for local development)
- Python 3.11+ (for local development)

### Environment Setup

1. **Secure Setup** (Recommended):
   ```bash
   python setup-env.py
   ```

2. **Manual Setup**:
   ```bash
   cp env.example .env
   ```

3. **Update the `.env` file** with your API keys:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   GEMINI_API_KEY=your_gemini_api_key_here
   SERPAPI_KEY=your_serpapi_key_here
   DATABASE_URL=your_database_url_here
   SECRET_KEY=your_strong_secret_key_here
   ```

   **⚠️ Security Warning**: Never commit your `.env` file to version control!

### Using Docker (Recommended)

1. Start all services:
   ```bash
   docker-compose up --build
   ```

2. Access the application:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Local Development

#### Backend Setup

1. Navigate to backend directory:
   ```bash
   cd backend
   ```

2. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Start the backend:
   ```bash
   uvicorn app.main:app --reload
   ```

#### Frontend Setup

1. Navigate to frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the frontend:
   ```bash
   npm start
   ```

## 📖 Usage

1. **Create a Workflow**: Use the drag-and-drop interface to create workflows by connecting components
2. **Upload Documents**: Add PDF documents to your knowledge base for context-aware responses
3. **Configure Components**: Set up LLM models, prompts, and other component settings
4. **Execute Workflows**: Use the chat interface to interact with your workflows
5. **Monitor Results**: View responses and manage your workflows

## 🔧 API Endpoints

### Workflows
- `POST /api/workflows` - Create a new workflow
- `GET /api/workflows` - List all workflows
- `GET /api/workflows/{id}` - Get workflow details
- `PUT /api/workflows/{id}` - Update workflow
- `DELETE /api/workflows/{id}` - Delete workflow
- `POST /api/workflows/{id}/execute` - Execute workflow

### Documents
- `POST /api/documents/upload` - Upload document
- `GET /api/documents` - List documents
- `GET /api/documents/{id}` - Get document details
- `DELETE /api/documents/{id}` - Delete document
- `POST /api/documents/{id}/process` - Process document

### LLM
- `POST /api/llm/generate` - Generate response
- `POST /api/llm/chat` - Chat with LLM
- `GET /api/llm/models` - List available models

### Search
- `POST /api/search/web` - Perform web search
- `GET /api/search/suggestions` - Get search suggestions

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions, please open an issue in the GitHub repository.

## 🗺️ Roadmap

- [ ] Advanced workflow validation
- [ ] Real-time collaboration
- [ ] Workflow templates
- [ ] Advanced analytics
- [ ] Multi-tenant support
- [ ] Plugin system for custom components



