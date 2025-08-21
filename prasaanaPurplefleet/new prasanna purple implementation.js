const express = require("express");
const bodyParser = require("body-parser");
const cors = require("cors");
const path = require("path");
const fs = require("fs/promises");
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
    console.log("Request body ", req.body);
    console.log("Request body ", req);
    await client1.connect();
    const db = await client1.db("aiqod-staging");
    const { input, orgId, subscriberId, userId } = req.body;
    console.log("hello ", input, orgId, subscriberId, userId);
    console.log(`Running Node.js version: ${process.version}`);

    if (input == "" || !input) {
      throw new Error("Missing htmlContent in request body");
    }
    if (orgId == "" || !orgId) {
      throw new Error("Missing orgId in request body");
    }
    if (subscriberId == "" || !subscriberId) {
      throw new Error("Missing subscriberId in request body");
    }
    if (userId == "" || !userId) {
      throw new Error({ error: "Missing userId in request body" });
    }
    res.status(200).json("Success FUlly done");
    let route = input.route;
    console.log("Route", route);
    if (route.length == 0) {
      throw new Error({ error: "Missing route in request body" });
    }
    let response = {};
    console.log("Before paytm");
    try {
      const resData = await searchPaytm(route);
      response["paytm"] = resData.data;
    } catch (e) {
      console.log("Error in paytm", e);
      response["paytm"] = "no buses found";
    }
    console.log("After paytm");
    console.log("Before searchAbhiBus");

    try {
      const resData = await searchAbhiBus(route);
      response["abhibus"] = resData.data;
    } catch (e) {
      console.log("Error in paytm", e);
      response["abhibus"] = "no buses found";
    }
    console.log("After searchAbhiBus");
    console.log("Before searchRedBus");

    try {
      const resData = await searchRedBus(route);
      response["redbus"] = resData.data;
    } catch (e) {
      console.log("Error in paytm", e);
      response["redbus"] = "no buses found";
    }
    console.log("After searchRedBus");

    const formattedDate = new Date()
      .toLocaleDateString("en-GB")
      .replaceAll("/", "-");

    // console.log("+++++++++++++++++++++++   ",response,"____________+++++++++++++++");
    let prompt = `
        You are a data aggregation assistant.

        I have extracted bus data from three different platforms: Redbus, Abhibus, and Paytm. Each platform lists bus details like route, departure time, and bus rating.

        Important Notes:
        - I have a travel agency, and I have registered the same bus (same route and time) on all three platforms.
        - Each platform may assign a different rating to the same bus (same route and time).
        - I want to consolidate the data by grouping the buses based on the same **route** and **departure time**.
        - For each unique route and departure time, create **only one JSON object**, and attach the bus rating from each platform under their respective keys.

        Scrapped data : ${JSON.stringify(response)}
        Today's date is ${formattedDate}.  


        ### Input Format:
        List of bus entries (from different platforms) in any order, each entry will contain:
        [
        {
            paytm: {  "Pune-Dhule": "...scrapped data..." },
            abhibus: {"Pune-Dhule":"...scrapped data..."  },
            redbus: { "Pune-Dhule": {
                "Bus 1":  "...scrapped data...",
                "Bus 2":"...scrapped data...",  
            }
            },
        },
        ];
        If a rating is missing for any platform, use 'null'.
        Redbus entries include a field called srpRanking — The srp ranking will be availble at the end of the each bus scarpped data in the redbus objct like \n\n\n\nSrp Rank 10\n\n; 
        The srp ranking value will only availble to redbus platform only
        if it's "SRP NA", set it as null. Ensure srpRanking is mapped correctly to each Redbus entry based on its position in the list.) Dates may appear as section headers in the table (e.g., "21 Apr", "22 Apr") and apply to all entries beneath them until the next date header appears.
        
        
        Please follow these strict output requirements:

            Group all bus trips under the correct route name.
            For each route, list each departure time and map platform ratings correctly (Redbus, Paytm, Abhibus) to the same route and time.
            Time format may vary (24-hour or 12-hour); always convert to 12-hour format with correct AM/PM designation.
            Extract only the following fields: startTime (in 12-hour format), date, ratings per platform, and srpRanking (Redbus only).
            It is very Crucial to use the 12 hour time format only, and the am/pm need to be correct.
            For Redbus, extract the rating located just after "View trend" and map the SRP ranking found at the end of the data block.
            srpRanking will available only to the redbus, and it is attached to the end of each bus scrapping data.
            For missing SRP values ("Srp NA"), use "NA".
            Do not duplicate entries if the route and time are the same across platforms. Instead, merge their ratings under a single JSON object per unique route and departure time.
            Ensure all ratings and srpRanking values are correctly mapped to the corresponding bus trip and departure time. This mapping is critical.
            All numeric fields (ratings and srpRanking) must be typed as numbers. Use null or "NA" only when data is unavailable.

            Return only the final JSON object as output—no explanation or commentary.


            
            

         Important: 

        For any bus route with multiple entries for the same **departure time** (like "06:00 PM" and "18:00"), **consider them as the same entry** and **combine their ratings** into a single record. Make sure that only one entry is created per unique route and time.

        Instructions:
        1. Normalize all **departure time** values to **12-hour format** (e.g., "18:00" should be converted to "6:00 PM").
        2. Group entries with the same **route** and **normalized departure time**.
        3. If there are multiple ratings for the same time from different platforms (Redbus, Paytm, Abhibus), merge them into a single record for that route and time.
        4. Any missing ratings should be represented as null.
        5. No duplicate entries should be crated to the 'route', and 'startTime', means for same route there should not be another duplicate entry for the same 'startTime'. 
        5.a) If The route with same timing is already there, then that objct only need to use
        6) different route will have same time, since it is a different route

        For example:
        - "18:00" should be converted to "6:00 PM" and then combined with other entries for "6:00 PM".

        Expected result(Just only reference, should not take for output):
        json
        [
        {
            "route": "Pune-Dhule",
            "startTime": "6:00 PM",
            "srpRanking":"37",
            "ratings": {
            "redbus": 3.4,
            "paytm": 3.5,
            "abhibus": 4.8
            }
        },
        {
            "route": "Pune-Dhule",
            "startTime": "7:45 PM",
            "srpRanking":"21",
            "ratings": {
            "redbus": 3.4,
            "paytm": 3.5,
            "abhibus": 4.8
            }
        },
        {
            "route": "Pune-Dhule",
            "startTime": "10:00 PM",
            "srpRanking":"54",
            "ratings": {
            "redbus": 3.4,
            "paytm": 3.558,
            "abhibus": 4.8
            }
        }
        ]
        it is very crucial to Return only the final JSON object as output—no explanation or commentary.
        Populate the output in the following json format : {'output':{\"responseData\": {...}}}
        `;
    console.log("Prompt ", prompt);
    // const openaiRes = await callopenAI(prompt);
    const openaiRes = await callGemini(prompt);
    let jsonData = openaiRes.output;
    // let jsonData = JSON.parse(JSON.stringify(openaiRes));

    console.log(typeof jsonData, " openaiRes " + jsonData.responseData);
    jsonData = jsonData.responseData;

    console.log("OPenai response ", jsonData);

    let output = await convertExecel(jsonData);
    let excelFilePath = output["publicUrl"];
    console.log("Excel file path ", excelFilePath);
    console.log("Excel json ", output["jsonData"]);
    try {
      output["jsonData"] = output["jsonData"].map((item) => {
        return {
          ...item,
          isDeleted: false,
          createdAt: new Date(),
          updatedAt: new Date(),
          orgId: new ObjectId(orgId),
          subscriberId: new ObjectId(subscriberId),
          userId: new ObjectId(userId),
        };
      });

      await db
        .collection("purpleRatings")
        .updateMany({}, { $set: { isDeleted: true } });
      await db.collection("purpleRatings").insertMany(output["jsonData"]);
    } catch (e) {
      console.log("Error in inserting data ", e);
    }

    let userReview = await readUserReview(route);
    let reviewPrompt = `
        You are given raw, unstructured bus travel review data. Each review starts with the passenger's name, followed by details such as date and time of the trip, source and destination, rating, and review text along with the review date and time.
        Scrapped Data : ${JSON.stringify(userReview.data)}
        Today's date is ${formattedDate}

        Instructions;
        1) this is scrapped user review data from redbus, so always the platform is redbus only
        2) You need extract only the user reviews which is related to today and yesterday date,others are not needed.
        3) And also you need to alanyse the user review tone. according to the review and review tone, you have to mention whether need to esclate or not.
        4) If the review is positive or neutral then mention "no" and if the review is negative then mention "yes"
            positive scenerios :
                1) user may tell about the expirence and all
                2) user may tell about the bus and all
            Negative scenerios :
                1) User may feel that these things are not there, if added then it will be good
                2) All new features related quries,
                3) And also if the user is not happy with the service and all
                4) Sometimes, the user give above 3 star rating, but the review is negative, so you need to analyse this as well by user tone and need to determine to esclate or not.
                4) and other negative scenerios
            You need to analyse this regardless of the rating by the user,
        5) The date will be any format, so you must need to give it only in DD/MM/YYYY format 
        6) If there is no scrappped data then return "no reviews found"
        7) If the user review have like this, 
                    'Reply disabled
                    You have replied to the review'
            Then it is already replied by the execute so, no need to extract again. just ignore. 
        7) It is very crucial not extract the replied reviews

        Your task is to extract and return the following fields in a structured JSON format:
        passenger_name
        date(time of the journey)
        time (date of the journey)
        source
        destination
        rating (as a number)
        review_text
        review_date_time (when the review was written)
        platrform (e.g., Redbus)
        decription
        esclate

        Expected JSON format:
        {
        "reviews": [
            {
            "passenger_name": "Name",
            "date" : "DD/MMM/YYYY",
            time": "hh:mm AM/PM",
            "source": "SourceCity",
            "destination": "DestinationCity",
            "rating": 5,
            "review_text": "Review content",
            "review_date" : "DD/MMM/YYYY",
            "review_time": "hh:mm AM/PM",
            "platform": "Redbus",
            "description": "description",
            "esclate": "yes/no"
            },
            
            // Repeat for other reviews
        ]
        }

        In the description field, you need to give like the user review, mobile number, date and time, need like generated from the ai. It should comphrensive to understand at single read.
        It is very crucial that the description must have the mobile number, if it is mentioned.
        Use the structure of the text to identify when each new review begins. Assume that names are at the top of each review section, and that the format is consistent.
        Make sure the number fields are in number type(It is very crucial to be the number field be in number type)
        Populate the output in the following json format : {'output':{\"responseData\": {...}}}
        `;

    console.log("reviewPrompt ", reviewPrompt);
    // const openaiReview = await callopenAI(reviewPrompt);
    const openaiReview = await callopenAI(reviewPrompt);
    // let jsonData = openaiRes.output;
    let jsonReview = JSON.parse(JSON.stringify(openaiReview));
    console.log("Review data ", jsonReview);
    console.log(typeof jsonReview, " openaiRes " + jsonReview.responseData);
    jsonReview = jsonReview.responseData;
    jsonReview.reviews = jsonReview.reviews.map((item) => {
      return {
        ...item,
        isDeleted: false,
        createdAt: new Date(),
        updatedAt: new Date(),
        orgId: new ObjectId(orgId),
        subscriberId: new ObjectId(subscriberId),
        userId: new ObjectId(userId),
      };
    });
    console.log("Final insert data ", jsonReview.reviews);
    try {
      await db
        .collection("purpleReviews")
        .updateMany({}, { $set: { isDeleted: true } });
      await db.collection("purpleReviews").insertMany(jsonReview.reviews);
    } catch (e) {
      console.log("Error in inserting data for review ", e);
    }

    console.log("OPenai response ", jsonReview);

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
    res
      .status(400)
      .json({ error: "Error generating PDF", details: error.message });
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
  let sheetData = [];
  let timestamp = Date.now();
  const formattedDate = new Date()
    .toLocaleDateString("en-GB")
    .replaceAll("/", "-"); // dd/mm/yyyy
  console.log(formattedDate);

  console.log("timestamp ", timestamp);
  sheetData = jsonData.map((entry) => ({
    Route: entry.route,
    Time: entry.startTime,
    "SRP Ranking": entry.srpRanking || "NA",
    Redbus_Rating: entry.ratings.redbus ?? "",
    Paytm_Rating: entry.ratings.paytm ?? "",
    AbhiBus_Rating: entry.ratings.abhibus || 4.8,
  }));

  // Convert JSON data to worksheet
  const ws = XLSX.utils.json_to_sheet(sheetData);

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
  output["jsonData"] = sheetData;
  console.log("Public URL ", publicUrl);

  return output;
}
async function searchPaytm(routes) {
  try {
    const { chromium } = require("playwright");
    const { convert } = require("html-to-text");
    let response = {};
    for (const route of routes) {
      response[route.paytmBusSource + "-" + route.paytmBusDestination] = "";
      console.log("route", route);
      const browser = await chromium.launch({ headless: false }); // Run headful to avoid detection

      try {
        const context = await browser.newContext({});

        const page = await context.newPage();
        await page.waitForTimeout(1500);
        console.log(1);

        await page.goto("https://tickets.paytm.com/bus/");
        await page.waitForTimeout(5000);
        console.log(2);

        await page.getByRole("textbox", { name: "From" }).click();
        await page
          .getByRole("textbox", { name: "From" })
          .fill(route.paytmBusSource);
        await page.waitForTimeout(3000);
        console.log(1);

        // await page.getByText('PuneMaharashtra', { exact: true }).click();
        await page.waitForSelector("#source-section .dcrjM");
        await page.click("#source-section .dcrjM >> nth=0");
        await page.getByRole("textbox", { name: "To" }).click();
        await page
          .getByRole("textbox", { name: "To" })
          .fill(route.paytmBusDestination);
        await page.waitForTimeout(3000);
        console.log(3);

        await page.waitForSelector("#destination-section .dcrjM");
        await page.click("#destination-section .dcrjM >> nth=0");
        console.log(4);

        // await page.getByText('NagpurMaharashtra', { exact: true }).click();
        await page.getByRole("button", { name: "Search Buses" }).click();
        await page.waitForTimeout(5000);
        await page.getByRole("textbox", { name: "Search Operators" }).click();
        await page
          .getByRole("textbox", { name: "Search Operators" })
          .fill("prasanna");
        await page
          .locator("div")
          .filter({ hasText: /^Bus operatorsPrasanna - Purple Bus$/ })
          .getByLabel("unchecked")
          .click();
        console.log(5);

        let count = 0;
        while (count < 3) {
          console.log("count scroll", count);
          count++;
          await page.evaluate(() =>
            window.scrollTo(0, document.body.scrollHeight)
          );
          await page.waitForTimeout(1000);
        }

        const busCard = await page.locator("div.-iAp6").innerHTML();
        // console.log(busCard)
        const text = convert(busCard, {
          wordwrap: false, // optiresponseonal: prevents line breaks
          selectors: [
            { selector: "a", options: { hideLinkHrefIfSameAsText: true } },
          ],
        });
        console.log(6);

        response[`${route.paytmBusSource}-${route.paytmBusDestination}`] = text;
        await browser.close();
      } catch (e) {
        console.log("Error in paytm", e);
        response[`${route.paytmBusSource}-${route.paytmBusDestination}`] =
          "no buses found";
        await browser.close();
      }
      // console.log("res 1234 ",response)
    }

    return { status: 0, msg: "success", data: response };
  } catch (e) {
    console.log(e);
    return { status: 1, msg: "error", data: e };
  }
}

