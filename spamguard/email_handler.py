import base64
import os
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

from gui import routed_mails, blocked_spams  # Import the lists from gui.py

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

SOURCE_EMAIL = "cartnow.1@gmail.com"

DEPARTMENT_EMAILS = {
    "support": "suprt.cartnow@gmail.com",
    "sales": "sales.cartnow1@gmail.com",
    "tech": "tech.cartnow1@gmail.com"
}

# Authenticate with Gmail
def authenticate_gmail():
    current_dir = os.path.dirname(__file__)
    creds_path = os.path.join(current_dir, "credentials.json")
    flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
    creds = flow.run_local_server(port=0)
    service = build('gmail', 'v1', credentials=creds)
    return service

# Create message
def create_message(to, subject, message_text):
    message = MIMEText(message_text)
    message['to'] = to
    message['subject'] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes())
    return {'raw': raw.decode()}

# Send message
def send_message(service, user_id, message):
    service.users().messages().send(userId=user_id, body=message).execute()

# Classify email based on subject and body
def classify_email(subject, body):
    text = f"{subject.lower()} {body.lower()}"

    spam_keywords = [
        "win", "prize", "lottery", "bitcoin", "claim now", "free offer",
        "click here", "buy now", "cheap deals", "investment opportunity",
        "limited offer", "miracle", "guaranteed income", "easy money",
        "gift card", "reward now", "exclusive deal","free","gift"
    ]

    support_keywords = [
        "login issue", "account access", "refund", "payment", "billing",
        "support", "complaint", "order issue", "delivery problem",
        "cancel order", "subscription", "service", "warranty", "damaged"
    ]

    sales_keywords = [
        "pricing", "quotation", "purchase", "buy", "discount", "deal",
        "sales inquiry", "product inquiry", "product features",
        "quote", "bulk order", "wholesale", "price list"
    ]

    tech_keywords = [
        "bug", "error", "technical issue", "crash", "glitch", "server down",
        "troubleshooting", "network issue", "connectivity",
        "system failure", "api error", "timeout", "dashboard issue"
    ]

    priority_keywords = {
        "high": ["urgent", "immediate", "asap", "critical", "important"],
        "medium": ["reminder", "follow up", "pending", "waiting"],
        "low": ["suggestion", "feedback", "query", "information"]
    }

    # Spam logic ONLY if no department keywords are matched
    if any(word in text for word in spam_keywords):
        if not any(word in text for word in support_keywords + sales_keywords + tech_keywords):
            return "spam", "low"

    for word in tech_keywords:
        if word in text:
            for level, keys in priority_keywords.items():
                if any(k in text for k in keys):
                    return "tech", level
            return "tech", "low"

    for word in sales_keywords:
        if word in text:
            for level, keys in priority_keywords.items():
                if any(k in text for k in keys):
                    return "sales", level
            return "sales", "low"

    for word in support_keywords:
        if word in text:
            for level, keys in priority_keywords.items():
                if any(k in text for k in keys):
                    return "support", level
            return "support", "low"

    return "support", "low"


# Process unread emails
def process_emails():
    service = authenticate_gmail()
    results = service.users().messages().list(userId='me', labelIds=['INBOX'], q="is:unread").execute()
    messages = results.get('messages', [])

    for msg in messages:
        msg_data = service.users().messages().get(userId='me', id=msg['id']).execute()
        headers = msg_data['payload']['headers']
        subject = ''
        sender = ''
        for header in headers:
            if header['name'] == 'Subject':
                subject = header['value']
            elif header['name'] == 'From':
                sender = header['value']

        # Extract body
        body = ''
        if 'parts' in msg_data['payload']:
            for part in msg_data['payload']['parts']:
                if part['mimeType'] == 'text/plain' and 'data' in part['body']:
                    body = base64.urlsafe_b64decode(part['body']['data']).decode()
        elif 'body' in msg_data['payload'] and 'data' in msg_data['payload']['body']:
            body = base64.urlsafe_b64decode(msg_data['payload']['body']['data']).decode()

        # 🔒 Skip mails from Google
        if "google.com" in sender.lower():
            print(f"[SKIPPED SYSTEM MAIL] From: {sender} | Subject: {subject}")
            service.users().messages().modify(
                userId='me',
                id=msg['id'],
                body={'removeLabelIds': ['UNREAD']}
            ).execute()
            continue

        # Classify
        department, priority = classify_email(subject, body)

        if department == "spam":
            blocked_spams.append(f"SPAM Blocked | From: {sender} | Subject: {subject}")
            print(f"[SPAM BLOCKED] From: {sender} | Subject: {subject}")
            service.users().messages().modify(
                userId='me',
                id=msg['id'],
                body={'removeLabelIds': ['INBOX'], 'addLabelIds': ['SPAM']}
            ).execute()
        else:
            target_email = DEPARTMENT_EMAILS.get(department, DEPARTMENT_EMAILS['support'])

            # Clean structured forwarded message
            reply_body = (
                f"Forwarded message:\n"
                f"From: {sender}\n"
                f"Subject: {subject}\n"
                f"Department: {department.upper()}\n"
                f"Priority: {priority.upper()}\n\n"
                f"{body}"
            )

            msg_to_send = create_message(target_email, f"FWD: {subject}", reply_body)
            send_message(service, 'me', msg_to_send)

            routed_mails.append(
                f"ROUTED | From: {sender} | To Department: {department.upper()} | Subject: {subject} | Priority: {priority.upper()}"
            )
            print(f"[FORWARDED to {department.upper()} ({priority.upper()})] From: {sender} | Subject: {subject}")

        # ✅ Mark email as read
        service.users().messages().modify(
            userId='me',
            id=msg['id'],
            body={'removeLabelIds': ['UNREAD']}
        ).execute()
