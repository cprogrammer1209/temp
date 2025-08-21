const { DateTime } = require("luxon");
const { chromium } = require("playwright");
async function searchRedBus(route, response, mongoDocs) {
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
    // const closeIcon = await page.locator(".QuickFundBanner---cross---2Mp_5");
    // console.log("waiting ");

    // if (await closeIcon.isVisible()) {
    //   console.log("waiting 1");
    //   await closeIcon.click();
    // }
    await page.waitForSelector(".QuickFundBanner---cross---2Mp_5");
    await page.click(".QuickFundBanner---cross---2Mp_5");

    console.log("waiting 3");

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

    for (let i = 0; i < serviceCards.length; i++) {
      const card = serviceCards[i];

      const allDivs = await card.$$(
        "div.ServiceWise---body---1OnfX.App---clearfix---pl6UA"
      );
      // Try to find the one that also has the background class
      const targetDiv =
        (await allDivs.find(async (div) => {
          const className = await div.getAttribute("class");
          return className.includes("ServiceWise---backGround---2yaYw");
        })) ?? allDivs[0]; // fallback to the first if none match

      const textContent = await targetDiv.textContent();
      const viaArrivalTime = await targetDiv
        .$eval("span:has-text(':')", (el) => el.textContent.trim())
        .catch(() => "N/A");

      const fullRouteName = await targetDiv
        .$eval("span:has-text('-')", (el) => el.getAttribute("title"))
        .catch(() => "N/A");

      let fromCity = fullRouteName?.split("-")[1]?.trim() ?? fullRouteName;
      let toCity = fullRouteName?.split("-")[2]?.trim() ?? fullRouteName;
      fromCity = fromCity.split(" ")[0];
      toCity = toCity.split(" ")[0];
      console.log("Selected Div Text:", `fromCity: ${fromCity}, toCity: ${toCity}, viaArrivalTime: ${viaArrivalTime}`);

      const viaBtn = await card.$("span.ServiceWise---viaCnt---28sTm");
      if (viaBtn) {
        await viaBtn.click();
        await page.waitForTimeout(500);

        const viaRoutes = await card.$$("div.ServiceWise---body---1OnfX");
        console.log(`Via Routes: ${viaRoutes.length}`);
        let mainRouteTime = null;
        let match = null;
        for (let j = 0; j < viaRoutes.length; j++) {
          const via = viaRoutes[j];

          const viaArrivalTime = await via
            .$eval("span:has-text(':')", (el) => el.textContent.trim())
            .catch(() => "N/A");

          let subArrivalTime = normalizeTime(viaArrivalTime);
          const fullRouteName = await via
            .$eval("span:has-text('-')", (el) => el.getAttribute("title"))
            .catch(() => "N/A");

          let fromCity = fullRouteName?.split("-")[1]?.trim() ?? fullRouteName;
          let toCity = fullRouteName?.split("-")[2]?.trim() ?? fullRouteName;
          fromCity = fromCity.split(" ")[0];
          toCity = toCity.split(" ")[0];
          if (j === 0 && viaArrivalTime !== "N/A") {
            mainRouteTime = normalizeTime(viaArrivalTime);
            //mapping with the response structure
            match = await findMatchingSchedule(
              mainRouteTime,
              mongoDocs,
              fromCity,
              toCity
            );
          }
          const viaRating = await via
            .$eval("span.ServiceWise---Sub_Rated_space---3I1dX", (el) =>
              el.textContent.trim()
            )
            .catch(() => "N/A");

          const trend = await via.$(`span:has-text("View trend")`);
          await trend.scrollIntoViewIfNeeded();
          await trend.click();

          await page.waitForSelector("div.RNRCalendar---rankTextDiv---250HN", {
            timeout: 5000,
          });
          const parent = await page.$("div.RNRCalendar---slideDiv---x6LMd");

          let input = await parent
            .$eval("div", (el) => el.textContent.trim())
            .catch(() => "N/A");
          const regex = /(\d+)\s*out\s*of\s*(\d+)/i;

          const matchSRP = input.match(regex);
          let srpRanking = "N/A";
          if (matchSRP) {
            srpRanking = `${matchSRP[1]} / ${matchSRP[2]}`;
            console.log(srpRanking); // Output: 4 / 76
          }
          const closeBtn = await page.$(
            "xpath=//div[contains(@class,'RNRCalendar---headerDiv')]/div[last()]"
          );
          if (closeBtn) {
            await closeBtn.click();
          }
          await page.waitForTimeout(300);
          // console.log(`Via ${j+1} Today's Rank: ${todayRank} ${outOfText}`);
          console.log(
            `Via ${
              j + 1
            }: ${fromCity} - ${toCity}, Arrival: ${viaArrivalTime}, Rating: ${viaRating}, SRP Ranking: ${srpRanking}`
          );

          if (!match) {
            console.log(
              `--No matching schedule found for via route: ${fromCity} → ${toCity} @ ${subArrivalTime}`
            );
            continue;
          }

          const rawMainRouteName = match["Schedule Code"];
          const mainRouteName = extractMainRouteName(rawMainRouteName);
          const mainDepartureTime = formatTimeFromSchedule(rawMainRouteName);
          const subrouteKey = `${fromCity} - ${toCity}`;

          if (!response[mainRouteName]) response[mainRouteName] = {};
          if (!response[mainRouteName][mainDepartureTime])
            response[mainRouteName][mainDepartureTime] = {};
          if (!response[mainRouteName][mainDepartureTime][subrouteKey])
            response[mainRouteName][mainDepartureTime][subrouteKey] = {};
          if (
            !response[mainRouteName][mainDepartureTime][subrouteKey][
              subArrivalTime
            ]
          ) {
            response[mainRouteName][mainDepartureTime][subrouteKey][
              subArrivalTime
            ] = {};
          }

          response[mainRouteName][mainDepartureTime][subrouteKey][
            subArrivalTime
          ]["redbus"] = viaRating;

          response[mainRouteName][mainDepartureTime][subrouteKey][
            subArrivalTime
          ]["srpRating"] = viaSrpRating;
        }
      } else {
        console.log(`No via routes for service ${i + 1}`);
      }
    }
  } catch (e) {
    console.error(" Test failed:", e.message);
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
searchRedBus(
  {
    "SR No": 1326,
    RouteName:
      "Nagpur To Mumbai via Amravati 2x1(36) AC Sleeper, Prasanna - Purple Bus",
    Time: "09:15 PM",
    "From City": "Nagpur",
    "To City": "Pune",
    "Schedule Code": "118606-NagpurMumbai6:30 PM",
    "Bus Arrangement Name": "36 BERTH 2X1 AC SLEEPER",
    RouteID: 54694,
    RouteTimeID: 118606,
    "Status ": "Active",
    phone_num: "",
    subscriberId: "5beaabd82ac6767c86dc311c",
    orgId: "5c495dbfffa2a85b2c19a77f",
    redBusSource: "Pune",
    redBusDestination: "Nagpur",
  },
  {},
  []
).catch((e) => {
  console.error("Error in searchRedBus:", e.message);
});
function findMatchingSchedule(subTimeStr, dbRecords, fromCity, toCity) {
  let filteredDoc = dbRecords.filter(
    (item) =>
      item["Time"] == subTimeStr &&
      item["From City"] == fromCity &&
      item["To City"] == toCity
  );

  return filteredDoc[0];
}
function extractMainRouteName(rawName) {
  // Remove route code prefix (e.g., "14708 -")
  rawName = rawName.replace(/^\d+\s*-\s*/, "");

  // Fix camel case (e.g., PuneNagpur → Pune To Nagpur)
  rawName = rawName.replace(/([a-z])([A-Z])/g, "$1 To $2");

  // Remove time from end (e.g., "Pune To Chandrapur 5:00 PM" → "Pune To Chandrapur")
  rawName = rawName.replace(/\s*\d{1,2}:\d{2}\s*[APMapm]{2}$/, "");

  // Clean any trailing dash
  rawName = rawName.replace(/\s*-\s*$/, "");

  return rawName.trim();
}
function formatTimeFromSchedule(scheduleCode) {
  // Match standard format: "13223 - Pune To Nagpur - 07:00 PM"
  const standardMatch = scheduleCode.match(/(\d{1,2}:\d{2} ?[AP]M)$/i);
  if (standardMatch) return standardMatch[1].toUpperCase();

  // Match compact format: "119060-PuneNagpur8:30 PM"
  const compactMatch = scheduleCode.match(/(\d{1,2}:\d{2} ?[AP]M)/i);
  if (compactMatch) return compactMatch[1].toUpperCase();

  return "N/A"; // fallback
}
function normalizeTime(input) {
  input = input
    .trim()
    .toLowerCase()
    .replace(/\+1$/, "")
    .replace(/\.|–|—/g, ":")
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
    return dt.toFormat("hh:mm a").toUpperCase();
  } else {
    return input;
  }
}
