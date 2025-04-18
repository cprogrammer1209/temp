from playwright.sync_api import Playwright, sync_playwright
from playwright_stealth import stealth_sync  # use the sync version

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(locale="en-US")  # valid locale
    page = context.new_page()

    stealth_sync(page)  # stealth applied here

    page.goto("https://accounts.redbus.com/login?continue=https://www.redbus.pro/")
    page.get_by_role("textbox", name="Username").click()
    page.get_by_role("textbox", name="Username").fill("9748")
    page.get_by_role("textbox", name="Username").press("Tab")
    page.get_by_placeholder("Password").fill("prasannapurple")
    page.get_by_role("button", name="Login", exact=True).click()

    page.wait_for_timeout(10000)  # wait for UI to load or debug visually

    context.close()
    browser.close()

with sync_playwright() as playwright:
    run(playwright)
