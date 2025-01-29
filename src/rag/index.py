from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.core.node_parser import MarkdownNodeParser
from llama_index.core import Settings
from .loader import load_documents

def build_index():
    documents = load_documents()
    if not documents:
        # Return empty index if no documents
        return VectorStoreIndex([])
    
    node_parser = MarkdownNodeParser()
    nodes = node_parser.get_nodes_from_documents(documents)
    index = VectorStoreIndex(nodes, embed_model=Settings.embed_model)
    index.storage_context.persist(persist_dir="data/index")
    return index