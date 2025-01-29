from llm import settings

class ReviewerAgent:
	def __init__(self):
		self.llm = settings._llm
	
	def review(self, response: str) -> str:
		prompt = f"""
		Review this response for a 3-6 year old. Ensure it is:
		- Accurate
		- Simple (no complex words)
		- Engaging (use stories or analogies)
		- Safe (no inappropriate content)
		Response: {response}
		Revised Response (or 'APPROVED' if no changes):
		"""
		revised = self.llm.complete(prompt).text
		print("Printing the response of the reviewer agent...")
		return response if "APPROVED" in revised else revised