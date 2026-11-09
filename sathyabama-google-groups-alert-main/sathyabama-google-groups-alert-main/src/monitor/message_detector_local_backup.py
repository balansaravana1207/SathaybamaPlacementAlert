
import re
from playwright.sync_api import sync_playwright

from .message_tracker import (
    initialize_database,
    is_new_message
)

from ..notifications.telegram_bot import send_notification

GROUP_URL = "https://groups.google.com/g/sathyabama-pc-2027-engg"
CHROME_URL = "http://127.0.0.1:9222"


def detect_messages():
    print("\nStarting Google Groups monitor...")

    initialize_database()

    try:
        with sync_playwright() as p:
            browser = p.chromium.connect_over_cdp(CHROME_URL)
            context = browser.contexts[0]

            page = next(
                (
                    tab for tab in context.pages
                    if "groups.google.com" in tab.url
                ),
                None
            )

            if page is None:
                print("Google Groups tab not found!")
                return

            page.goto(
                GROUP_URL,
                wait_until="domcontentloaded"
            )

            page.wait_for_timeout(5000)

            links = page.locator(
                'a[href*="/g/sathyabama-pc-2027-engg/c/"]'
            ).evaluate_all("""
                elements => elements.map(a => ({
                    title: a.innerText.trim(),
                    url: a.href
                }))
            """)

            messages = {}

            for link in links:
                match = re.search(
                    r"/c/([^/?#]+)",
                    link["url"]
                )

                if not match:
                    continue

                message_id = match.group(1)
                title = link["title"].splitlines()[0].strip()

                if len(title) < 10:
                    continue

                if title == "Sathyabama Placement":
                    continue

                messages[message_id] = {
                    "title": title,
                    "url": link["url"]
                }

            print(f"Found {len(messages)} conversations.")

            new_count = 0

            for message_id, message in messages.items():

                if is_new_message(
                    message_id,
                    message["title"],
                    message["url"]
                ):
                    new_count += 1

                    print("New announcement:", message["title"])

                    notification = (
                        "🔔 NEW COLLEGE ANNOUNCEMENT!\n\n"
                        f"📢 {message['title']}\n\n"
                        "A new message has arrived in "
                        "Sathyabama Placement Group.\n\n"
                        f"🔗 Open announcement:\n{message['url']}"
                    )

                    try:
                        send_notification(notification)
                    except Exception as error:
                        print("Telegram notification failed:", error)

            print(f"\nNew announcements: {new_count}")

            browser.close()

    except Exception as error:
        print("Monitoring error:", error)


if __name__ == "__main__":
    detect_messages()
