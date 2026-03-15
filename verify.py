from playwright.sync_api import sync_playwright

def verify_pages():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # 1. Verify 2-minute timer
        page.goto("http://localhost:4321/sites/siliconbased/2-minute-timer")
        page.wait_for_selector(".timer-display")
        page.screenshot(path="/home/jules/verification/2-minute-timer.png", full_page=True)

        # 2. Verify Dark Wolf
        page.goto("http://localhost:4321/sites/siliconbased/terminal-list-dark-wolf")
        page.wait_for_selector("h1:text('The Terminal List: Dark Wolf')")
        page.screenshot(path="/home/jules/verification/dark-wolf.png", full_page=True)

        # 3. Verify The Rookie
        page.goto("http://localhost:4321/sites/siliconbased/the-rookie-episode-list")
        page.wait_for_selector("h1:text('The Rookie Episode List')")
        page.screenshot(path="/home/jules/verification/the-rookie.png", full_page=True)

        browser.close()

if __name__ == "__main__":
    import os
    os.makedirs("/home/jules/verification", exist_ok=True)
    verify_pages()
    print("Screenshots captured.")
