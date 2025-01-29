from googleapiclient.discovery import build
from google.oauth2 import service_account
import base64
from config.settings import GMAIL_CREDENTIALS_FILE, GMAIL_SCOPES

class EmailHandler:
    def __init__(self):
        """Initialize Gmail API service."""
        creds = service_account.Credentials.from_service_account_file(
            GMAIL_CREDENTIALS_FILE, scopes=GMAIL_SCOPES
        )
        self.service = build("gmail", "v1", credentials=creds)

    def fetch_latest_email(self):
        """Fetch the latest email from the inbox."""
        results = self.service.users().messages().list(userId="me", maxResults=1).execute()
        messages = results.get("messages", [])

        if not messages:
            return None

        msg_id = messages[0]["id"]
        msg = self.service.users().messages().get(userId="me", id=msg_id).execute()

        email_data = {
            "id": msg_id,
            "sender": "",
            "subject": "",
            "body": ""
        }

        for header in msg["payload"]["headers"]:
            if header["name"] == "From":
                email_data["sender"] = header["value"]
            elif header["name"] == "Subject":
                email_data["subject"] = header["value"]

        # Decode email body
        if "parts" in msg["payload"]:
            for part in msg["payload"]["parts"]:
                if part["mimeType"] == "text/plain":
                    email_data["body"] = base64.urlsafe_b64decode(part["body"]["data"]).decode("utf-8")

        return email_data
