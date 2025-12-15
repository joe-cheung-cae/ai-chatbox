from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
import PyPDF2
import docx
import os
from typing import List, Tuple

class KnowledgeBase:
    def __init__(self, embedding_model_name: str):
        self.embedding_model_name = embedding_model_name
        self.embeddings = HuggingFaceEmbeddings(model_name=embedding_model_name)
        self.vectorstore = None
        self.documents = []

    def extract_text_from_pdf(self, file) -> str:
        """Extract text from PDF file"""
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text

    def extract_text_from_docx(self, file) -> str:
        """Extract text from DOCX file"""
        doc = docx.Document(file)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text

    def extract_text_from_txt(self, file) -> str:
        """Extract text from TXT file"""
        return file.read().decode('utf-8')

    def process_uploaded_files(self, uploaded_files) -> List[str]:
        """Process uploaded files and return list of document texts"""
        documents = []

        for uploaded_file in uploaded_files:
            file_extension = os.path.splitext(uploaded_file.name)[1].lower()

            try:
                if file_extension == '.pdf':
                    text = self.extract_text_from_pdf(uploaded_file)
                elif file_extension == '.docx':
                    text = self.extract_text_from_docx(uploaded_file)
                elif file_extension == '.txt':
                    text = self.extract_text_from_txt(uploaded_file)
                else:
                    print(f"Unsupported file type: {file_extension}")
                    continue

                if text.strip():
                    documents.append(text)
                    print(f"Processed {uploaded_file.name}")
                else:
                    print(f"No text extracted from {uploaded_file.name}")

            except Exception as e:
                print(f"Error processing {uploaded_file.name}: {e}")

        return documents

    def create_vectorstore(self, documents: List[str]):
        """Create FAISS vectorstore from documents"""
        if not documents:
            return

        # Split documents into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )

        chunks = []
        for doc in documents:
            chunks.extend(text_splitter.split_text(doc))

        # Create vectorstore
        self.vectorstore = FAISS.from_texts(chunks, self.embeddings)
        print(f"Created vectorstore with {len(chunks)} chunks")

    def search_similar(self, query: str, k: int = 3) -> List[str]:
        """Search for similar documents"""
        if not self.vectorstore:
            return []

        docs = self.vectorstore.similarity_search(query, k=k)
        return [doc.page_content for doc in docs]

# Global knowledge base instance
knowledge_base = None

def initialize_knowledge_base(embedding_model_name: str):
    """Initialize global knowledge base"""
    global knowledge_base
    knowledge_base = KnowledgeBase(embedding_model_name)

def get_knowledge_base():
    """Get global knowledge base instance"""
    return knowledge_base