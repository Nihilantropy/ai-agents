import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Gmail API Settings
GMAIL_SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
GMAIL_CREDENTIALS_FILE =  os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

# Telegram API Settings
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# LLM Model
LLM_MODEL_NAME = "deepseek-r1:7b"

# Work Email List (Path)
WORK_EMAILS_FILE = "data/docs/work_emails.txt"

RAG_DATA_DIR = "data/docs/"
