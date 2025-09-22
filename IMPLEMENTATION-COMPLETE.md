# 🎉 GenAI Stack - No-Code AI Workflow Platform

A complete No-Code/Low-Code web application for building intelligent AI workflows with drag-and-drop components, document processing, and real-time chat interface.

## 🚀 Quick Start

### Prerequisites
- **Docker & Docker Compose** (Recommended)
- **Node.js 18+** (for local development)
- **Python 3.11+** (for local development)

### Option 1: Docker (Recommended)

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd AI-WorkFlow
   ```

2. **Set up environment variables**
   ```bash
   cp env.example .env
   ```

3. **Edit `.env` file with your API keys**
   ```env
   # Required API Keys
   OPENAI_API_KEY=your_openai_api_key_here
   GEMINI_API_KEY=your_gemini_api_key_here
   SERPAPI_KEY=your_serpapi_key_here
   
   # Database (use provided or your own)
   DATABASE_URL=postgresql://postgres:password@localhost:5432/genai_stack
   
   # Security
   SECRET_KEY=your_strong_secret_key_here
   ```

4. **Start the application**
   ```bash
   docker-compose up --build
   ```

5. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

### Option 2: Local Development

1. **Backend Setup**
   ```bash
   cd backend
   pip install -r requirements.txt
   python setup.py
   python start.py
   ```

2. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   npm start
   ```

## 🎯 How to Use

### 1. **Build a Workflow**
- Drag components from the left panel to the canvas
- Connect components with edges
- Configure each component's settings
- Click "Save" to save your workflow

### 2. **Upload Documents**
- Go to Documents section
- Upload PDF, TXT, or MD files
- Documents are automatically processed and indexed

### 3. **Chat with Your Workflow**
- Save a workflow first
- Click "Chat" button
- Ask questions and get intelligent responses
- Your workflow processes queries through all components

## 🔧 Features

- **Drag & Drop Workflow Builder**: Visual workflow creation
- **Multiple LLM Support**: OpenAI GPT & Google Gemini
- **Document Processing**: PDF, TXT, MD file support
- **Vector Search**: Semantic document search with ChromaDB
- **Web Search**: Real-time web search with SerpAPI
- **Real-time Chat**: Interactive chat with workflows
- **Secure**: Environment-based API key management

## 🛡️ Security

- All API keys stored in environment variables
- No secrets committed to git
- Comprehensive `.gitignore` files
- Security check script included

## 📁 Project Structure

```
AI-WorkFlow/
├── backend/           # FastAPI backend
├── frontend/          # React frontend
├── docker-compose.yml # Docker orchestration
├── .env.example       # Environment template
└── README.md          # Detailed documentation
```

## 🆘 Troubleshooting

- **Port conflicts**: Change ports in `docker-compose.yml`
- **API key errors**: Check your `.env` file
- **Database issues**: Ensure PostgreSQL is running
- **Frontend not loading**: Check if backend is running on port 8000

## 📚 API Documentation

Once running, visit http://localhost:8000/docs for complete API documentation.

---

**🎉 You're ready to build AI workflows! Start by creating your first workflow and chatting with it.**
