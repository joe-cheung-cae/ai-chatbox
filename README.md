# AI Chatbox Application

A Python-based AI chatbox application built with Streamlit that supports local Ollama LLM models and knowledge base integration using RAG (Retrieval-Augmented Generation).

## Features

- **Local Ollama Integration**: Automatically detects and allows selection of locally available Ollama models
- **Embedding Model Support**: Automatically detects and allows selection of local sentence transformer models
- **RAG Knowledge Base**: Upload and process PDF, DOCX, and TXT documents for enhanced responses
- **Conversation History**: Maintains chat history with export functionality
- **Modern UI**: Clean Streamlit interface for easy interaction

## Prerequisites

1. **Python 3.8+**
2. **Ollama**: Install and run Ollama locally with models downloaded
   ```bash
   # Install Ollama (see https://ollama.ai)
   # Pull some models
   ollama pull llama2
   ollama pull mistral
   ```
3. **Required Python packages**:
   ```bash
   pip install streamlit ollama sentence-transformers langchain faiss-cpu PyPDF2 python-docx
   ```

## Installation

1. Clone or download this repository
2. Set up the Python virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
3. Ensure Ollama is running with models available:
   ```bash
   # Install Ollama from https://ollama.ai
   ollama pull llama2  # or any other model you want
   ```

## Usage

1. Start the application:
   ```bash
   # Option 1: Use the provided script
   ./run.sh

   # Option 2: Manual activation and run
   source venv/bin/activate
   streamlit run app.py
   ```

2. In the sidebar:
   - Select an available Ollama model from the dropdown
   - Select an embedding model for knowledge base processing
   - Upload documents (PDF/DOCX/TXT) to build knowledge base
   - Click "Process Documents" to create the vector database

3. Start chatting in the main interface

4. Use "Export Conversation" to download chat history as JSON

## File Structure

```
ai-chatbox/
├── app.py                 # Main Streamlit application
├── model_detection.py     # Model detection utilities
├── knowledge_base.py      # Document processing and vector database
├── requirements.txt       # Python dependencies
├── plan.md               # Development plan
└── README.md             # This file
```

## Architecture

- **Model Detection**: Automatically scans for available Ollama and embedding models
- **Knowledge Base**: Uses LangChain and FAISS for document chunking and vector search
- **Chat Logic**: Integrates RAG by retrieving relevant context before generating responses
- **UI State Management**: Uses Streamlit session state for conversation persistence

## Troubleshooting

- **No Ollama models detected**: Ensure Ollama is running and has models installed
- **Embedding model errors**: Check if sentence-transformers models are available
- **Document processing fails**: Verify file formats are supported (PDF/DOCX/TXT)

## Development

The application follows a modular architecture with separate concerns:
- Model detection and loading
- Document processing and vectorization
- Chat interface and state management
- RAG integration for enhanced responses