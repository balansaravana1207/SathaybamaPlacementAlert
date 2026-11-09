
import re
from pathlib import Path
from playwright.sync_api import sync_playwright

from .message_tracker import (
    initialize_database,
    is_new_message
)

from ..notifications.telegram_bot import send_notification


GROUP_URL = "https://groups.google.com/g/sathyabama-pc-2027-engg"
AUTH_FILE = Path("data/google_auth.json")


def detect_messages():
    print("\nStarting Google Groups cloud monitor...")

    if not AUTH_FILE.exists():
        print("ERROR: Google authentication file not found!")
        return

    initialize_database()

    try:
        # Playwright and browser share the same lifecycle
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)

            try:
                context = browser.new_context(
                    storage_state=str(AUTH_FILE)
                )

                page = context.new_page()

                page.goto(
                    GROUP_URL,
                    wait_until="domcontentloaded",
                    timeout=60000
                )

                page.wait_for_timeout(7000)

                print("Current page:", page.url)
                print("Page title:", page.title())

                if "accounts.google.com" in page.url:
                    print(
                        "ERROR: Google session expired or login required."
                    )
                    return

                # Find conversation links
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

                if not messages:
                    print(
                        "WARNING: No conversations detected. "
                        "Google Groups page may have changed."
                    )
                    return

                new_count = 0

                for message_id, message in messages.items():

                    if is_new_message(
                        message_id,
                        message["title"],
                        message["url"]
                    ):
                        new_count += 1

                        print(
                            "New announcement:",
                            message["title"]
                        )

                        notification = (
                            "NEW COLLEGE ANNOUNCEMENT!\n\n"
                            f"{message['title']}\n\n"
                            "A new message has arrived in "
                            "Sathyabama Placement Group.\n\n"
                            f"Open announcement:\n{message['url']}"
                        )

                        try:
                            send_notification(notification)

                        except Exception as error:
                            print(
                                "Telegram notification failed:",
                                error
                            )

                print(f"\nNew announcements: {new_count}")

            finally:
                browser.close()

    except Exception as error:
        print("Monitoring error:", error)


if __name__ == "__main__":
    detect_messages()
