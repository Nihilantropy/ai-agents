from srcs.llm.model import LLMModel
from srcs.rag.index import build_index
from config.settings import WORK_EMAILS_FILE

class EmailClassifier:
    def __init__(self, model: LLMModel):
        self.model = model
        self.index = build_index()  # Load the RAG index
        self.work_senders = self._load_work_email_senders()

    def _load_work_email_senders(self):
        """Load known work-related email senders."""
        try:
            with open(WORK_EMAILS_FILE, "r") as f:
                return set(line.strip() for line in f.readlines())
        except FileNotFoundError:
            print("⚠️ work_emails.txt not found. Using RAG + LLM only.")
            return set()

    def is_work_email(self, sender: str, subject: str, body: str) -> bool:
        """Determine if an email is work-related using RAG + LLM."""
        if sender in self.work_senders:
            return True  

        # 🔍 Query RAG index for similar work-related emails
        query_text = f"Subject: {subject}\nBody: {body}"
        query_response = self.index.as_retriever().retrieve(query_text)

        # 📌 Only accept results with high relevance scores
        if query_response and len(query_response) > 0:
            if query_response[0].score > 0.7:  # Adjust score threshold
                print("📌 RAG confirms work email.")
                return True  

        # 🤖 Fallback: Use LLM
        print("🤖 LLM classifying email...")
        prompt = (
            f"Classify this email strictly:\n\n"
            f"Subject: {subject}\n"
            f"Body: {body[:500]}\n\n"
            f"Reply only with one number: (1) Work, (2) Non-Work, (3) Spam."
        )
        response = self.model.generate_text(prompt)

        return "1" in response  # Expect strict classification
