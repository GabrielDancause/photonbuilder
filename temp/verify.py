from playwright.sync_api import sync_playwright
import os

def verify_feature(page):
    # Navigate to local dev server URL
    url = "http://localhost:4322/sites/28grams/best-coffee-beans"
    print(f"Navigating to {url}")
    page.goto(url)
    page.wait_for_timeout(500)

    # Scroll down to capture the content
    page.evaluate("window.scrollTo(0, document.body.scrollHeight / 3)")
    page.wait_for_timeout(500)

    page.screenshot(path="/app/temp/screenshot.png", full_page=True)
    page.wait_for_timeout(1000)

if __name__ == "__main__":
    os.makedirs("/app/temp/video", exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(record_video_dir="/app/temp/video")
        page = context.new_page()
        try:
            verify_feature(page)
        finally:
            context.close()
            browser.close()