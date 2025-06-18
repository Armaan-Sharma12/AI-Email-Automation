import asyncio
from automation.email_handler import fetch_emails
from classification.cohere_classifier import classify_email
from telegram_bot_module.telegram_bot import send_telegram_alert
from automation.gmail_actions import delete_email, send_auto_reply, save_draft
from automation.gmail_reader import get_email_body
from Integrations.google_calendar import add_event_to_calendar

async def process_emails():
    emails = await fetch_emails()
    if not emails:
        print("⚠️ No emails returned. Skipping processing.")
        return

    for idx, msg in enumerate(emails, 1):
        subject = msg.get("subject")
        sender = msg.get("sender")  # corrected key from 'from' to 'sender'
        date = msg.get("date")
        message_id = msg.get("id")
        body = msg.get("body")

        print(f"\n📧 Email {idx}")
        print(f"Subject: {subject}")
        print(f"From: {sender}")
        print(f"Date: {date}")
        print(f"Body: ...")

        result = classify_email(subject, body)

        if result is None:
            print("❌ Skipping email due to classification failure.")
            continue

        print("🧠 AI Classification Result:\n", result)

        # 1. Junk email → delete
        if result.get("is_junk"):
            delete_email(message_id)
            print("🗑️ Junk email deleted.")
            continue

        # 2. Has deadline → Add to Google Calendar
        if result.get("has_deadline") and result.get("deadline") and result.get("deadline") != "null":
            add_event_to_calendar(subject, result.get("deadline"))
            print("📅 Deadline added to Google Calendar.")

        # 3. Important and should_draft is False → Auto-reply
        if result.get("is_important") and not result.get("should_draft"):
            send_auto_reply(message_id, sender, result.get("suggested_reply"))
            print("✉️ Auto-reply sent.")

        # 4. should_draft is True → Save as draft
        elif result.get("should_draft"):
            save_draft(sender, subject, result.get("suggested_reply"))
            print("💾 Suggested reply saved as draft.")

        # 5. Send Telegram alert (sync call)
        alert_message = (
            f"📬 Email Alert:\n"
            f"Subject: {subject}\n"
            f"From: {sender}\n"
            f"Date: {date}\n\n"
            f"Classification:\n{result}"
        )
        send_telegram_alert(alert_message)
        print("✅ Telegram alert sent successfully.")

if __name__ == "__main__":
    asyncio.run(process_emails())
