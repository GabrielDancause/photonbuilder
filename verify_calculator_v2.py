from playwright.sync_api import sync_playwright, expect

def test_calculator(page):
    # Navigate to the calculator page
    page.goto('http://localhost:4321/sites/siliconbased/calculator')

    # Check title
    expect(page.locator('h1')).to_have_text('Scientific Calculator')

    # Check calculator visibility (not covered by nav)
    calc = page.locator('.calculator')
    expect(calc).to_be_visible()

    # Check if top row buttons are visible and clickable
    ac_btn = page.locator('button:has-text("AC")')
    expect(ac_btn).to_be_visible()
    ac_btn.click()

    # Test calculation: (5 + 3) * 2 = 16
    page.click('button[data-op="("]')
    page.click('button:has-text("5")')
    page.click('button[data-op="+"]')
    page.click('button:has-text("3")')
    page.click('button[data-op=")"]')
    page.click('button[data-op="*"]')
    page.click('button:has-text("2")')
    page.click('button[data-action="calculate"]')

    display = page.locator('#calc-display')
    expect(display).to_have_text('16')

    # Test sin(90) in DEG mode
    page.click('button:has-text("AC")')
    # Ensure DEG mode
    deg_btn = page.locator('button#deg-btn')
    deg_btn.click()
    page.click('button:has-text("9")')
    page.click('button:has-text("0")')
    page.click('button[data-func="sin"]')
    expect(display).to_have_text('1')

    # Take screenshot
    page.screenshot(path='/home/jules/verification/calculator_fixed_v2.png', full_page=True)

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            test_calculator(page)
            print("Verification successful")
        except Exception as e:
            print(f"Verification failed: {e}")
            page.screenshot(path='/home/jules/verification/failure.png')
        finally:
            browser.close()
