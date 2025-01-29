from llama_index.llms.ollama import Ollama
import httpx
import logging
from config import settings

logging.basicConfig(level=logging.INFO)

class AnalyzerAgent:
	def __init__(self):
		self.llm = settings._llm

	def analyze(self, query: str) -> str:
		prompt = f"""Rephrase this query for a preschool teacher:
		Original: {query}
		Simplified:"""
		
		try:
			response = self.llm.complete(prompt)
			print("Printing the response of the analyzer agent...")
			print(response.text)
			return response.text
		except httpx.ReadTimeout:
			logging.error("Ollama timeout! Possible fixes:")
			logging.error("1. Check if model is loaded: `ollama ls`")
			logging.error("2. Increase GPU memory (14B models need >16GB VRAM)")
			logging.error("3. Try simpler model first: `ollama run deepseek-7b`")
			raise
		except Exception as e:
			logging.error(f"Unexpected error: {str(e)}")
			raise