from playwright.sync_api import sync_playwright

MESSAGE_URL = (
    "https://groups.google.com/g/"
    "sathyabama-pc-2027-engg/c/lGQcI4SqJ5Q"
)

def inspect_message():
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(
            "http://127.0.0.1:9222"
        )

        page = browser.contexts[0].new_page()
        page.goto(MESSAGE_URL, wait_until="domcontentloaded")
        page.wait_for_timeout(5000)

        for selector in [
            "main",
            '[role="main"]',
            "article"
        ]:
            locator = page.locator(selector)
            count = locator.count()

            print(f"\nSELECTOR: {selector}")
            print(f"COUNT: {count}")

            for i in range(min(count, 3)):
                text = locator.nth(i).inner_text()
                print(text[:5000])

        page.close()
        browser.close()


if __name__ == "__main__":
    inspect_message()