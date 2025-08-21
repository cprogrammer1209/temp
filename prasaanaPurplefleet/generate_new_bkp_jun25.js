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

app.post("/scrapper/playwright", async (req, res) => {
  try {
    await client1.connect();
    const db = await client1.db("aiqod-staging");
    const { input, orgId, subscriberId, userId } = req.body;

    if (!input || !orgId || !subscriberId || !userId) {
      return res.status(400).json({ error: "Missing required fields" });
    }
    const routes = input.route;
    if (!routes || routes.length === 0) {
      return res.status(400).json({ error: "Missing route in request body" });
    }
    console.log("Routes to process: ", routes);

    // Respond immediately that processing has started
    res.status(202).json({ message: "Processing started" });

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

    const url = "http://172.168.1.19:7894/gibots-api/bots/triggerProcess";
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
      model: "gemini-2.5-flash-preview-04-17",
      contents: prompt,
    });
    let output = response.text;

    console.log(output);
    console.log("Type ", typeof output);

    let cleaned = output.replace(/^`+json\n|`+$/g, "");

    let parsed;
    try {
      parsed = JSON.parse(cleaned);
      console.log(parsed.ouptut); // Note the typo: "ouptut"
    } catch (e) {
      console.error("Failed to parse JSON:", e);
    }

    return parsed;
  } catch (error) {
    console.error("Error:", error);
    return { message: "There was an error running this function" };
  }
}

async function readUserReview(routes) {
  try {
    const { chromium } = require("playwright");
    const { convert } = require("html-to-text");
    let data = {};
    for (const route of routes) {
      data[route.source + "-" + route.destination] = "";
      console.log("route", route);
      const browser = await chromium.launch({ headless: false }); // Run headful to avoid detection

      try {
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
        console.log(1);
        await page.goto(
          "https://accounts.redbus.com/login?continue=https://www.redbus.pro/"
        );
        await page.waitForTimeout(5000);
        console.log(2);

        await page.getByRole("textbox", { name: "Username" }).click();
        await page.getByRole("textbox", { name: "Username" }).fill("9748");
        await page.getByRole("textbox", { name: "Username" }).press("Tab");
        await page.getByRole("textbox", { name: "Password" }).click();
        await page
          .getByRole("textbox", { name: "Password" })
          .fill("prasannapurple");
        await page.getByRole("button", { name: "Login", exact: true }).click();
        console.log(3);

        await page.locator('role=button[name="Skip"]').click();

        await page.hover("aside.SideNav---sideNav---3QZiY ");

        await page.locator('role=link[name="R & R"]').click();
        await page.waitForTimeout(5000);
        console.log(4);

        await page.click("#reviews_tab");
        const response = await page.waitForResponse(
          (response) =>
            response
              .url()
              .includes(
                "https://www.redbus.pro/win/api/ratingsReviews/getAllReviewsRnR/0"
              ) && response.status() === 200
        );
        await page.waitForTimeout(1000);
        const inputSelector = 'input[placeholder="Source"]';
        console.log(5);

        await page.waitForSelector(inputSelector);
        await page.click(inputSelector);
        await page.waitForTimeout(2000);
        await page.fill(inputSelector, route.redBusSource);
        await page.waitForTimeout(2000);
        await page
          .locator("#react-autowhatever-1 #react-autowhatever-1--item-0")
          .click();
        await page.waitForTimeout(2000);
        console.log(6);

        const inputSelector1 = 'input[placeholder="Destination"]';

        await page.waitForSelector(inputSelector1);
        await page.click(inputSelector1);
        await page.waitForTimeout(2000);
        await page.fill(inputSelector1, route.redBusDestination);
        await page
          .locator("#react-autowhatever-1 #react-autowhatever-1--item-0")
          .click();
        await page.waitForTimeout(2000);
        console.log(7);

        const filterBtnSelector = 'button:has-text("Filter")';
        await page.waitForSelector(filterBtnSelector, { state: "visible" });
        await page.click(filterBtnSelector);
        await page.waitForTimeout(2000);
        console.log(8);

        let count = 0;
        while (count < 3) {
          count++;
          await page.evaluate(() =>
            window.scrollTo(0, document.body.scrollHeight)
          );
          await page.waitForTimeout(1000);
        }
        console.log(9);

        const busCard = await page
          .locator("div.AllRatings---containerDomestic---3_5gZ")
          .innerHTML();
        // console.log(busCard)
        const text = convert(busCard, {
          wordwrap: false, // optional: prevents line breaks
          selectors: [
            { selector: "a", options: { hideLinkHrefIfSameAsText: true } },
            { selector: "div", format: "block" },
          ],
        });
        console.log(10);

        data[`${route.source}-${route.destination}`] = text;
        await browser.close();
      } catch (e) {
        console.log("Error in paytm", e);
        data[`${route.source}-${route.destination}`] = "no buses found";
        await browser.close();
      }
      // console.log("res 1234 ",response)
    }

    return { status: 0, msg: "success", data: data };
  } catch (e) {
    console.log("Error in reading user review", e);
    return { status: 1, msg: "error", data: e };
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
    "https://deployement.aiqod.com/automation/public/excel/ExcelSheets/" +
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

    const sourceInput = page.locator("#dwebSourceInput");
    await sourceInput.fill(route.paytmBusSource);
    await page.waitForTimeout(2000);
    await page.locator("(//div[@class='+2ajg'])[1]").click();
    console.log("Source filled");
    const destinationInput = page.locator("#dwebDestinationInput");
    await destinationInput.fill(route.paytmBusDestination);
    await page.waitForTimeout(2000);
    await page.locator("(//div[@class='+2ajg'])[1]").click();
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
    await browser.close();
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
    await page.fill(
      "//input[@placeholder='Leaving From']",
      route.abhiBusSource
    );
    await page.waitForSelector(
      `//div[contains(@class,'auto-complete-drop-down')]//div[contains(text(),'${route.abhiBusSource}')]`
    );
    await page.click(
      `//div[contains(@class,'auto-complete-drop-down')]//div[contains(text(),'${route.abhiBusSource}')]`
    );
    console.log("Source filled");
    await page.waitForTimeout(2000);

    // Step 4: Enter destination - Chandrapur
    await page.fill(
      "//input[@placeholder='Going To']",
      route.abhiBusDestination
    );
    await page.waitForSelector(
      `//div[contains(@class,'auto-complete-drop-down')]//div[contains(text(),'${route.abhiBusDestination}')]`
    );
    await page.click(
      `//div[contains(@class,'auto-complete-drop-down')]//div[contains(text(),'${route.abhiBusDestination}')]`
    );
    console.log("Destination filled");
    await page.waitForTimeout(2000);

    // Step 5: Click Search
    await page.click("//span[normalize-space()='Search']");
    await page.waitForTimeout(10000);

    // Step 6: Apply Bus Partner Filter
    await page.click("//div[contains(text(),'Bus Partner')]");
    await page.waitForTimeout(2000);
    await page.fill("//input[@placeholder='Search here']", "Prasanna");
    await page.waitForTimeout(2000);
    await page.click("//input[@type='checkbox']"); // Select the checkbox
cosnole.log("Bus Partner filter applied");
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
    await browser.close();
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
    await browser.close();
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
// Start the Server
app.listen(PORT, () => {
  console.log(`🚀 Server running on http://localhost:${PORT}`);
});
