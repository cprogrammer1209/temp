const { chromium } = require("playwright");

async function readUserReview() {
  const browser = await chromium.launch({ headless: false });

  const context = await browser.newContext({});

  const page = await context.newPage();
  try {
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

    // Login
    await page.goto("https://www.redbus.pro/");
    await page.fill("#username", "9748");
    await page.fill("#password", "prasannapurple");
    await page.waitForTimeout(1000);
    await page.click("#loginSubmit");
    await page.waitForTimeout(5000);

    const closeIcon = page.locator(".QuickFundBanner---cross---2Mp_5");

    if (await closeIcon.isVisible()) {
      await closeIcon.click();
    }
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
            .includes(
              "/win/api/ratingsReviews/getCustomerCountsForReviewsRnR"
            ) && response.status() === 200
      ),
    ]);

    let customerReviews = [];
    try {
      let totalReviews = await page
        .locator(".ReviewsFilter---totalnumber---3Xhc8")
        .textContent();
      console.log(`Total reviews text: ${totalReviews}`);

      if (totalReviews) {
        totalReviews = totalReviews.replace(/[^0-9,]/g, "");
        console.log(`Total reviews after cleaning: ${totalReviews}`);
        totalReviews = parseInt(totalReviews.replace(/,/g, ""));
        let totalScrolls = Math.ceil(totalReviews / 50);
        for (let i = 0; i < totalScrolls; i++) {
          console.log(`Scrolling for page ${i}...`);
          let options = {
            filterBy: {
              opId: "9748",
              country: "IND",
              srcId: null,
              destId: null,
              bpId: null,
              dpId: null,
              startDateInLong: new Date().getTime() - 8 * 24 * 60 * 60 * 1000,
              endDateInLong: new Date().getTime(),
              routeId: null,
              ratingRange: null,
              reviewAvailable: true,
              tagsAvailable: null,
              oprReplyToReviewsAvailable: null,
              redProWinEmailStatus: null,
              moderatorStatus: null,
              PNR: null,
              UUID: null,
              isUnrated: false,
              IsAcknowledgementSent: null,
              IsReminderSentSch: null,
            },
            sortBy: {
              ratings: null,
              DOJ: true,
              RatingSubmittedDate: null,
              ReviewModifiedDate: null,
            },
            orderBy: {
              order: "DESC",
            },
            CountValue: false,
          };
          let postData = {
            options: options,
            pageNumber: i,
          };
          const apiResponse = await page.evaluate(async (postData, i) => {
            const response = await fetch(
              `https://www.redbus.pro/win/api/ratingsReviews/getAllReviewsRnR/${postData.pageNumber}`,
              {
                method: "POST",
                headers: {
                  "Content-Type": "application/json",
                  Accept: "application/json",
                },
                credentials: "include", // sends cookies
                body: JSON.stringify(postData.options),
              }
            );

            const data = await response.json(); // or response.text() for plain text
            return data;
          }, postData);

          console.log(`Scrolled for page ${i}`, apiResponse.length);
          if (apiResponse && apiResponse.length > 0) {
            customerReviews.push(...apiResponse);
          } else {
            console.log(`No reviews found for page ${i}`);
          }
        }
      }
    } catch (e) {
      console.error("Error during scrolling:", e.message);
      return [];
    }

    console.log(`Total reviews collected so far: ${customerReviews.length}`);
    if (customerReviews.length == 0) {
      throw new Error("No reviews found after scrolling");
    }

    let customerReviewObjects = customerReviews.map((review) => {
      return {
        customerName: review.CustomerName,
        customerReview: review.ReviewModified,
        reviewPostedDate: new Date(
          new Date(review.ReviewSubmitTime).getTime() + 5.5 * 60 * 60 * 1000
        ),
        journeyDate: new Date(
          new Date(review.DOJInLocal).getTime() + 5.5 * 60 * 60 * 1000
        ),
        Mobile: review.Mobile,
        PNR: review.Pnr,
        rating: review.OverallRatings.oldRating,
        journeySRC: review.SrcName,
        journeyDST: review.DstName,
        TIN: review.TIN,
      };
    });

    console.log(
      "type of reviewPostedDate ",
      typeof customerReviewObjects[0].reviewPostedDate
    );

    const yesterday = new Date();
    yesterday.setDate(yesterday.getDate() - 1);

    // Create a string like '2025-06-25' for comparison
    const targetDateStr = yesterday.toISOString().split("T")[0];

    const filteredReviews = customerReviewObjects.filter((review) => {
      const reviewDateStr = new Date(review.reviewPostedDate)
        .toISOString()
        .split("T")[0];
      return reviewDateStr === targetDateStr;
    });

    let replyOptions = {
      reply:
        "We always try to provide the best service for our customer.Do give us another chance as we work to implement your feedback. ",
      tin: "TU8N53326324",
      travelsName: "Prasanna Purple Mobility Solutions Pvt Ltd",
    };

    const replyResponse = await page.evaluate(async (replyOptions) => {
      const response = await fetch(
        `https://www.redbus.pro/win/api/ratingsReviews/replyToReviewPreModeration`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Accept: "application/json",
          },
          credentials: "include", // sends cookies
          body: JSON.stringify(replyOptions),
        }
      );

      const data = await response.json(); // or response.text() for plain text
      return data;
    }, replyOptions);

    return filteredReviews;
  } catch (e) {
    console.error(" Test failed:", e.message);
    return [];
  } finally {
    await browser.close();
  }
}

readUserReview()
  .then((reviews) => {
    console.log("Reviews collected:", reviews);
  })
  .catch((error) => {
    console.error("Error in reading user reviews:", error);
  });
