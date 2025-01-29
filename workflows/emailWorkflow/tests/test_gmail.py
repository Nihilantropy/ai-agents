from googleapiclient.discovery import build
from google.oauth2 import service_account

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
SERVICE_ACCOUNT_FILE = "config/service_account.json"

def test_gmail_api():
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    service = build("gmail", "v1", credentials=creds)
    
    try:
        results = service.users().messages().list(userId="me", maxResults=1).execute()
        print("✅ Gmail API is working.")
    except Exception as e:
        print("❌ Gmail API Error:", e)

test_gmail_api()