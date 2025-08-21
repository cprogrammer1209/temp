const { chromium } = require("playwright");

async function prasannaTravelFlow() {
  const browser = await chromium.launch({ headless: false });

  const context = await browser.newContext({});

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
  await page.waitForTimeout(1500);

  try {
    // Step 1: Login to redbus.pro
    await page.goto("https://www.redbus.pro/");
    await page.setViewportSize({ width: 1280, height: 800 });

    await page.fill("#username", "9748");
    await page.fill("#password", "prasannapurple");
    await page.waitForTimeout(1000);
    await page.click("#loginSubmit");
    await page.waitForTimeout(5000);

    // Step 2: Handle SVG Close Icon if present
    const closeIcon = await page.locator("g[clip-path*='url(#clip0']").first();
    if (await closeIcon.isVisible()) {
      await closeIcon.click();
    }

    // Step 3: Open Side Menu and click "R & R"
    await page.click(".Header---ham_menu---gOm2d");
    await page.waitForTimeout(2000);

    const scrollableDiv = await page.locator(
      "xpath=//body/div[@id='root']/div/div/div/div[3]"
    );
    await page.evaluate(
      (el) => (el.scrollTop = el.scrollHeight),
      await scrollableDiv.elementHandle()
    );
    await page.waitForTimeout(2000);

    await page.click("xpath=//span[normalize-space()='R & R']");
    await page.waitForTimeout(5000);

    // Hide menu with offset click
    await page.mouse.click(500, 200);
    await page.waitForTimeout(3000);

    // Step 4: Skip Intro Coach Mark
    const skipBtn = page.locator(
      "xpath=//button[contains(@class,'CoachMarks---btn1') and text()='Skip']"
    );
    if ((await skipBtn.count()) > 0 && (await skipBtn.first().isVisible())) {
      await skipBtn.first().click();
      console.log("Skip button clicked.");
    }

    // Step 5: Input Source/Destination and Apply Filter
    await page.fill("xpath=//input[@placeholder='Source']", "Pune");
    await page.waitForTimeout(3000);
    await page.click("xpath=//div[contains(text(),'Pune')]");
    await page.waitForTimeout(2000);
    await page.fill("xpath=//input[@placeholder='Destination']", "Nagpur");
    await page.waitForTimeout(2000);
    await page.click("xpath=//div[contains(text(),'Nagpur')]");
    await page.waitForTimeout(2000);
    await page.click("xpath=//button[normalize-space()='Filter']");
    await page.waitForTimeout(3000);

    // Step 6: Extract Data
    await page.waitForSelector("xpath=//span[contains(text(),'View trend')]");

    try {
      const targetSelector = ".ServiceWise---noScroll---2s4RK";
      await scrollUntilVisible(page, targetSelector);
    } catch (e) {
      console.error("Error scrolling to target:", e.message);
      
    }
    const serviceCards = await page.$$(
      "xpath=//div[contains(@class,'CardV2---card')]"
    );
    console.log(`Total services found: ${serviceCards.length}`);
    const count = serviceCards.length;
    for (let i = 0; i < count; i++) {
      const card = serviceCards[i]; // <-- Use array indexing

      try {
        const getText = async (card, selector) => {
          // Use page.locator with card's element handle as the parent
          const element = await card.$(selector);
          return element
            ? (await (await element.getProperty('textContent')).jsonValue()).trim()
            : "NA";
        };

        const arrivalTime = await getText(
          card,
          "span[style*='text-align: left']"
        );
        const rating = await getText(card, "span[class*='Sub_Rated_space']");

        console.log(`\nService ${i + 1} Arrival Time: ${arrivalTime}`);
        console.log(`Service ${i + 1} Rating: ${rating}`);

        // Click calendar icon
        const calendarIcons = await page.$$(
          "xpath=//img[contains(@alt,'calendar')]"
        );
        if (calendarIcons[i]) {
          await calendarIcons[i].click();

          // Wait for rank popup
          await page.waitForSelector(
            "xpath=//div[contains(@class,'RNRCalendar---rankTextDiv')]",
            { timeout: 5000 }
          );

          let todayRank = "NA";
          let outOf = "NA";

          const todayRankElem = await page.$("xpath=(//div[contains(@class,'rankTextDiv')])[1]");
          if (todayRankElem) {
            todayRank = (await todayRankElem.textContent())?.trim() || "NA";
          }

          const outOfElem = await page.$("xpath=(//div[contains(@class,'totalTextDiv')])[1]");
          if (outOfElem) {
            outOf = (await outOfElem.textContent())?.trim() || "NA";
          }

          console.log(`Service ${i + 1} Today's Rank: ${todayRank} ${outOf}`);

          // Close popup
          const closeButton = await page.locator(
            "xpath=//div[contains(@class,'RNRCalendar---headerDiv')]/div[last()]"
          );
          await closeButton.click();
          await page.waitForTimeout(1500);
        }
      } catch (err) {
        console.log(`Error in Service ${i + 1}: ${err.message}`);
      }
    }
  } catch (e) {
    console.error("❌ Test failed:", e.message);
  } finally {
    await browser.close();
  }
}

prasannaTravelFlow();


async function scrollUntilVisible(page,targetSelector) {
  const maxScrolls = 50;
  const scrollDelay = 500;
  let found = false;

  for (let i = 0; i < maxScrolls; i++) {
    const element = await page.$(targetSelector);
    if (element) {
      // Ensure it's visible in viewport
      const isVisible = await element.isVisible();
      if (isVisible) {
        console.log("Element is visible");
        found = true;
        break;
      }
    }

    // Scroll down
    await page.evaluate(() => {
      window.scrollBy(0, window.innerHeight);
    });

    await page.waitForTimeout(scrollDelay);
  }

  if (!found) {
    throw new Error(`Element '${targetSelector}' not found after scrolling`);
  }
}
