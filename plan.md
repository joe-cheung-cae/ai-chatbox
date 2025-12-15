# AI Chatbox UI Application Development Plan

## Overview
Develop a Python-based AI chatbox desktop application using Tkinter as the UI framework for independent window execution. The application will support local Ollama LLM models with automatic detection and dropdown selection, as well as local knowledge base models (embedding models for text similarity) with similar detection and selection capabilities.

## Requirements
- **UI Framework**: Tkinter for desktop GUI with independent window
- **LLM Support**: Local Ollama models, auto-detected and selectable via dropdown
- **Knowledge Base Support**: Local embedding models (e.g., sentence-transformers), auto-detected and selectable via dropdown
- **Core Features**:
  - Basic chat functionality with selected LLM
  - RAG integration with document upload and embedding retrieval
  - Conversation history and export capabilities
- **Architecture**: Modular design with separate components for model detection, UI, chat logic, and knowledge base management

## System Architecture
```
graph TD
    A[Tkinter App] --> B[Model Detection Module]
    A --> C[Chat Interface]
    B --> D[Ollama Models]
    B --> E[Embedding Models]
    C --> F[Chat Logic]
    F --> D
    F --> E
```

## Implementation Steps
1. **Project Setup**
   - Create project directory structure
   - Set up virtual environment
   - Install required dependencies (tkinter, ollama, sentence-transformers, etc.)

2. **Model Detection Implementation**
   - Implement Ollama model detection using ollama Python API
   - Implement embedding model detection (check installed sentence-transformers models)
   - Create dropdown components for model selection

3. **UI Development**
   - Design Tkinter layout with frames for model selection and chat
   - Implement chat message display area with scrollable text
   - Add input field for user messages and send button
   - Add file upload functionality for knowledge base

4. **Chat Logic Integration**
   - Integrate selected Ollama model for text generation
   - Optionally integrate embedding model for enhanced responses (if needed)
   - Handle conversation state management

5. **Testing and Refinement**
   - Test model detection functionality
   - Test chat interactions
   - Add error handling and user feedback

## Dependencies
- tkinter (built-in)
- ollama
- sentence-transformers
- langchain
- faiss-cpu
- PyPDF2
- python-docx
- torch (for embeddings)
- Other utilities as needed

## File Structure
```
ai-chatbox/
├── app.py                 # Main Tkinter application
├── model_detection.py     # Model detection utilities
├── chat_logic.py          # Chat processing logic
├── knowledge_base.py      # Knowledge base management
├── requirements.txt       # Python dependencies
├── plan.md               # This development plan
└── README.md             # Project documentation
```

## Risk Considerations
- Ollama must be running locally for model detection
- Embedding models require sufficient local resources
- Model loading times may affect user experience
- Tkinter UI may require threading for non-blocking operations

## Success Criteria
- Application launches successfully as independent desktop window
- Ollama models are auto-detected and selectable
- Embedding models are auto-detected and selectable
- Basic chat functionality works with selected models
- Clean, responsive desktop UI suitable for chat interactions
- File upload and knowledge base processing works
- Conversation export functionality available