from config import settings

class TeacherAgent:
	def __init__(self):
		self.llm = settings._llm
	
	def teach(self, refined_query: str, context: str) -> str:
		prompt = f"""
		You are a teacher for children aged 3-6. Use simple words, short sentences, and playful examples.
		Context: {context}
		Question: {refined_query}
		Answer:
		"""
		response = self.llm.complete(prompt)
		print("Printing the response of teh teacher agent...")
		print(response.text)
		return response.text