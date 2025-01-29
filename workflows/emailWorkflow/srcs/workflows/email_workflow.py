from srcs.handlers.email_handler import EmailHandler
from srcs.agents.email_classifier import EmailClassifier
from srcs.agents.notification_agent import NotificationAgent
from srcs.llm.model import LLMModel

def emailWorkflow():
    """Entrypoint for the AI workflow."""
    email_handler = EmailHandler()
    model = LLMModel()
    classifier = EmailClassifier(model)
    notifier = NotificationAgent()

    # Fetch the latest email
    email = email_handler.fetch_latest_email()
    if not email:
        print("No new emails found.")
        return

    sender, subject, body = email["sender"], email["subject"], email["body"]

    # Classify email
    if classifier.is_work_email(sender, subject, body):
        summary = model.generate_text(f"Summarize this email:\n\n{body}")
        email_link = f"https://mail.google.com/mail/u/0/#inbox/{email['id']}"
        notifier.send_notification(sender, subject, summary, email_link)

### ENTRYPOINT ###
if __name__ == "__main__":
    emailWorkflow()
