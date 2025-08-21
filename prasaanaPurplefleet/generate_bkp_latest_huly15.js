const express = require("express");
const bodyParser = require("body-parser");
const cors = require("cors");
const path = require("path");
const fs = require("fs/promises");
const { chromium } = require("playwright");

const axios = require("axios");
const { MongoClient, ObjectId } = require("mongodb");
const uriSrc =
  "mongodb://staging:stage789@172.168.1.19:27017/?authSource=aiqod-staging"; //stage
const client1 = new MongoClient(uriSrc);
const { GoogleGenAI } = require("@google/genai");
const ai = new GoogleGenAI({
  apiKey: "AIzaSyBxWGfT94b1dScgtTm1lzlUSdNUKH1CK6U",
});

const app = express();
const PORT = 3000;

// Middleware
app.use(bodyParser.json({ limit: "10mb" })); // Allows sending large HTML content
app.use(cors()); // Enable CORS for external requests

app.post("/scrapper/testing", async (req, res) => {
  try {
    await client1.connect();
    const db = await client1.db("aiqod-staging"); //stage
    console.log(`Running Node.js version: ${process.version}`);

    const data = await db.collection("prasannaPurpleBuses").find({}).toArray();
    console.log(data);

    return res.status(200).json("Hello");
  } catch (error) {
    res
      .status(500)
      .json({ error: "Error generating PDF", details: error.message });
  }
});

app.get("/scrapper/check", async (req, res) => {
  try {
    console.log(`Running Node.js version: ${process.version}`);

    return res.status(200).json("Hello");
  } catch (error) {
    res
      .status(500)
      .json({ error: "Error generating PDF", details: error.message });
  }
});

app.post("/scrapper/yuvaraj", async (req, res) => {
  try {
    let body = req.body;
    let response = await toneAnalysis(body);
    console.log("Response from toneAnalysis: ", response);
    res.status(200).json(response);
  } catch (error) {
    console.error("Error in /scrapper/yuvaraj:", error);
  }
});