async function searchAbhiBus(routes) {
  try {
    const { chromium } = require("playwright");
    const { convert } = require("html-to-text");
    let response = {};
    for (const route of routes) {
      response[route.abhiBusSource + "-" + route.abhiBusDestination] = "";
      console.log("route", route);
      const browser = await chromium.launch({ headless: false }); // Run headful to avoid detection

      try {
        const context = await browser.newContext({});

        const page = await context.newPage();
        await page.waitForTimeout(1500);
        console.log(1);

        await page.goto("https://www.abhibus.com/");
        await page.waitForTimeout(5000);
        console.log(2);

        await page.getByRole("textbox", { name: "Leaving From" }).click();
        await page
          .getByRole("textbox", { name: "Leaving From" })
          .fill(route.abhiBusSource);
        await page.waitForTimeout(5000);

        await page.waitForSelector(
          "div.auto-complete-drop-down .auto-complete-list"
        );
        await page.click(
          ".auto-complete-list .auto-complete-list-item >> nth=0"
        );
        console.log(3);

        //   await page.getByText('Pune', { exact: true }).click();
        await page.getByRole("textbox", { name: "Going To" }).click();

        await page
          .getByRole("textbox", { name: "Going To" })
          .fill(route.abhiBusDestination);
        await page.waitForTimeout(5000);
        await page.waitForSelector(
          "div.auto-complete-drop-down .auto-complete-list"
        );
        await page.click(
          ".auto-complete-list .auto-complete-list-item >> nth=0"
        );
        //   await page.getByRole('listitem').filter({ hasText: 'NagpurMaharashtra' }).locator('small').click();
        // await page.getByRole('button', { name: 'Today' }).click();
        await page.click("text=Today");

        await page.waitForTimeout(3000);
        console.log(4);

        await page.getByText("Bus Partner").click();
        await page.getByRole("textbox", { name: "Search here" }).click();
        await page.waitForTimeout(3000);
        console.log(5);

        await page
          .getByRole("textbox", { name: "Search here" })
          .fill("Prasanna - Purple Bus");
        await page.waitForTimeout(3000);
        console.log(6);

        await page
          .locator("#list-filter-option-container")
          .getByRole("checkbox")
          .check();
        await page.waitForTimeout(1500);
        console.log(7);

        let count = 0;
        while (count < 3) {
          console.log("count scroll", count);
          count++;
          await page.evaluate(() =>
            window.scrollTo(0, document.body.scrollHeight)
          );
          await page.waitForTimeout(1000);
        }

        const busCard = await page
          .locator("div#service-cards-container")
          .innerHTML();
        // console.log(busCard)
        const text = convert(busCard, {
          wordwrap: false, // optional: prevents line breaks
          selectors: [
            { selector: "a", options: { hideLinkHrefIfSameAsText: true } },
          ],
        });
        console.log(8);

        response[`${route.abhiBusSource}-${route.abhiBusDestination}`] = text;
        await browser.close();
      } catch (e) {
        console.log("Error in abhibus", e);
        response[`${route.abhiBusSource}-${route.abhiBusDestination}`] =
          "no buses found";
        await browser.close();
      }
      // console.log("res 1234 ",response)
    }

    return { status: 0, msg: "success", data: response };
  } catch (e) {
    console.log(e);
    return { status: 1, msg: "error", data: e };
  }
}
async function searchRedBus(routes) {
  try {
    const { chromium } = require("playwright");
    const { convert } = require("html-to-text");
    let response = {};
    for (const route of routes) {
      response[route.redBusSource + "-" + route.redBusDestination] = {};
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

        await page.getByRole("textbox", { name: "Username" }).click();
        await page.getByRole("textbox", { name: "Username" }).fill("9748");
        await page.getByRole("textbox", { name: "Username" }).press("Tab");
        await page.getByRole("textbox", { name: "Password" }).click();
        await page
          .getByRole("textbox", { name: "Password" })
          .fill("prasannapurple");
        await page.getByRole("button", { name: "Login", exact: true }).click();
        console.log(2);
        //QuickFundBanner---cross---2Mp_5
        await page.locator('.QuickFundBanner---cross---2Mp_5').click();
        await page.locator('role=button[name="Skip"]').click();
        console.log(3);

        await page.hover("aside.SideNav---sideNav---3QZiY ");

        await page.locator('role=link[name="R & R"]').click();
        await page.waitForTimeout(5000);
        console.log(4);

        // await page.click("#servicewise_tab")
        await page.waitForTimeout(1000);
        const inputSelector = 'input[placeholder="Source"]';
        await page.waitForSelector(inputSelector);
        await page.click(inputSelector);
        console.log(5);

        await page.waitForTimeout(2000);
        await page.fill(inputSelector, route.redBusSource);
        await page.waitForTimeout(2000);
        await page
          .locator("#react-autowhatever-1 #react-autowhatever-1--item-0")
          .click();
        await page.waitForTimeout(2000);

        const inputSelector1 = 'input[placeholder="Destination"]';

        await page.waitForSelector(inputSelector1);
        await page.click(inputSelector1);
        console.log(6);

        await page.waitForTimeout(2000);
        await page.fill(inputSelector1, route.redBusDestination);
        await page
          .locator("#react-autowhatever-1 #react-autowhatever-1--item-0")
          .click();
        await page.waitForTimeout(2000);

        const filterBtnSelector = 'button:has-text("Filter")';
        await page.waitForSelector(filterBtnSelector, { state: "visible" });
        await page.click(filterBtnSelector);
        console.log(7);

        await page.waitForTimeout(2000);

        let count = 0;
        while (count < 3) {
          count++;
          await page.evaluate(() =>
            window.scrollTo(0, document.body.scrollHeight)
          );
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
          response[route.redBusSource + "-" + route.redBusDestination][
            `Bus ${i + 1}`
          ] = textContent + "\n\n";

          // Click the calendar button inside the card
          const calendarButton = await card.$(
            ".ServiceWise---calendar---22hhI"
          );
          if (calendarButton) {
            try {
              await Promise.all([
                // Trigger the API call
                calendarButton.click(),

                // Wait for the specific API call to complete
                page.waitForResponse(
                  (response) =>
                    response
                      .url()
                      .includes("/win/api/ratingsReviews/getSrpRank") &&
                    response.status() === 200
                ),
              ]);

              // Wait for ranking popup
              const rankSelector = 'div[class*="RNRCalendar---rankTextDiv"]';
              await page.waitForSelector(rankSelector, { timeout: 5000 });

              const rankElements = await page
                .locator(rankSelector)
                .allTextContents();
              console.log(`\nService ${i + 1} Rankings:`);
              rankElements.forEach((rank) => console.log(rank));
              if (rankElements.length > 0) {
                response[route.redBusSource + "-" + route.redBusDestination][
                  `Bus ${i + 1}`
                ] += "\n\nSrp " + rankElements[0] + "\n\n";
              }

              // Close the popup RNRCalendar---closeDiv---20D9a
              await page
                .locator('div[class*="RNRCalendar---headerDiv"] >> nth=-1')
                .click();
              await page.locator("div.RNRCalendar---closeDiv---20D9a").click();
              await page.waitForTimeout(1000);
            } catch (e) {
              console.log("Popup did not appear in time.");
              response[route.redBusSource + "-" + route.redBusDestination][
                `Bus ${i + 1}`
              ] = "no buses found";
            }
          }
        }

        await browser.close();
      } catch (e) {
        console.log("Error in abhibus", e);
        response[`${route.redBusSource}-${route.redBusDestination}`] =
          "no buses found";
        await browser.close();
      }
      // console.log("res 1234 ",response)
    }

    return { status: 0, msg: "success", data: response };
  } catch (e) {
    console.log(e);
    return { status: 1, msg: "error", data: e };
  }
}

// Start the Server
app.listen(PORT, () => {
  console.log(`🚀 Server running on http://localhost:${PORT}`);
});
