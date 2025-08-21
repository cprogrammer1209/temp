const express = require("express");
const bodyParser = require("body-parser");
const cors = require("cors");
const puppeteer = require("puppeteer");
const path = require("path");
const fs = require("fs");
const { chromium } = require("playwright");
const { convert } = require("html-to-text");
const multer = require("multer");
const axios = require("axios");
const FormData = require("form-data");
const https = require("https");
const { MongoClient } = require("mongodb");


const agent = new https.Agent({ rejectUnauthorized: false });

const app = express();
const PORT = 3000;
const storage = multer.memoryStorage();
const upload = multer({ storage });

const wait = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

// Middleware
app.use(bodyParser.json({ limit: "10mb" })); // Allows sending large HTML content
app.use(cors()); // Enable CORS for external requests

const API_1 = "https://demo.aiqod.com:3443/gibots-api/bots/triggerProcess"; // replace with real URL
const API_2 = "https://demo.aiqod.com:3443/gibots-api/bots/extractionStatus"; // replace with real URL
const API_3 = "https://demo.aiqod.com:3443/gibots-api/bots/getJSON";

app.post("/aiqod-api/process-file", upload.any(), async (req, res) => {
  console.log("Inside the API");
  try {
    console.log("Body  ", req.body, " Length ", JSON.stringify(req.body));
    console.log("Files  ", req.files);

    // Step 1: Upload to API 1
    console.log(1);

    const formData = new FormData();

    const filesGroupedByFieldname = {};
    for (const file of req.files) {
      if (!filesGroupedByFieldname[file.fieldname]) {
        filesGroupedByFieldname[file.fieldname] = [];
      }
      filesGroupedByFieldname[file.fieldname].push(file);
    }
    console.log("data ", filesGroupedByFieldname);

    for (const fieldname in filesGroupedByFieldname) {
      const files = filesGroupedByFieldname[fieldname];
      for (const file of files) {
        if (file.buffer) {
          formData.append(fieldname, file.buffer, {
            filename: file.originalname,
          });
        } else {
          throw new Error(
            `File buffer is undefined for file: ${file.originalname}`
          );
        }
      }
    }
    for (const key in req.body) {
      formData.append(key, req.body[key]);
    }
    console.log(3, " hello ");
    console.log("token ", req.headers["authorization"]);

    let uploadRes = await axios.post(API_1, formData, {
      headers: {
        // ...req.headers,
        selectedorgid: "662b515be421fedde2247c47",
        Authorization: req.headers["authorization"] || "",
      },
      httpsAgent: agent,
    });
    //  uploadRes = await uploadRes.json()
    console.log(
      "Response from 1st API ",
      uploadRes.data.data.data[0].fileRefNum
    );
    const uniqueId = uploadRes.data.data.data[0].fileRefNum;

    // Step 2: Poll API 2
    let status = "fileQueued";
    let apiBody = {
      referenceNo: uniqueId,
    };
    let count = 0;
    while (status !== "Success") {
      const statusRes = await axios.post(API_2, apiBody, {
        headers: {
          // ...req.headers,
          selectedorgid: "662b515be421fedde2247c47",
          Authorization: req.headers["authorization"] || "",
        },
        httpsAgent: agent,
      });

      console.log("statusRes.data ", statusRes.data);
      status = statusRes.data.data.status;
      console.log(status);
      if (status !== "Success") {
        count++;
        console.log("wait for 60s   ", count);
        await wait(60000);
      } // wait 60 seconds
      if (count > 15) {
        res.status(500).json({ error: "Processing failed" });
        break;
      }
    }

    // Step 3: Call API 3 for final result
    const finalRes = await axios.post(API_3, apiBody, {
      headers: {
        // ...req.headers,
        selectedorgid: "662b515be421fedde2247c47",
        Authorization: req.headers["authorization"] || "",
      },
      httpsAgent: agent,
    });
    console.log("3rd response ", finalRes.data);

    // Return final result to client
    res.json(finalRes.data);
  } catch (err) {
    console.error("Error:", err.message);
    res.status(500).json({ error: "Processing failed" });
  }
});

/**
 * Function to generate a PDF from HTML content.
 * @param {string} htmlContent - The HTML content as a string.
 * @param {string} outputFilePath - The path where the PDF will be saved.
 */
async function generatePDF(htmlContent, outputFilePath) {
  try {
    // const browser = await puppeteer.launch({
    //     args: ["--no-sandbox", "--disable-setuid-sandbox"],
    //     headless: "new",
    //     executablePath: "/usr/bin/google-chrome"  // Ensures it uses the installed Chrome
    // });
    const browser = await puppeteer.launch({
      args: ["--no-sandbox", "--disable-setuid-sandbox"],
      executablePath: "/usr/bin/google-chrome",
      headless: "new",
    });
    const page = await browser.newPage();
    await page.setContent(htmlContent, { waitUntil: "networkidle0" });

    await page.pdf({
      path: outputFilePath,
      format: "A4",
      printBackground: true,
      displayHeaderFooter: false,
      preferCSSPageSize: true,
    });

    await browser.close();
    console.log(`✅ PDF successfully generated: ${outputFilePath}`);
  } catch (error) {
    console.error("❌ Error generating PDF:", error);
    throw error;
  }
}