app.post("/scrapper/playwright", async (req, res) => {
  try {
    const { input, orgId, subscriberId, userId, config } = req.body;

    if (!input || !orgId || !subscriberId || !userId || !config) {
      console.error("Missing required fields in request body");

      return res.status(400).json({ error: "Missing required fields" });
    }
    const routes = input.route;
    if (!routes || routes.length === 0) {
      return res.status(400).json({ error: "Missing route in request body" });
    }
    console.log("Routes to process: ", routes);

    // Respond immediately that processing has started
    res.status(202).json({ message: "Processing started" });
    console.log("config : ", config);
    console.log("config : ", typeof config);
    let configData = JSON.parse(config);
    console.log("configData : ", typeof configData);
    console.log("configData : ", configData);

    // console.log("Config Data: ", configData);
    const uriSrc = configData.mongourl; //db url
    const client1 = new MongoClient(uriSrc);
    await client1.connect();
    const db = await client1.db(configData.dbname);

    let response = {};
    for (const route of routes) {
      response[route.redBusSource + "-" + route.redBusDestination] = {};
      // 1. Scrape Paytm
      try {
        const resData = await searchPaytm(
          route,
          response[route.redBusSource + "-" + route.redBusDestination]
        );
      } catch (e) {
        console.log("Error in paytm", e);
        response["paytm"] = "no buses found";
      }

      // 2. Scrape Abhibus
      try {
        const resData = await searchAbhiBus(
          route,
          response[route.redBusSource + "-" + route.redBusDestination]
        );
      } catch (e) {
        console.log("Error in abhibus", e);
        response["abhibus"] = "no buses found";
      }

      // 3. Scrape Redbus
      try {
        const resData = await searchRedBus(
          route,
          response[route.redBusSource + "-" + route.redBusDestination]
        );
      } catch (e) {
        console.log("Error in redbus", e);
        response["redbus"] = "no buses found";
      }
    }
    console.log("Response ", response);
    let convertExcel = await convertExecel(response);
    let excelFilePath = convertExcel["publicUrl"];
    console.log("Excel file path ", excelFilePath);

    // reviews part
    try {
      const reviews = await readUserReview();
      console.log("Reviews: ", reviews);
      if (!reviews || reviews.length === 0) {
        console.log("No reviews found to process");
        throw new Error("No reviews found");
      }
      const reviewsAboveThree = reviews.filter((review) => review.rating > 3);
      let reviewsBelowThree = reviews.filter((review) => review.rating <= 3);
      let reviewsToInsert = reviewsBelowThree.map((review) => {
        return { ...review, escalate: "yes" };
      });
      let responseFromGenAi =[];
      if( reviewsAboveThree.length >0) {
       responseFromGenAi = await toneAnalysis(reviewsAboveThree);
      }
      reviewsToInsert = [...reviewsToInsert, ...responseFromGenAi];
      reviewsToInsert = reviewsToInsert.map((review) => {
        return {
          ...review,
          description: `Mobile : ${review.Mobile},\n
          PNR: ${review.PNR}, \n
          Journey SRC: ${review.journeySRC},  Journey DST: ${review.journeyDST},\n
          Customer Name: ${review.customerName},\n
          Customer Review: ${review.customerReview},\n
          Review Posted Date: ${review.reviewPostedDate},\n
          Journey Date: ${review.journeyDate},\n
          Rating: ${review.rating}
          `,
          passenger_name: review.customerName,
          isDeleted: false,
          createdAt: new Date(),
          updatedAt: new Date(),
          orgId: new ObjectId(orgId),
          subscriberId: new ObjectId(subscriberId),
          userId: new ObjectId(userId),
        };
      });
      console.log("Reviews to insert: ", reviewsToInsert);
      await db
        .collection("purpleReviews")
        .updateMany({}, { $set: { isDeleted: true } });
      if (reviewsToInsert.length > 0) {
        const collection = db.collection("purpleReviews");
        await collection.insertMany(reviewsToInsert);
        console.log("Reviews inserted successfully");
      }
    } catch (e) {
      console.log("Error in reading reviews", e);
    }

    const url = `${configData.apirUrl}/gibots-api/bots/triggerProcess`;
    const options = {
      orgId: orgId,
      subscriberId: subscriberId,
      userId: userId,
      triggerData: {
        additionalInfo: [
          {
            addToTaskList: false,
            name: "publicUrl",
            required: false,
            label: "publicUrl",
            value: excelFilePath,
            id: "0",
          },
        ],
        customerId: "5b8fd401b3930517f134c569",
        processId: "680627c3eff7f475cf839148",
        projectId: "680627c3eff7f475cf83914e",
        taskDesc: "",
        projectName: "Automatic Prassana Automation",
        username: "Admin",
        accessControlList: [
          {
            permissionsList: {
              execute: true,
              view: true,
              edit: true,
              add: true,
            },
            controlType: "users",
            controlName: "Admin",
            controlId: "5beaabd82ac6767c86dc311e",
            _id: "67729c4be8ea3efa77dfa76a",
          },
          {
            permissionsList: {
              execute: true,
              view: true,
              edit: true,
              add: true,
            },
            controlType: "users",
            controlName: "Deepa",
            controlId: "66eac67c4b94159b93983810",
            _id: "67729c4be8ea3efa77dfa769",
          },
        ],
      },
    };
    await axios.post(url, options);
    console.log("Process is triggered successfully");
  } catch (error) {
    console.log("error ", error);
    // No res.status here, as response is already sent
  }
});

async function readUserReview() {
  const { chromium } = require("playwright");

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
      };
    });
    console.log("Customer Reviews:", customerReviewObjects[0]);
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

    // const reviewsAboveThree = filteredReviews.filter(
    //   (review) => review.rating > 3
    // );
    // const reviewsBelowThree = filteredReviews.filter(
    //   (review) => review.rating <= 3
    // );
    // // console.log("Filtered Reviews:", filteredReviews);
    // console.log("reviewsAboveThree Reviews:", reviewsAboveThree);
    // console.log("reviewsBelowThree Reviews:", reviewsBelowThree);
    return filteredReviews;
  } catch (e) {
    console.error("❌ Test failed:", e.message);
    return [];
  } finally {
    try {
      if (browser?.isConnected()) {
        await browser.close();
      }
    } catch (e) {
      console.warn("Error while closing browser:", e.message);
    }
  }
}

