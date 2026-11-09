
import os
import socket
import requests
import urllib3.util.connection as urllib3_connection
from dotenv import load_dotenv

load_dotenv(".env")

# Prefer IPv4 for Telegram connections
urllib3_connection.allowed_gai_family = lambda: socket.AF_INET


def send_notification(message):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        raise ValueError("Telegram credentials are missing from .env")

    url = f"https://api.telegram.org/bot{token}/sendMessage"

    try:
        response = requests.post(
            url,
            data={"chat_id": chat_id, "text": message},
            timeout=30
        )

        result = response.json()

        if not result.get("ok"):
            raise RuntimeError(
                f"Telegram error: {result.get('description')}"
            )

        print("Notification sent successfully!")

    except requests.RequestException as error:
        print("Telegram connection failed:", type(error).__name__)
        raise


if __name__ == "__main__":
    send_notification(
        "🔔 TEST ALERT\n\nYour Sathyabama notification system is connected!"
    )
