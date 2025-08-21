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
    // Login
    await page.goto("https://www.redbus.pro/");
    await page.fill("#username", "9748");
    await page.fill("#password", "prasannapurple");
    await page.click("#loginSubmit");
    await page.waitForTimeout(5000);

    // Close pop-up if present
    const closeIcons = await page.$$(
      'xpath=//*[name()="g" and contains(@clip-path,"url(#clip0")]'
    );
    if (closeIcons.length > 0) await closeIcons[0].click();

    // Click hamburger and scroll menu
    await page.click(".Header---ham_menu---gOm2d");
    const scrollableDiv = await page.$(
      'xpath=//body/div[@id="root"]/div/div/div/div[3]'
    );
    await page.evaluate((div) => {
      div.scrollTop = div.scrollHeight;
    }, scrollableDiv);
    await page.waitForTimeout(2000);

    // Go to R & R and hide menu
    await page.click('xpath=//span[normalize-space()="R & R"]');
    await page.mouse.click(500, 200);
    await page.waitForTimeout(3000);

    // Skip walkthrough if present
    const skipButton = await page.$(
      '//button[contains(@class,"CoachMarks---btn1") and text()="Skip"]'
    );
    if (skipButton) await skipButton.click();

    // Select 'Reviews' radio
    await page.click('input[value="Reviews"]');
    await Promise.all([
       page.waitForResponse(
        (response) =>
          response
            .url()
            .includes("/win/api/ratingsReviews/getCustomerCountsForReviewsRnR") &&
          response.status() === 200
      ),
      page.waitForResponse(
        (response) =>
          response
            .url()
            .includes("/win/api/ratingsReviews/getAllReviewsRnR/0") &&
          response.status() === 200
      ),
    ]);
   
    //enter source and destination
    // Step 5: Input Source/Destination and Apply Filter
    // await page.fill("xpath=//input[@placeholder='Source']", "Pune");
    // await page.waitForTimeout(3000);
    // await page.click("xpath=//div[contains(text(),'Pune')]");
    // await page.waitForTimeout(2000);
    // await page.fill("xpath=//input[@placeholder='Destination']", "Nagpur");
    // await page.waitForTimeout(2000);
    // await page.click("xpath=//div[contains(text(),'Nagpur')]");
    // await page.waitForTimeout(2000);
    // // await page.click("xpath=//button[normalize-space()='Filter']");
    // // await page.waitForTimeout(3000);
    // // await page.waitForResponse(
    // //   (response) =>
    // //     response.url().includes("/win/api/ratingsReviews/getAllReviewsRnR/0") &&
    // //     response.status() === 200
    // // );

    // await Promise.all([
    //   page.click('//button[normalize-space()="Filter"]'),
    //   page.waitForResponse(
    //     (response) =>
    //       response
    //         .url()
    //         .includes("/win/api/ratingsReviews/getAllReviewsRnR/0") &&
    //       response.status() === 200
    //   ),
    // ]);
    const totalReviews = await page.locator(".ReviewsFilter---totalnumber---3Xhc8")
      .textContent();
    console.log(`Total reviews found: ${totalReviews}`);
    const reviewCards = await page.locator(
      'xpath=//div[contains(@class,"CardV2---card")]'
    );

    const count = await reviewCards.count();
    console.log(`Total reviews found: ${count}`);

    for (let i = 0; i < count; i++) {
      //   const card = reviewCards[i];
      const card = reviewCards.nth(i);
      const getTextForCss = async (sel) => {
        const el = await card.$(sel);
        return el ? (await el.textContent()).trim() : "NA";
      };

      const getText = async (sel) => {
        const el = card.locator(sel);
        return (await el.count()) > 0 ? await el.first().textContent() : "NA";
      };

      const reviewerName = await getText(
        `xpath=//*[@id="reviews_${i}"]/div[1]/div[2]`
      );

      let mobileNumber = await getText(`xpath=//*[@id="reviews_${i}"]/div[4]`);
      let dateTime = await getText(`xpath=//*[@id="reviews_${i}"]/div[2]`);
      let route = await getText(`xpath=//*[@id="reviews_${i}"]/div[3]/div`);
      let rating = await getText(".ReviewsList---rating---EyAYO");
      let reviewText = await getText(".ReviewsList---modifiedReview---1xUF9");
      let postedDate = await getText(
        `.ReviewsList---reviewModifiedDate---3OmBa`
      );
      const showMore = card.locator(
        'xpath=.//span[contains(@class,"ReviewsList---showMore---")]'
      );
      if ((await showMore.count()) > 0) {
        await showMore.scrollIntoViewIfNeeded();
        await showMore.click();
        await page.waitForTimeout(500);
      }

      // Get review text
      const reviewTextElement = card.locator(
        'xpath=.//*[contains(@class,"ReviewsList---modifiedReview---")]'
      );
      if ((await reviewTextElement.count()) > 0) {
        const text = await reviewTextElement.first().textContent();
        if (text) reviewText = text.trim();
      }

      console.log(`Review ${i + 1} Details:`);
      console.log(`Name: ${reviewerName}`);
      console.log(`Mobile: ${mobileNumber}`);
      console.log(`Date & Time: ${dateTime}`);
      console.log(`Route: ${route}`);
      console.log(`Rating: ${rating}`);
      console.log(`Review Text: ${reviewText}`);
      console.log(`postedDate : ${postedDate}`);
      console.log("-----------------------------------");
    }
  } catch (e) {
    console.error("❌ Test failed:", e.message);
  } finally {
    await browser.close();
  }
}

prasannaTravelFlow();

async function scrollUntilVisible(page, targetSelector) {
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
