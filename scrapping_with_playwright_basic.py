from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    # ১. ব্রাউজার ওপেন
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    # ২. সাইটে যাওয়া
    page.goto("https://www.wikipedia.org")

    # ৩. সার্চ করা
    search_input = page.locator("input[name='search']")
    search_input.fill("Python (programming language) for AI")
    search_input.press("Enter")

    # ৪. রেজাল্ট লোড হওয়া পর্যন্ত অপেক্ষা (প্রথম হেডিং এর জন্য)
    page.wait_for_selector("h1")

    # ৫. ডাটা কালেক্ট করা
    title = page.locator("h1").inner_text()
    print(f"Page Title: {title}")

    # ৬. স্ক্রিনশট
    page.screenshot(path="wiki_python.png")

    # ৭. বন্ধ করা
    browser.close()
    