import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import threading
import json
from datetime import datetime
import ollama
from model_detection import get_available_ollama_models, get_available_embedding_models
from knowledge_base import initialize_knowledge_base, get_knowledge_base

class AIChatboxApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Chatbox with Local Models")
        self.root.geometry("800x600")

        # Initialize variables
        self.messages = []
        self.ollama_model = None
        self.embedding_model = None
        self.knowledge_base_initialized = False

        # Create UI components
        self.create_widgets()

        # Load available models
        self.load_models()

    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Model selection frame
        model_frame = ttk.LabelFrame(main_frame, text="Model Configuration", padding="5")
        model_frame.pack(fill=tk.X, pady=(0, 10))

        # Ollama model selection
        ttk.Label(model_frame, text="Ollama LLM:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.ollama_combo = ttk.Combobox(model_frame, state="readonly")
        self.ollama_combo.grid(row=0, column=1, sticky=tk.EW, padx=(0, 10))
        self.ollama_combo.bind("<<ComboboxSelected>>", self.on_ollama_select)

        # Embedding model selection
        ttk.Label(model_frame, text="Embedding Model:").grid(row=1, column=0, sticky=tk.W, padx=(0, 5), pady=(5, 0))
        self.embedding_combo = ttk.Combobox(model_frame, state="readonly")
        self.embedding_combo.grid(row=1, column=1, sticky=tk.EW, padx=(0, 10), pady=(5, 0))
        self.embedding_combo.bind("<<ComboboxSelected>>", self.on_embedding_select)

        # Configure grid weights
        model_frame.columnconfigure(1, weight=1)

        # Knowledge base frame
        kb_frame = ttk.LabelFrame(main_frame, text="Knowledge Base", padding="5")
        kb_frame.pack(fill=tk.X, pady=(0, 10))

        self.upload_btn = ttk.Button(kb_frame, text="Upload Documents", command=self.upload_files)
        self.upload_btn.pack(side=tk.LEFT, padx=(0, 10))

        self.process_btn = ttk.Button(kb_frame, text="Process Documents", command=self.process_documents, state=tk.DISABLED)
        self.process_btn.pack(side=tk.LEFT)

        # Chat frame
        chat_frame = ttk.LabelFrame(main_frame, text="Chat", padding="5")
        chat_frame.pack(fill=tk.BOTH, expand=True)

        # Chat display
        self.chat_text = scrolledtext.ScrolledText(chat_frame, wrap=tk.WORD, state=tk.DISABLED)
        self.chat_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # Input frame
        input_frame = ttk.Frame(chat_frame)
        input_frame.pack(fill=tk.X)

        self.input_entry = ttk.Entry(input_frame)
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.input_entry.bind("<Return>", self.send_message)

        self.send_btn = ttk.Button(input_frame, text="Send", command=self.send_message)
        self.send_btn.pack(side=tk.RIGHT)

        # Control buttons frame
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=(10, 0))

        self.export_btn = ttk.Button(control_frame, text="Export Conversation", command=self.export_conversation)
        self.export_btn.pack(side=tk.LEFT, padx=(0, 10))

        self.clear_btn = ttk.Button(control_frame, text="Clear Chat", command=self.clear_chat)
        self.clear_btn.pack(side=tk.LEFT)

    def load_models(self):
        # Load Ollama models
        ollama_models = get_available_ollama_models()
        if ollama_models:
            self.ollama_combo['values'] = ollama_models
            self.ollama_combo.set(ollama_models[0])
            self.ollama_model = ollama_models[0]
        else:
            messagebox.showerror("Error", "No Ollama models detected. Please ensure Ollama is running and models are installed.")

        # Load embedding models
        embedding_models = get_available_embedding_models()
        if embedding_models:
            self.embedding_combo['values'] = embedding_models
            self.embedding_combo.set(embedding_models[0])
            self.embedding_model = embedding_models[0]
            initialize_knowledge_base(embedding_models[0])
            self.knowledge_base_initialized = True
            self.process_btn.config(state=tk.NORMAL)

    def on_ollama_select(self, event):
        self.ollama_model = self.ollama_combo.get()

    def on_embedding_select(self, event):
        self.embedding_model = self.embedding_combo.get()
        initialize_knowledge_base(self.embedding_model)
        self.knowledge_base_initialized = True
        self.process_btn.config(state=tk.NORMAL)

    def upload_files(self):
        files = filedialog.askopenfilenames(
            title="Select documents",
            filetypes=[("PDF files", "*.pdf"), ("Word files", "*.docx"), ("Text files", "*.txt")]
        )
        if files:
            self.uploaded_files = files
            self.process_btn.config(state=tk.NORMAL)

    def process_documents(self):
        if hasattr(self, 'uploaded_files') and self.uploaded_files:
            kb = get_knowledge_base()
            if kb:
                # Process files (this might take time, so run in thread)
                threading.Thread(target=self._process_files_thread, args=(kb,)).start()
        else:
            messagebox.showwarning("Warning", "Please upload files first.")

    def _process_files_thread(self, kb):
        try:
            # Convert file paths to file-like objects
            documents = []
            for file_path in self.uploaded_files:
                with open(file_path, 'rb') as f:
                    # Create a file-like object that matches the expected interface
                    import io
                    file_obj = io.BytesIO(f.read())
                    file_obj.name = file_path.split('/')[-1]  # Set name attribute
                    documents.extend(kb.process_uploaded_files([file_obj]))

            if documents:
                kb.create_vectorstore(documents)
                messagebox.showinfo("Success", "Knowledge base updated!")
            else:
                messagebox.showwarning("Warning", "No documents were processed.")
        except Exception as e:
            messagebox.showerror("Error", f"Error processing documents: {e}")

    def send_message(self, event=None):
        prompt = self.input_entry.get().strip()
        if not prompt:
            return

        if not self.ollama_model:
            messagebox.showerror("Error", "Please select an Ollama model first.")
            return

        # Clear input
        self.input_entry.delete(0, tk.END)

        # Add user message
        self.add_message("user", prompt)

        # Generate response in thread
        threading.Thread(target=self._generate_response, args=(prompt,)).start()

    def _generate_response(self, prompt):
        try:
            # Get context from knowledge base if available
            context = ""
            if self.knowledge_base_initialized:
                kb = get_knowledge_base()
                if kb and kb.vectorstore:
                    similar_docs = kb.search_similar(prompt)
                    if similar_docs:
                        context = "\n".join(similar_docs)

            # Chat with Ollama
            response = self.chat_with_ollama(prompt, context)

            # Add assistant response
            self.add_message("assistant", response)

        except Exception as e:
            self.add_message("assistant", f"Error: {e}")

    def chat_with_ollama(self, prompt, context=""):
        """Chat with Ollama model"""
        try:
            if context:
                full_prompt = f"Context: {context}\n\nQuestion: {prompt}"
            else:
                full_prompt = prompt

            response = ollama.chat(
                model=self.ollama_model,
                messages=[{'role': 'user', 'content': full_prompt}]
            )
            return response['message']['content']
        except Exception as e:
            return f"Error: {e}"

    def add_message(self, role, content):
        """Add message to chat display"""
        self.messages.append({"role": role, "content": content, "timestamp": datetime.now().isoformat()})

        # Update display
        self.chat_text.config(state=tk.NORMAL)
        if role == "user":
            self.chat_text.insert(tk.END, f"You: {content}\n\n", "user")
        else:
            self.chat_text.insert(tk.END, f"Assistant: {content}\n\n", "assistant")
        self.chat_text.config(state=tk.DISABLED)
        self.chat_text.see(tk.END)

        # Configure tags
        self.chat_text.tag_config("user", foreground="blue")
        self.chat_text.tag_config("assistant", foreground="green")

    def export_conversation(self):
        """Export conversation as JSON"""
        if not self.messages:
            messagebox.showwarning("Warning", "No conversation to export.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")],
            title="Save Conversation"
        )

        if file_path:
            conversation_data = {
                'export_date': datetime.now().isoformat(),
                'ollama_model': self.ollama_model,
                'embedding_model': self.embedding_model,
                'messages': self.messages
            }

            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(conversation_data, f, indent=2, ensure_ascii=False)
                messagebox.showinfo("Success", "Conversation exported successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export conversation: {e}")

    def clear_chat(self):
        """Clear chat history"""
        self.messages = []
        self.chat_text.config(state=tk.NORMAL)
        self.chat_text.delete(1.0, tk.END)
        self.chat_text.config(state=tk.DISABLED)

def main():
    root = tk.Tk()
    app = AIChatboxApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()