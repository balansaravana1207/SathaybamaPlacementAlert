from playwright.sync_api import sync_playwright

CHROME_URL = "http://127.0.0.1:9222"


def extract_message(message_url):

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CHROME_URL)

        page = browser.contexts[0].new_page()

        page.goto(
            message_url,
            wait_until="domcontentloaded"
        )

        page.wait_for_timeout(4000)

        content = page.locator(
            '[role="main"]'
        ).inner_text()

        page.close()
        browser.close()

        return content


if __name__ == "__main__":

    test_url = (
        "https://groups.google.com/g/"
        "sathyabama-pc-2027-engg/c/lGQcI4SqJ5Q"
    )

    message = extract_message(test_url)

    print("\nEXTRACTED ANNOUNCEMENT:\n")
    print(message)