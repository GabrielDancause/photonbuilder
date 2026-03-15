from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # Options Profit Calculator
        page.goto('http://localhost:4321/sites/westmount/options-profit-calculator')
        page.wait_for_timeout(2000)
        page.screenshot(path='options-fixed.png', full_page=True)

        # Position Size Calculator
        page.goto('http://localhost:4321/sites/westmount/position-size-calculator')
        page.wait_for_timeout(2000)
        page.screenshot(path='position-fixed.png', full_page=True)

        browser.close()

if __name__ == '__main__':
    run()