// POST API to Generate PDF
app.post("/generate-pdf", async (req, res) => {
  try {
    const { htmlContent } = req.body;
    console.log(`Running Node.js version: ${process.version}`);
    if (!htmlContent) {
      return res
        .status(400)
        .json({ error: "Missing htmlContent in request body" });
    }

    const outputFilePath = path.join(__dirname, "output.pdf");
    //let temp = await fs.readFileSync(htmlContent, 'utf8');
    await generatePDF(htmlContent, outputFilePath);

    // Send the PDF as a response
    res.download(outputFilePath, "generated.pdf", (err) => {
      if (err) {
        console.error("❌ Error sending file:", err);
        res.status(500).json({ error: "Failed to send PDF file" });
      } else {
        console.log("📩 PDF sent successfully");
        //fs.unlinkSync(outputFilePath); // Delete the file after sending
      }
    });
  } catch (error) {
    res
      .status(500)
      .json({ error: "Error generating PDF", details: error.message });
  }
});

app.post("/playwright", async (req, res) => {
  try {
    const { input } = req.body;
    console.log(`Running Node.js version: ${process.version}`);
    if (input == "" || !input) {
      return res
        .status(400)
        .json({ error: "Missing htmlContent in request body" });
    }
    let bus = input.bus;
    let route = input.route;

    if (route.length == 0) {
      return res.status(400).json({ error: "Missing route in request body" });
    }
    let response = {};
    if (bus == "paytm") {
      response = await searchPaytm(route);
    }

    return res.status(200).json(response);
  } catch (error) {
    res
      .status(500)
      .json({ error: "Error generating PDF", details: error.message });
  }
});

async function searchPaytm(routes) {
  try {
    let response = {};
    for (const route of routes) {
      response[route.source + "-" + route.destination] = "";
      const browser = await chromium.launch({
        headless: true,
        args: ["--no-sandbox", "--disable-setuid-sandbox"],
        executablePath: "/usr/bin/google-chrome",
      });
      const context = await browser.newContext();
      const page = await context.newPage();

      await page.goto("https://tickets.paytm.com/bus/");
      await page.getByRole("textbox", { name: "From" }).click();
      await page.getByRole("textbox", { name: "From" }).fill(route.source);
      // await page.getByText('PuneMaharashtra', { exact: true }).click();
      await page.waitForSelector("#source-section .dcrjM");
      await page.click("#source-section .dcrjM >> nth=0");
      await page.getByRole("textbox", { name: "To" }).click();
      await page.getByRole("textbox", { name: "To" }).fill(route.destination);

      await page.waitForSelector("#destination-section .dcrjM");
      await page.click("#destination-section .dcrjM >> nth=0");

      // await page.getByText('NagpurMaharashtra', { exact: true }).click();
      await page.getByRole("button", { name: "Search Buses" }).click();
      await page.waitForTimeout(5000);
      await page.getByRole("textbox", { name: "Search Operators" }).click();
      await page
        .getByRole("textbox", { name: "Search Operators" })
        .fill("pras");
      await page
        .locator("div")
        .filter({ hasText: /^Bus operatorsPrasanna - Purple Bus$/ })
        .getByLabel("unchecked")
        .click();

      const busCard = await page.locator("div.-iAp6").innerHTML();
      // console.log(busCard)
      const text = convert(busCard, {
        wordwrap: false, // optional: prevents line breaks
        selectors: [
          { selector: "a", options: { hideLinkHrefIfSameAsText: true } },
        ],
      });

      response[route.source + "-" + route.destination] = text;
    }

    return { status: 0, msg: "success", data: response };
  } catch (e) {
    console.log(e);
    return { status: 1, msg: "error", data: e };
  }
}

app.post("/testing", async (req, res) => {
  try {
    console.log(`Running Node.js version: ${process.version}`);

    return res.status(200).json("Hello");
  } catch (error) {
    res
      .status(500)
      .json({ error: "Error generating PDF", details: error.message });
  }
});

app.post("/aiqod-api/whatsapp", async (req, res) => {
  console.log("Inside the API");
  try {
    console.log("Incoming webhook message:", JSON.stringify(req.body, null, 2));
    res.sendStatus(200);
    const url  = "mongodb://dev-SU:mdhdiIQTS@172.168.1.199:27017/?authSource=aiqod-dev"
    const client = new MongoClient(url);
    await client.connect();
    let db = await client.db("aiqod-dev");
    let datas = await db.collection("whatsappOrderManagement").findOne({})
    console.log("datas : ",datas)
    const incomingMessage = req.body.entry[0].changes[0].value
    
    const wa_id = incomingMessage.contacts[0]?.wa_id;
    const messageText = incomingMessage.messages[0]?.text?.body || "";
    const messageId = incomingMessage.messages[0]?.id;
    const timestamp = new Date();

    console.log("wa_id : ",wa_id)
    console.log("messageText : ",messageText)
    console.log("messageId : ",messageId)
    console.log("timestamp : ",timestamp)
  } catch (err) {
    console.error("Error:", err);
    res.status(500).json({ error: "Processing failed" });
  }
});

app.get("/aiqod-api/whatsapp", async (req, res) => {
  console.log("Inside the API");
  try {
    console.log("Incoming webhook message:", JSON.stringify(req.body, null, 2));
    const VERIFY_TOKEN = "whatsapp_webhook_token_2025";

    const mode = req.query["hub.mode"];
    const token = req.query["hub.verify_token"];
    const challenge = req.query["hub.challenge"];

    if (mode && token === VERIFY_TOKEN) {
      res.status(200).send(challenge);
    } else {
      res.sendStatus(403);
    }
  } catch (err) {
    console.error("Error:", err);
    res.status(500).json({ error: "Processing failed" });
  }
});

// Start the Server
app.listen(PORT, () => {
  console.log(`🚀 Server running on http://localhost:${PORT}`);
});
