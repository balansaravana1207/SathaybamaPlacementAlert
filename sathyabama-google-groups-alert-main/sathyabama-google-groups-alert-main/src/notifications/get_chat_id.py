import os
import requests
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("TELEGRAM_BOT_TOKEN")

print("Checking Telegram bot token...")

if not token:
    print("ERROR: Bot token not found in .env")
else:
    print("Token loaded successfully!")

    url = f"https://api.telegram.org/bot{token}/getUpdates"

    response = requests.get(url, timeout=15)

    print("\nTelegram response:")
    print(response.json())