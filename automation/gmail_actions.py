import base64
import os
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from auth.gmail_auth import get_gmail_service


def create_message(to, subject, body):
    message = MIMEText(body)
    message['to'] = to
    message['subject'] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {'raw': raw}


def send_auto_reply(service, to, subject, body):
    message = create_message(to, subject, body)
    sent = service.users().messages().send(userId="me", body=message).execute()
    print("📤 Auto-reply sent, ID:", sent['id'])


def save_draft(service, to, subject, body):
    message = create_message(to, subject, body)
    draft = service.users().drafts().create(userId="me", body={'message': message}).execute()
    print("💾 Draft saved, ID:", draft['id'])


def delete_email(service, msg_id):
    service.users().messages().delete(userId='me', id=msg_id).execute()
    print(f"🗑️ Deleted email ID: {msg_id}")


def extract_email_headers(message_payload):
    headers = message_payload.get("payload", {}).get("headers", [])
    subject = next((h["value"] for h in headers if h["name"] == "Subject"), "")
    sender = next((h["value"] for h in headers if h["name"] == "From"), "")
    return subject, sender


def get_sender_email(sender_str):
    # Handles formats like "Name <email@example.com>"
    import re
    match = re.search(r'<(.*?)>', sender_str)
    return match.group(1) if match else sender_str.strip()


# Optional helper to call all functions cleanly
def handle_email_action(service, email_id, classification, subject, sender, reply_text):
    sender_email = get_sender_email(sender)

    if classification['is_junk']:
        delete_email(service, email_id)

    elif classification['is_important'] and not classification['should_draft']:
        send_auto_reply(service, sender_email, f"Re: {subject}", reply_text)

    elif classification['should_draft']:
        save_draft(service, sender_email, f"Re: {subject}", reply_text)
