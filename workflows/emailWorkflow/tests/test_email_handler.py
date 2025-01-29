import unittest
from srcs.handlers.email_handler import EmailHandler

class TestEmailHandler(unittest.TestCase):
    def setUp(self):
        """Initialize the email handler."""
        self.email_handler = EmailHandler()

    def test_fetch_latest_email(self):
        """Test if the handler fetches emails correctly."""
        email = self.email_handler.fetch_latest_email()
        self.assertIsNotNone(email)
        self.assertIn("sender", email)
        self.assertIn("subject", email)
        self.assertIn("body", email)

if __name__ == "__main__":
    unittest.main()
