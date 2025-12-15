import ollama
from sentence_transformers import SentenceTransformer

def get_available_ollama_models():
    """Get list of available Ollama models"""
    try:
        models = ollama.list()
        return [model.model for model in models.models]
    except Exception as e:
        print(f"Error detecting Ollama models: {e}")
        return []

def get_available_embedding_models():
    """Get list of available sentence transformer models"""
    # Common embedding models - check if they exist locally
    import os
    from sentence_transformers import util

    common_models = [
        'all-MiniLM-L6-v2',
        'all-mpnet-base-v2',
        'paraphrase-MiniLM-L6-v2',
        'distilbert-base-nli-stsb-mean-tokens'
    ]

    available_models = []
    for model_name in common_models:
        try:
            # Check if model is cached locally without downloading
            cache_folder = os.path.join(os.path.expanduser('~'), '.cache', 'torch', 'sentence_transformers')
            model_path = os.path.join(cache_folder, model_name.replace('/', '_'))

            if os.path.exists(model_path) and os.path.isdir(model_path):
                # Check if essential files exist
                config_file = os.path.join(model_path, 'config_sentence_transformers.json')
                if os.path.exists(config_file):
                    available_models.append(model_name)
        except Exception:
            continue

    # If no local models found, return a basic one that should work
    if not available_models:
        available_models = ['all-MiniLM-L6-v2']  # This will be downloaded when needed

    return available_models

def load_embedding_model(model_name):
    """Load the selected embedding model"""
    try:
        return SentenceTransformer(model_name)
    except Exception as e:
        print(f"Error loading embedding model {model_name}: {e}")
        return None