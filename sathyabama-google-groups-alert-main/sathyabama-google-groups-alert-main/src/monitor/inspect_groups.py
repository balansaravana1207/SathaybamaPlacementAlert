
from playwright.sync_api import sync_playwright

GROUP_URL = "https://groups.google.com/g/sathyabama-pc-2027-engg"


def inspect_group():
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(
            "http://127.0.0.1:9222"
        )

        context = browser.contexts[0]
        page = next(
            (tab for tab in context.pages
             if "groups.google.com/g/" in tab.url),
            None
        )

        if page is None:
            print("Google Groups tab not found!")
            return

        page.goto(GROUP_URL, wait_until="domcontentloaded")
        page.wait_for_timeout(5000)

        print("\n===== MESSAGE LINK ANALYSIS =====")

        links = page.locator("a").evaluate_all("""
            elements => elements.map(a => ({
                text: a.innerText.trim(),
                href: a.href,
                aria: a.getAttribute('aria-label')
            })).filter(a =>
                a.text.length > 15 &&
                a.href.includes('/g/sathyabama-pc-2027-engg')
            )
        """)

        for index, link in enumerate(links, 1):
            print(f"\nMESSAGE CANDIDATE {index}")
            print("Title:", link["text"][:200])
            print("URL:", link["href"])
            print("Label:", link["aria"])

        print("\nTotal candidates:", len(links))
        print("===== ANALYSIS COMPLETED =====")


if __name__ == "__main__":
    inspect_group()
