import asyncio
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # Set headless=True to run in headless mode
        context = await browser.new_context(
            viewport={"width": 1860, "height": 966},
            device_scale_factor=1
        )

        page = await context.new_page()
        await stealth_async(page)  # Apply stealth

        # Navigate to login page
        await page.goto("https://accounts.redbus.com/login?continue=https://www.redbus.pro/")

        # Fill username
        await page.click("#username")
        await page.fill("#username", "9748")

        # Fill password
        await page.click("#password")
        await page.fill("#password", "prasannapurple")

        # Click login and wait for navigation
        await page.click("#loginSubmit")
        await page.wait_for_url("https://accounts.redbus.com/loginsuccess?continue=https://www.redbus.pro/")

        # Click Skip button
        await page.click("text=Skip")

        # Click on task list image
        await page.click("div.DashBoard---taskListContainerOne---1wsLJ img")

        # Click "R & R"
        await page.click("#gtm_cf span")

        # Optional: keep the browser open until user presses Enter
        input("Press Enter to close browser...")
        await browser.close()

# Run the async function
asyncio.run(run())