async function toneAnalysis(reviews) {
  try {
    let prompt = `
        You are a customer support assistant analyzing post-journey reviews to determine customer satisfaction and whether any review requires escalation.

        Given the following JSON array of customer feedback data, analyze each object’s 'customerReview' for **tone** (e.g., positive, neutral, negative) and **sentiment** (e.g., happy, frustrated, complaining, praising).

        For each review, add a new field 'escalate':
        - "yes" if the review indicates a **problem**, **complaint**, or **negative sentiment** that might need customer support or follow-up.
        - "no" if the review is positive, appreciative, or does not require attention.

        Keep the rest of the original data as-is.

        Here is the data:
        ${JSON.stringify(reviews, null, 2)}
        
        it is very crucial to Return only the final JSON object as output—no explanation or commentary.
        Populate the output JSON: Respond **only** with this code block:
        \`\`\`json{{result}}\`\`\`
        `;

    let response = await callGemini(prompt);
    console.log("Response from Gemini: ", response);
    return response;
  } catch (e) {
    console.error("Error in toneAnalysis: ", e.message);
    return [];
  }
}
async function convertExecel(jsonData) {
  const XLSX = require("xlsx");
  const fs = require("fs");
  let timestamp = Date.now();
  const formattedDate = new Date()
    .toLocaleDateString("en-GB")
    .replaceAll("/", "-"); // dd/mm/yyyy
  console.log(formattedDate);
  const rows = [];
  for (const route in jsonData) {
    for (const time in jsonData[route]) {
      const entry = jsonData[route][time];
      rows.push({
        route,
        time,
        paytmBus: entry.paytmBus || "NA",
        abhiBus: entry.abhiBus || "NA",
        redBus: entry.redBus || "NA",
        srpRanking: entry.srpRanking || "NA",
      });
    }
  }

  // Convert JSON data to worksheet
  const ws = XLSX.utils.json_to_sheet(rows);

  // Create a new workbook with the worksheet
  const wb = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(wb, ws, "Bus Ratings");
  let output = {};

  let filepath = path.join(
    "E:/test/public/excel",
    "ExcelSheets",
    `excel-${timestamp}-${formattedDate}.xlsx`
  );
  output["filepath"] = filepath;
  console.log("first path ", filepath);
  // Write the Excel file to disk
  XLSX.writeFile(wb, filepath);
  publicUrl =
    "https://172.168.1.22/public/excel/ExcelSheets/" +
    `excel-${timestamp}-${formattedDate}.xlsx`;
  output["publicUrl"] = publicUrl;
  output["jsonData"] = rows;
  console.log("Public URL ", publicUrl);

  return output;
}
async function searchPaytm(route, response) {
  const { chromium } = require("playwright");

  const browser = await chromium.launch({ headless: false }); // set to true for headless
  const context = await browser.newContext();
  const page = await context.newPage();

  try {
    await page.goto("https://tickets.paytm.com/");
    await page.waitForTimeout(2000);

    await page.click("#Bus");
    console.log("Clicked on Buses");
    await page.waitForTimeout(2000);

    // await page.click('#oneway');
    // await page.waitForTimeout(2000);

    // const sourceInput = page.locator("#dwebSourceInput");
    // await sourceInput.fill(route.paytmBusSource);
    // await page.waitForTimeout(2000);
    // await page.locator("(//div[@class='+2ajg'])[1]").click();

    //from old code
    await page.getByRole("textbox", { name: "From" }).click();
    await page
      .getByRole("textbox", { name: "From" })
      .fill(route.paytmBusSource);
    await page.waitForTimeout(3000);
    console.log(1);
    await page.waitForSelector("#source-section .dcrjM");
    await page.click("#source-section .dcrjM >> nth=0");
    //from old code

    console.log("Source filled");
    // const destinationInput = page.locator("#dwebDestinationInput");
    // await destinationInput.fill(route.paytmBusDestination);
    // await page.waitForTimeout(2000);
    // await page.locator("(//div[@class='+2ajg'])[1]").click();

    //from old code
    await page.getByRole("textbox", { name: "To" }).click();
    await page
      .getByRole("textbox", { name: "To" })
      .fill(route.paytmBusDestination);
    await page.waitForTimeout(3000);
    console.log(3);

    await page.waitForSelector("#destination-section .dcrjM");
    await page.click("#destination-section .dcrjM >> nth=0");
    console.log(4);
    //from old code

    console.log("Destination filled");
    await page.waitForTimeout(2000);
    await page.locator("//div[@aria-label='Today']").click();
    console.log("Date selected");
    await page.waitForTimeout(2000);
    await page.click("button:has-text('Search Buses')");
    await page.waitForTimeout(5000);
    console.log("Search Buses clicked");
    await page.evaluate(() => window.scrollBy(0, 900));
    await page.waitForTimeout(2000);

    const viewMore = await page.$("//div[normalize-space()='View More(3)']");
    if (viewMore) await viewMore.click();
    await page.waitForTimeout(5000);
    await page
      .getByRole("textbox", { name: "Search Operators" })
      .fill("prasanna");
    const prasannaBus = await page.$(
      "(//div[contains(text(),'Prasanna - Purple Bus')])[1]"
    );
    if (prasannaBus) await prasannaBus.click();
    console.log("Prasanna bus selected");
    await page.waitForTimeout(5000);
    await page.evaluate(() => window.scrollBy(0, -1400));

    // Extract bus data
    await page.waitForSelector("div.IHKeM", { timeout: 20000 });
    const buses = await page.$$("div.IHKeM");

    console.log(`Total buses found: ${buses.length}`);

    for (let i = 0; i < buses.length; i++) {
      console.log("-------------------------------------");
      console.log(`Bus ${i + 1}`);

      const bus = buses[i];

      const rating = await bus
        .$eval("span.QJoiM", (el) => el.textContent)
        .catch(() => "NA");
      const departure = await bus
        .$eval("div.wYtCy div._4rWgi", (el) => el.textContent)
        .catch(() => "NA");
      const arrival = await bus
        .$eval("div.EjC2U div._4rWgi", (el) => el.textContent)
        .catch(() => "NA");
      const price = await bus
        .$eval("span.A2eT9", (el) => el.textContent)
        .catch(() => "NA");

      console.log(`Rating: ${rating}`);
      console.log(`Departure: ${normalizeTime(departure)}`);
      console.log(`Arrival: ${normalizeTime(arrival)}`);
      console.log(`Price: ${price}`);

      if (!response[normalizeTime(departure)]) {
        response[normalizeTime(departure)] = {};
      }
      response[normalizeTime(departure)]["paytmBus"] = rating;
    }
  } catch (err) {
    console.error("Error:", err);
  } finally {
    try {
      if (browser?.isConnected()) {
        await browser.close();
      }
    } catch (e) {
      console.warn("Error while closing browser:", e.message);
    }
  }
}

