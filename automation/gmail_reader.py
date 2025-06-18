from googleapiclient.discovery import build
import base64
import re

def get_latest_emails(service, max_results=5):
    results = service.users().messages().list(
        userId='me',
        maxResults=max_results,
        labelIds=['INBOX'],
        q="is:unread"
    ).execute()

    messages = results.get('messages', [])
    email_data = []

    for msg in messages:
        msg_id = msg['id']
        msg_detail = service.users().messages().get(userId='me', id=msg_id, format='full').execute()
        payload = msg_detail.get("payload", {})
        headers = payload.get("headers", [])

        subject = next((h["value"] for h in headers if h["name"] == "Subject"), "No Subject")
        sender = next((h["value"] for h in headers if h["name"] == "From"), "Unknown Sender")
        date = next((h["value"] for h in headers if h["name"] == "Date"), "Unknown Date")

        # Extract plain text body
        body = get_email_body(payload)

        email_data.append({
            "id": msg_id,
            "subject": subject,
            "sender": sender,
            "date": date,
            "body": body
        })

    return email_data


def get_email_body(payload):
    def extract_parts(parts):
        for part in parts:
            mime_type = part.get("mimeType")
            body_data = part.get("body", {}).get("data", "")
            if mime_type == "text/plain" and body_data:
                return body_data
            elif part.get("parts"):
                # Recursive for nested multiparts
                nested = extract_parts(part.get("parts"))
                if nested:
                    return nested
        return None

    data = extract_parts(payload.get("parts", []))

    # Fallback if data is still None
    if not data:
        data = payload.get("body", {}).get("data", "")

    try:
        decoded_bytes = base64.urlsafe_b64decode(data.encode("UTF-8"))
        text = decoded_bytes.decode("utf-8", errors="ignore")
        return re.sub(r'\s+', ' ', text).strip()
    except Exception as e:
        print("❌ Error decoding email body:", e)
        return ""

    

