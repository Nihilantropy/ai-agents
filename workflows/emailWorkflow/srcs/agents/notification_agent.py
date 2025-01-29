import requests
import os
from config.settings import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

class TelegramNotifier:
    def __init__(self):
        self.bot_token = TELEGRAM_BOT_TOKEN
        self.chat_id = TELEGRAM_CHAT_ID

    def send_notification(self, sender, subject, summary, email_link):
        """Send a notification via Telegram."""
        message = f"📧 *You've received a work email!*\n\n"
        message += f"**From:** {sender}\n"
        message += f"**Subject:** {subject}\n"
        message += f"**Summary:** {summary}\n"
        message += f"[View Email]({email_link})"

        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": message,
            "parse_mode": "Markdown"
        }
        
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("✅ Notification sent successfully!")
        else:
            print("❌ Failed to send notification:", response.text)
