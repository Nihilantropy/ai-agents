from llama_index.core import Settings
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

from config.settings import LLM_MODEL_NAME

# Initialize Ollama LLM
_llm = Ollama(
    model=LLM_MODEL_NAME,
    temperature=0.3,
    base_url="http://localhost:11434",  # Ensure Ollama is running locally
    request_timeout=600,
    num_gpu=24,       # Use all GPU layers
    num_predict=512,  # Limit response length
    top_k=20,         # Reduce sampling complexity
    main_gpu=0,       # Force primary GPU
)

# Initialize HuggingFace Embeddings
_embeddings = HuggingFaceEmbedding(model_name="BAAI/bge-small-en")

# Apply to global LlamaIndex settings
Settings.llm = _llm
Settings.embed_model = _embeddings

class LLMModel:
    """Wrapper for LLM-based text generation."""
    def __init__(self):
        self.model = Settings.llm

    def generate_text(self, prompt: str) -> str:
        """Generate text using the local Ollama model."""
        response = self.model.complete(prompt)
        return response.text  # Ensure correct response parsing