async function searchAbhiBus(route, response) {
  const { chromium } = require("playwright");

  const browser = await chromium.launch({ headless: false }); // set headless: true for automation
  const context = await browser.newContext();
  const page = await context.newPage();

  try {
    // Step 1: Login to AbhiBus Travel (navigate)
    await page.goto("https://www.abhibus.com/");
    await page.waitForTimeout(5000);
    console.log("Navigated to AbhiBus");
    // Step 2: Click "Buses"
    await page.click(
      "//div[contains(@class,'lob-actions col')]//span[contains(text(),'Buses')]"
    );
    await page.waitForTimeout(2000);
    console.log("Clicked on Buses");
    // Step 3: Enter source - Pune
    // await page.fill(
    //   "//input[@placeholder='Leaving From']",
    //   route.abhiBusSource
    // );
    // await page.waitForSelector(
    //   `//div[contains(@class,'auto-complete-drop-down')]//div[contains(text(),'${route.abhiBusSource}')]`
    // );
    // await page.click(
    //   `//div[contains(@class,'auto-complete-drop-down')]//div[contains(text(),'${route.abhiBusSource}')]`
    // );
    //from old code
    await page.getByRole("textbox", { name: "Leaving From" }).click();
    await page
      .getByRole("textbox", { name: "Leaving From" })
      .fill(route.abhiBusSource);
    await page.waitForTimeout(5000);

    await page.waitForSelector(
      "div.auto-complete-drop-down .auto-complete-list"
    );
    await page.click(".auto-complete-list .auto-complete-list-item >> nth=0");
    //from old code
    console.log("Source filled");
    await page.waitForTimeout(2000);

    // Step 4: Enter destination - Chandrapur
    // await page.fill(
    //   "//input[@placeholder='Going To']",
    //   route.abhiBusDestination
    // );
    // await page.waitForSelector(
    //   `//div[contains(@class,'auto-complete-drop-down')]//div[contains(text(),'${route.abhiBusDestination}')]`
    // );
    // await page.click(
    //   `//div[contains(@class,'auto-complete-drop-down')]//div[contains(text(),'${route.abhiBusDestination}')]`
    // );
    //from old code
    await page
      .getByRole("textbox", { name: "Going To" })
      .fill(route.abhiBusDestination);
    await page.waitForTimeout(5000);
    await page.waitForSelector(
      "div.auto-complete-drop-down .auto-complete-list"
    );
    await page.click(".auto-complete-list .auto-complete-list-item >> nth=0");
    //from old code

    console.log("Destination filled");
    await page.waitForTimeout(2000);

    // Step 5: Click Search
    await page.click("//span[normalize-space()='Search']");
    await page.waitForTimeout(5000);

    // Step 6: Apply Bus Partner Filter
    await page.click("//div[contains(text(),'Bus Partner')]");
    await page.waitForTimeout(2000);
    await page.fill("//input[@placeholder='Search here']", "Prasanna");
    await page.waitForTimeout(2000);
    await page.click("//input[@type='checkbox']"); // Select the checkbox
    console.log("Bus Partner filter applied");
    // Step 7: Extract Bus Data
    const buses = await page.$$("div[id^='service-card-body-']");
    console.log(`Total buses found: ${buses.length}`);

    let count = 1;
    for (const bus of buses) {
      console.log("-------------------------------------");
      console.log(`Bus ${count}`);

      const getText = async (selector) => {
        try {
          const el = await bus.$(selector);
          return el ? await el.textContent() : "NA";
        } catch {
          return "NA";
        }
      };

      const busType = await getText(
        "*[id*='service-operator-agent-name-'] > div"
      );
      const departure = await getText(
        "#travel-distance-source-info div div span"
      );
      const arrival = await getText(
        "#travel-distance-destination-info div div span"
      );
      const price = await getText(
        "*[id*='service-operator-fare-info-'] div div:nth-child(1) div:nth-child(2) span:nth-child(2)"
      );
      const rating = await getText("*[id*='rating-card-container'] > div span");

      console.log(`Bus Type: ${busType}`);
      console.log(`Departure: ${normalizeTime(departure)}`);
      console.log(`Arrival: ${normalizeTime(arrival)}`);
      console.log(`Price: ${price}`);
      console.log(`Rating: ${rating}`);

      if (!response[normalizeTime(departure)]) {
        response[normalizeTime(departure)] = {};
      }
      response[normalizeTime(departure)]["abhiBus"] = rating;

      count++;
    }
  } catch (err) {
    console.error("❌ Error:", err);
  } finally {
    try {
      if (browser?.isConnected()) {
        await browser.close();
      }
    } catch (e) {
      console.warn("Error while closing browser:", e.message);
    }
  }
}
async function searchRedBus(route, response) {
  const { chromium } = require("playwright");

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
    const closeIcon = page.locator(".QuickFundBanner---cross---2Mp_5");

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
    await page.fill("xpath=//input[@placeholder='Source']", route.redBusSource);
    await page.waitForTimeout(3000);
    await page.click(`xpath=//div[contains(text(),'${route.redBusSource}')]`);
    await page.waitForTimeout(2000);
    await page.fill(
      "xpath=//input[@placeholder='Destination']",
      route.redBusDestination
    );
    await page.waitForTimeout(2000);
    await page.click(
      `xpath=//div[contains(text(),'${route.redBusDestination}')]`
    );
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
            ? (
                await (await element.getProperty("textContent")).jsonValue()
              ).trim()
            : "NA";
        };

        const arrivalTime = await getText(
          card,
          "span[style*='text-align: left']"
        );
        const rating = await getText(card, "span[class*='Sub_Rated_space']");

        console.log(`\nService ${i + 1} Arrival Time: ${arrivalTime}`);
        console.log(`Service ${i + 1} Rating: ${rating}`);
        if (!response[normalizeTime(arrivalTime)]) {
          response[normalizeTime(arrivalTime)] = {};
        }
        response[normalizeTime(arrivalTime)]["redBus"] = rating;

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

          const todayRankElem = await page.$(
            "xpath=(//div[contains(@class,'rankTextDiv')])[1]"
          );
          if (todayRankElem) {
            todayRank = (await todayRankElem.textContent())?.trim() || "NA";
          }

          const outOfElem = await page.$(
            "xpath=(//div[contains(@class,'totalTextDiv')])[1]"
          );
          if (outOfElem) {
            outOf = (await outOfElem.textContent())?.trim() || "NA";
          }

          console.log(`Service ${i + 1} Today's Rank: ${todayRank} ${outOf}`);
          response[normalizeTime(arrivalTime)]["srpRanking"] =
            todayRank + " " + outOf;

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
    try {
      if (browser?.isConnected()) {
        await browser.close();
      }
    } catch (e) {
      console.warn("Error while closing browser:", e.message);
    }
  }
}

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
function normalizeTime(input) {
  const { DateTime } = require("luxon");

  input = input
    .trim()
    .toLowerCase()
    .replace(/\.|–|—/g, ":") // Replace dots and other separators with colon
    .replace(/\s+/g, " ") // Normalize spaces
    .replace(/\s*([ap]m)/, " $1"); // Ensure space before am/pm
  let dt;

  // Try parsing as 12-hour format with AM/PM
  if (
    input.toLowerCase().includes("am") ||
    input.toLowerCase().includes("pm")
  ) {
    dt = DateTime.fromFormat(input.trim(), "hh:mm a");
  } else {
    // Try parsing as 24-hour format
    dt = DateTime.fromFormat(input.trim(), "HH:mm");
  }

  // Return in 24-hour format (HH:mm) or throw if invalid
  if (dt.isValid) {
    return dt.toFormat("HH:mm");
  } else {
    return input;
  }
}

