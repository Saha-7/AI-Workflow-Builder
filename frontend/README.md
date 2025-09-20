# GenAI Stack Frontend

A React-based frontend application for building and managing AI workflows with a drag-and-drop interface.

## 🚀 Features

- **Drag & Drop Workflow Builder**: Visual interface for creating AI workflows
- **Component Library**: Pre-built components for different workflow steps
- **Real-time Configuration**: Configure components with live preview
- **Chat Interface**: Interactive chat with your workflows
- **Document Management**: Upload and process documents for knowledge base
- **Responsive Design**: Works on desktop and mobile devices

## 🛠️ Tech Stack

- **React 18** with TypeScript
- **React Flow** for drag-and-drop workflows
- **Tailwind CSS** for styling
- **Lucide React** for icons
- **Axios** for API communication
- **React Hot Toast** for notifications

## 📁 Project Structure

```
src/
├── components/          # Reusable UI components
│   ├── ComponentLibrary.tsx
│   ├── WorkflowCanvas.tsx
│   ├── WorkflowNode.tsx
│   ├── ComponentConfigPanel.tsx
│   └── ChatInterface.tsx
├── pages/              # Page components
│   ├── WorkflowBuilder.tsx
│   └── TestPage.tsx
├── hooks/              # Custom React hooks
│   ├── useWorkflow.ts
│   └── useDocuments.ts
├── services/           # API service functions
│   └── api.ts
├── types/              # TypeScript type definitions
│   └── index.ts
├── utils/              # Utility functions
├── App.tsx             # Main app component
└── index.tsx           # App entry point
```

## 🚀 Getting Started

### Prerequisites

- Node.js 18+ 
- npm or yarn
- Backend API running on port 8000

### Installation

1. Install dependencies:
   ```bash
   npm install
   ```

2. Set up environment variables:
   ```bash
   node setup.js
   ```

3. Start the development server:
   ```bash
   npm start
   ```

4. Open [http://localhost:3000](http://localhost:3000) in your browser

### Testing

Visit [http://localhost:3000/test](http://localhost:3000/test) to run the frontend test suite.

## 🎯 Usage

### Creating a Workflow

1. **Add Components**: Drag components from the library to the canvas
2. **Connect Components**: Draw connections between components
3. **Configure Components**: Click on components to configure their settings
4. **Save Workflow**: Click the Save button to persist your workflow
5. **Execute Workflow**: Click Execute to run the workflow
6. **Chat with Workflow**: Click Chat to interact with your workflow

### Component Types

#### User Query Component
- Accepts user input and queries
- Configurable placeholder text

#### Knowledge Base Component
- Processes and searches documents
- Configurable max results and similarity threshold

#### LLM Engine Component
- Generates responses using AI models
- Support for OpenAI GPT and Google Gemini
- Configurable temperature, max tokens, and system prompts
- Optional web search integration

#### Output Component
- Displays the final response
- Configurable response format (text, markdown, JSON)

### Document Management

1. **Upload Documents**: Use the upload button in the component library
2. **Process Documents**: Documents are automatically processed for embeddings
3. **Search Documents**: Knowledge base components can search uploaded documents

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the frontend directory:

```env
REACT_APP_API_URL=http://localhost:8000
REACT_APP_WS_URL=ws://localhost:8000
```

### API Integration

The frontend communicates with the backend API through the `services/api.ts` file. All API calls are centralized and typed for better maintainability.

## 🎨 Styling

The application uses Tailwind CSS for styling. Key design principles:

- **Clean Interface**: Minimalist design with clear visual hierarchy
- **Responsive Layout**: Adapts to different screen sizes
- **Accessible**: Proper contrast ratios and keyboard navigation
- **Consistent**: Unified color scheme and spacing

## 🧪 Testing

The application includes a test page that verifies:

- API connection to backend
- Component loading and functionality
- Styling and CSS integration

## 🚀 Deployment

### Build for Production

```bash
npm run build
```

This creates a `build` folder with optimized production files.

### Docker Deployment

The frontend is containerized and can be deployed using Docker:

```bash
docker build -t genai-stack-frontend .
docker run -p 3000:3000 genai-stack-frontend
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For support and questions, please open an issue in the GitHub repository.
