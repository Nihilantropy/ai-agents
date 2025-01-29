from llama_index.core import Settings
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

# Singleton LLM instance (shared across agents)
_llm = Ollama(
    model="deepseek-r1:7b",
    temperature=0.3,
    base_url="http://localhost:11434",
    request_timeout=600,
    num_gpu=24,       # Use all GPU layers
    num_predict=512,  # Limit response length
    top_k=20,         # Reduce sampling complexity
    main_gpu=0,       # Force primary GPU
)

# Singleton Embeddings
_embeddings = HuggingFaceEmbedding(model_name="BAAI/bge-small-en")

# Global settings
Settings.llm = _llm
Settings.embed_model = _embeddings