import ollama
from sentence_transformers import SentenceTransformer

def get_available_ollama_models():
    """Get list of available Ollama models"""
    try:
        models = ollama.list()
        return [model['name'] for model in models['models']]
    except Exception as e:
        print(f"Error detecting Ollama models: {e}")
        return []

def get_available_embedding_models():
    """Get list of available sentence transformer models"""
    # Common local embedding models that might be available
    common_models = [
        'all-MiniLM-L6-v2',
        'all-mpnet-base-v2',
        'paraphrase-MiniLM-L6-v2',
        'distilbert-base-nli-stsb-mean-tokens'
    ]

    available_models = []
    for model_name in common_models:
        try:
            # Try to load the model to check if it's available
            model = SentenceTransformer(model_name)
            available_models.append(model_name)
        except Exception:
            continue

    return available_models

def load_embedding_model(model_name):
    """Load the selected embedding model"""
    try:
        return SentenceTransformer(model_name)
    except Exception as e:
        print(f"Error loading embedding model {model_name}: {e}")
        return None