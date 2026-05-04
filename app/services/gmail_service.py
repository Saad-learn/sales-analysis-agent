import base64
from googleapiclient.discovery import build

class GmailService:
    def __init__(self, credentials):
        self.service = build("gmail", "v1", credentials=credentials)

    def list_messages(self, max_results=10):
        res = self.service.users().messages().list(
            userId="me",
            maxResults=max_results
        ).execute()
        return res.get("messages", [])

    def get_message(self, msg_id: str):
        return self.service.users().messages().get(
            userId="me",
            id=msg_id,
            format="full"
        ).execute()

    def extract_email_data(self, message):
        payload = message.get("payload", {})
        headers = payload.get("headers", [])
        subject = ""
        sender = ""
        for h in headers:
            if h.get("name") == "Subject":
                subject = h.get("value", "")
            if h.get("name") == "From":
                sender = h.get("value", "")
        body = ""
        if payload.get("parts"):
            for part in payload["parts"]:
                if part.get("mimeType") == "text/plain":
                    data = part.get("body", {}).get("data")
                    if data:
                        body = base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")
        else:
            data = payload.get("body", {}).get("data")
            if data:
                body = base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")
        return {
            "subject": subject,
            "sender": sender,
            "body": body
        }