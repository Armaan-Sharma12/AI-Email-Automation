import os
from telegram import Bot, error
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

bot = Bot(token=TELEGRAM_TOKEN)

def send_telegram_alert(message: str) -> bool:
    try:
        bot.send_message(chat_id=CHAT_ID, text=message)
        print("✅ Telegram message sent successfully.")
        return True
    except error.TelegramError as e:
        print(f"❌ Failed to send Telegram message: {e}")
        return False
