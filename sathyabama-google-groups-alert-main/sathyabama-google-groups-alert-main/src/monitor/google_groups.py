
from playwright.sync_api import sync_playwright


def connect_to_chrome():
    print("Connecting to your Chrome browser...")

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(
            "http://127.0.0.1:9222"
        )

        print("Successfully connected to Chrome!")

        for context in browser.contexts:
            for page in context.pages:
                print("----------------------------")
                print("Page title:", page.title())
                print("Page URL:", page.url)

        browser.close()

    print("Connection test completed.")


if __name__ == "__main__":
    connect_to_chrome()
