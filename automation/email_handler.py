import os
import json
import datetime
from dotenv import load_dotenv

from automation.gmail_reader import get_latest_emails
from automation.gmail_actions import send_auto_reply, save_draft, delete_email
from classification.cohere_classifier import classify_email
from telegram_bot_module.telegram_bot import send_telegram_alert
from Integrations.google_calendar import add_event_to_calendar
from auth.gmail_auth import get_gmail_service

# Load environment variables
load_dotenv()

# Path to store metadata
EMAILS_JSON = os.path.join(os.path.dirname(__file__), '..', 'emails.json')

def save_email_metadata(data: dict):
    """Append processed email metadata to emails.json."""
    try:
        if os.path.exists(EMAILS_JSON):
            with open(EMAILS_JSON, 'r', encoding='utf-8') as f:
                existing = json.load(f)
        else:
            existing = []
    except json.JSONDecodeError:
        existing = []

    existing.append(data)
    with open(EMAILS_JSON, 'w', encoding='utf-8') as f:
        json.dump(existing, f, ensure_ascii=False, indent=2)

def fetch_emails():
    service = get_gmail_service()
    emails = get_latest_emails(service)

    for email in emails:
        msg_id = email.get('id')
        subject = email.get('subject', '(No Subject)')
        sender = email.get('sender', '(Unknown Sender)')
        body = email.get('body', '')
        received_at = email.get('date', datetime.datetime.utcnow().isoformat() + "Z")

        sender_email = sender.split('<')[-1].strip('> ') if '<' in sender else sender

        result = classify_email(subject, body)
        if result is None:
            print(f"⚠️ Skipping email {msg_id}, classification failed.")
            continue

        print(f"\n📩 Processing Email from {sender_email} | Subject: {subject}")
        print("🧠 Classification Result:", result)

        action = 'none'

        # 📛 Junk
        if result.get('is_junk'):
            delete_email(service, msg_id)
            action = 'deleted'

        # 📅 Calendar
        elif result.get('has_deadline') and result.get('deadline') and result['deadline'] != 'null':
            add_event_to_calendar(subject, 'Auto-added from email', result['deadline'])

        # ✉️ Draft or Auto-reply
        if result.get('should_draft'):
            save_draft(service, sender_email, f"Re: {subject}", result.get('suggested_reply', ''))
            action = 'drafted'
        elif result.get('is_important') and result.get('suggested_reply'):
            send_auto_reply(service, sender_email, f"Re: {subject}", result.get('suggested_reply'))
            action = 'auto_replied'

        # 📲 Telegram Notification
        if result.get('is_important'):
            send_telegram_alert(f"📬 Important Email:\nFrom: {sender_email}\nSubject: {subject}")

        # 💾 Save email metadata
        save_email_metadata({
            'id': msg_id,
            'subject': subject,
            'sender': sender_email,
            'received_at': received_at,
            'body_preview': body[:200],
            'classification': result,
            'action': action,
            'processed_at': datetime.datetime.utcnow().isoformat() + "Z"
        })

    print("\n✅ All emails processed and saved to emails.json.")
