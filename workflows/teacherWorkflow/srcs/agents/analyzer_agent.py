import httpx
import logging
from llm import settings

logging.basicConfig(level=logging.INFO)

class AnalyzerAgent:
	def __init__(self):
		self.llm = settings._llm

	def analyze(self, query: str) -> str:
		prompt = f"""A child  asked a question, analyze it. If the question is well done, simply return it as it is.
		If the question has problems (like mispell, illogical connection etc...), rephrase it correctly. The output of this question will
		be passed to another ai-agent that will respond to the question. Your only job is to analyze it and give teh most clear and clean
		result of this analysis to the teacher-agent as a response. The original query is as follow:
		Original: {query}
		Result:"""
		
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