async function callopenAI(prompt) {
  // last parameters contains info from headerParams
  const requestId = Date.now().toString();
  try {
    const response = await fetch("https://api.openai.com/v1/chat/completions", {
      method: "POST",
      headers: {
        Authorization: `Bearer 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`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        model: "gpt-4o-mini",
        response_format: { type: "json_object" },
        messages: [{ role: "user", content: prompt }],
      }),
    });

    const data = await response.json();
    console.log(data);
    const promptTokens = data.usage.prompt_tokens;
    const completionTokens = data.usage.completion_tokens;
    console.log(data.choices[0].message.content);
    const parsedData = JSON.parse(data.choices[0].message.content);

    const output = parsedData.output;
    console.log(output);

    return output;
  } catch (error) {
    console.error("Error:", error);
    return { message: "There was an error running this function" };
  }
}

async function callGemini(prompt) {
  // last parameters contains info from headerParams
  const requestId = Date.now().toString();
  try {
    const response = await ai.models.generateContent({
      model: "gemini-2.5-flash-lite-preview-06-17",
      contents: prompt,
    });
    let output = response.text;

    console.log(output);
    console.log("Type ", typeof output);

    let cleaned = output.replace(/^`+json\n|`+$/g, "");

    let parsed;
    try {
      parsed = JSON.parse(cleaned);
      console.log(parsed); // Note the typo: "ouptut"
    } catch (e) {
      console.error("Failed to parse JSON:", e);
    }

    return parsed;
  } catch (error) {
    console.error("Error:", error);
    return { message: "There was an error running this function" };
  }
}
// Start the Server
app.listen(PORT, () => {
  console.log(`🚀 Server running on http://localhost:${PORT}`);
});
