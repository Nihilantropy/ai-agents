import unittest
from srcs.agents.notification_agent import TelegramNotifier

class TestTelegramNotifier(unittest.TestCase):
    def setUp(self):
        """Initialize Telegram notifier."""
        self.notifier = TelegramNotifier()

    def test_send_notification(self):
        """Test sending a Telegram message."""
        result = self.notifier.send_notification(
            sender="boss@company.com",
            subject="Meeting Reminder",
            summary="Reminder about our meeting at 3 PM.",
            email_link="https://mail.google.com/mail/u/0/#inbox/"
        )
        self.assertTrue(result)  # Expect a success response

if __name__ == "__main__":
    unittest.main()
