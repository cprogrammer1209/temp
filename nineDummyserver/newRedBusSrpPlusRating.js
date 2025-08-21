const { chromium } = require("playwright");
const { convert } = require("html-to-text");
const fs = require("fs/promises");

(async () => {
  const browser = await chromium.launch({ headless: false }); // Run headful to avoid detection
  const context = await browser.newContext({
    userAgent:
      "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    viewport: { width: 1280, height: 720 },
    locale: "en-US",
  });

  const page = await context.newPage();

  await page.addInitScript(() => {
    Object.defineProperty(navigator, "webdriver", {
      get: () => false,
    });

    Object.defineProperty(navigator, "plugins", {
      get: () => [1, 2, 3, 4, 5],
    });

    Object.defineProperty(navigator, "languages", {
      get: () => ["en-US", "en"],
    });

    const getParameter = WebGLRenderingContext.prototype.getParameter;
    WebGLRenderingContext.prototype.getParameter = function (param) {
      if (param === 37445) return "Intel Inc.";
      if (param === 37446) return "Intel Iris OpenGL Engine";
      return getParameter.call(this, param);
    };
  });

  await page.goto(
    "https://accounts.redbus.com/login?continue=https://www.redbus.pro/"
  );
  await page.getByRole("textbox", { name: "Username" }).click();
  await page.getByRole("textbox", { name: "Username" }).fill("9748");
  await page.getByRole("textbox", { name: "Username" }).press("Tab");
  await page.getByRole("textbox", { name: "Password" }).click();
  await page.getByRole("textbox", { name: "Password" }).fill("prasannapurple");
  await page.getByRole("button", { name: "Login", exact: true }).click();

  await page.locator('role=button[name="Skip"]').click();

  await page.hover("aside.SideNav---sideNav---3QZiY ");

  await page.locator('role=link[name="R & R"]').click();
  // await page.click("#servicewise_tab")
  await page.waitForTimeout(5000);
  const inputSelector = 'input[placeholder="Source"]';
  await page.waitForSelector(inputSelector);
  await page.click(inputSelector);
  await page.waitForTimeout(2000);
  await page.fill(inputSelector, "Pune");
  await page.waitForTimeout(2000);
  await page
    .locator("#react-autowhatever-1 #react-autowhatever-1--item-0")
    .click();
  await page.waitForTimeout(2000);

  const inputSelector1 = 'input[placeholder="Destination"]';

  await page.waitForSelector(inputSelector1);
  await page.click(inputSelector1);
  await page.waitForTimeout(2000);
  await page.fill(inputSelector1, "Dhule");
  await page
    .locator("#react-autowhatever-1 #react-autowhatever-1--item-0")
    .click();
  await page.waitForTimeout(2000);

  const filterBtnSelector = 'button:has-text("Filter")';
  await page.waitForSelector(filterBtnSelector, { state: "visible" });
  await page.click(filterBtnSelector);
  await page.waitForTimeout(2000);

  let count = 0;
  while (count < 3) {
    count++;
    await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
    await page.waitForTimeout(1000);
  }

  await page.waitForSelector(".CardV2---card---2s3HN");
  const cards = await page.$$(".CardV2---card---2s3HN");
  console.log(`Total cards icons found: ${cards.length}`);

  for (let i = 0; i < cards.length; i++) {
    const card = cards[i];
    console.log(`\n--- Card ${i + 1} ---`);

    // Extract and print text from card
    const textContent = await card.innerText();
    console.log(textContent);

    // Click the calendar button inside the card
    const calendarButton = await card.$(".ServiceWise---calendar---22hhI");
    if (calendarButton) {

      try {
        await Promise.all([
          // Trigger the API call
          calendarButton.click(),

          // Wait for the specific API call to complete
          page.waitForResponse(
            (response) =>
              response.url().includes("/win/api/ratingsReviews/getSrpRank") &&
              response.status() === 200
          ),
        ]);

        // Wait for ranking popup
        const rankSelector = 'div[class*="RNRCalendar---rankTextDiv"]';
        await page.waitForSelector(rankSelector, { timeout: 5000 });

        const rankElements = await page.locator(rankSelector).allTextContents();
        console.log(`\nService ${i + 1} Rankings:`);
        
        rankElements.forEach((rank) => console.log(rank));

        // Close the popup RNRCalendar---closeDiv---20D9a
        await page
          .locator('div[class*="RNRCalendar---headerDiv"] >> nth=-1')
          .click();
        await page.locator("div.RNRCalendar---closeDiv---20D9a").click();
        await page.waitForTimeout(1000);
      } catch (e) {
        console.log("Popup did not appear in time.");
      }
    }
  }
 
})();
