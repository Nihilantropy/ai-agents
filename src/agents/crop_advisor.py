from llama_index.core.agent import ReActAgent

class CropAgent:
    def __init__(self):
        self.agent = ReActAgent.from_tools(...)
