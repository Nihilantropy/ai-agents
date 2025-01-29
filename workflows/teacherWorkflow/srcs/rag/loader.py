from llama_parse import LlamaParse
from llama_index.core import SimpleDirectoryReader
import os
from pathlib import Path

def load_documents(data_dir="data/docs"):
    data_path = Path(data_dir)
    
    # Check if directory exists and has files
    if not data_path.exists() or not any(data_path.iterdir()):
        print("No documents found in data/docs. Continuing without RAG context.")
        return []
    
    # Initialize LlamaParse with API key
    parser = LlamaParse(
        api_key=os.getenv("LLAMA_CLOUD_API_KEY"),  # Load from .env
        result_type="markdown"
    )
    
    documents = SimpleDirectoryReader(
        data_dir, 
        file_extractor={".pdf": parser}
    ).load_data()
    
    return documents