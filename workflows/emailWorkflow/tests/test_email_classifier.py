import unittest
from srcs.agents.email_classifier import EmailClassifier
from srcs.llm.model import LLMModel

class TestEmailClassifier(unittest.TestCase):
	def setUp(self):
		"""Initialize classifier for testing."""
		self.model = LLMModel()
		self.classifier = EmailClassifier(self.model)

	def test_work_email_by_sender(self):
		"""Test if known work sender is classified correctly."""
		result = self.classifier.is_work_email("claudio.rea@cliccaqui.org", "Project Update", "Please review the report.")
		self.assertTrue(result)

	def test_work_email_by_rag(self):
		"""Test if RAG correctly classifies work emails based on index."""
		result = self.classifier.is_work_email("unknown@gmail.com", "Financial Report", "Quarterly financial summary.")
		self.assertTrue(result)  # Expect it to be classified as work-related

	def test_non_work_email(self):
		"""Test if non-work emails are classified correctly."""
		result = self.classifier.is_work_email("random@spam.com", "Win a Free iPhone!", "Click this link to claim your prize!")
		self.assertFalse(result)

if __name__ == "__main__":
	unittest.main()
