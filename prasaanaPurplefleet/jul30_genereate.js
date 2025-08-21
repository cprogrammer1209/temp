const express = require("express");
const bodyParser = require("body-parser");
const cors = require("cors");
const path = require("path");
const fs = require("fs/promises");
const { chromium } = require("playwright");
const { GoogleGenAI } = require("@google/genai");
const { DateTime } = require("luxon");
const axios = require("axios");
const XLSX = require("xlsx");
const { MongoClient, ObjectId } = require("mongodb");

// import { DateTime } from "luxon";
// import express from "express";
// import bodyParser from "body-parser";
// import cors from "cors";
// import path from "path";
// import fs from "fs/promises";
// import { chromium } from "playwright";
// import axios from "axios";
// import XLSX from "xlsx";
// import { MongoClient, ObjectId } from "mongodb";
// import { GoogleGenAI } from "@google/genai";
// import { group } from "console";

const uriSrc =
  "mongodb://staging:stage789@172.168.1.19:27017/?authSource=aiqod-staging";
const client1 = new MongoClient(uriSrc);

// Gemini API Setup
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

// app.post("/scrapper/playwright", async (req, res) => {
//   try {
//     await client1.connect();
//     const db = client1.db("aiqod-staging");
//     const { input, orgId, subscriberId, userId } = req.body;

//     if (!input || !orgId || !subscriberId || !userId) {
//       return res.status(400).json({ error: "Missing required fields" });
//     }

//     const routes = await db.collection("prasannaPurpleBuses").find().toArray();

//     if (!routes || routes.length === 0) {
//       return res.status(400).json({ error: "Missing route in request body" });
//     }
//     console.log("Routes to process: ", routes);
//     ``;

//     // Respond immediately that processing has started
//     res.status(202).json({ message: "Processing started" });

//     let response = {};
//     for (const route of routes) {
//       response[route["From City"] + "-" + route["To City"]] = {};
//       route.paytmBusSource = route["From City"];
//       route.paytmBusDestination = route["To City"];

//       // 1. Scrape Paytm

//       try {
//         const resData = await searchPaytm(
//           route,
//           response[route["From City"] + "-" + route["To City"]]
//         );
//       } catch (e) {
//         console.log("Error in paytm", e);
//         response["paytm"] = "no buses found";
//       }

// 2. Scrape Abhibus
// try {
//   const resData = await searchAbhiBus(
//     route,
//     response[route.redBusSource + "-" + route.redBusDestination]
//   );
// } catch (e) {
//   console.log("Error in abhibus", e);
//   response["abhibus"] = "no buses found";
// }

// 3. Scrape Redbus
// try {
//   const resData = await searchRedBus(
//     route,
//     response[route.redBusSource + "-" + route.redBusDestination]
//   );
// } catch (e) {
//   console.log("Error in redbus", e);
//   response["redbus"] = "no buses found";
// }
// }
// console.log("Response ", response);
// let convertExcel = await convertExecel(response);
// let excelFilePath = convertExcel["publicUrl"];
// console.log("Excel file path ", excelFilePath);
//--------------------------------

// function timeStringToMinutes(timeStr) {
//   let dt = DateTime.fromFormat(timeStr, "hh:mm a");
//   return dt.hour * 60 + dt.minute;
// }

function getUniqueRoutes_bkp(routes) {
  const seen = new Set();
  const uniqueRoutes = [];

  for (const route of routes) {
    const from = route["From City"];
    const to = route["To City"];
    const time = route["Time"];
    const key = `${from}___${to}___${time}`;

    if (!seen.has(key)) {
      seen.add(key);
      uniqueRoutes.push(route);
    }
  }

  return uniqueRoutes;
}

async function getUniqueRoutes(db, coll) {
  try {
    const docs = await db
      .collection(coll)
      .aggregate([
        {
          $group: {
            _id: {
              fromCity: "$From City",
              toCity: "$To City",
            },
          },
        },
        {
          $project: {
            _id: 0,
            fromCity: "$_id.fromCity",
            toCity: "$_id.toCity",
          },
        },
      ])
      .toArray();
    if (docs.length == 0) {
      throw new Error("no docs found");
    }
    return { status: 0, msg: "success", output: docs };
  } catch (e) {
    console.error("error in getUniqueroutes ", e);
    return { status: 1, msg: e, output: [] };
  }
}

function findMatchingSchedule(subTimeStr, dbRecords, fromCity, toCity) {
  let filteredDoc = dbRecords.filter(
    (item) =>
      item["Time"] == subTimeStr &&
      item["FromCityName"] == fromCity &&
      item["ToCityName"] == toCity
  );

  return filteredDoc[0];
}

//paytm and abhibus convert excel

// function convertExcel(jsonData) {
//   const timestamp = Date.now();
//   const formattedDate = new Date()
//     .toLocaleDateString("en-GB")
//     .replaceAll("/", "-");

//   const rows = [];

//   for (const mainRoute in jsonData) {
//     const timeBlocks = jsonData[mainRoute];

//     // Extract subroute-level static ratings like Abhibus
//     const staticRatings = {};
//     for (const key in timeBlocks) {
//       // Skip if this is a time string (like 10:00 PM)
//       if (!/AM|PM/i.test(key)) {
//         const subroute = key;
//         for (const subTime in timeBlocks[subroute]) {
//           const entry = timeBlocks[subroute][subTime];
//           staticRatings[`${subroute}-${subTime}`] = {
//             paytmBus: entry?.paytmBus ?? "NA",
//             abhibus: entry?.abhibus ?? "NA",
//           };
//         }
//       }
//     }

//     // Loop through actual time blocks
//     for (const mainTime in timeBlocks) {
//       if (!/AM|PM/i.test(mainTime)) continue;

//       const subroutes = timeBlocks[mainTime];

//       for (const subroute in subroutes) {
//         const times = subroutes[subroute];
//         for (const subTime in times) {
//           const entry = times[subTime];

//           // Match any static rating (like abhibus)
//           const key = `${subroute}-${subTime}`;
//           const staticEntry = staticRatings[key] || {};

//           rows.push({
//             "Main Route": mainRoute,
//             "Main Time": mainTime,
//             Subroute: subroute,
//             "Subroute Time": subTime,
//             paytmBus: entry?.paytmBus ?? staticEntry.paytmBus ?? "NA",
//             abhibus: entry?.abhibus ?? staticEntry.abhibus ?? "NA",
//           });
//         }
//       }
//     }
//   }

//   // Convert to worksheet

//   const ws = XLSX.utils.json_to_sheet(rows);

//   const wb = XLSX.utils.book_new();
//   XLSX.utils.book_append_sheet(wb, ws, "Bus Ratings");

//   // Save
//   const filename = `excel-${timestamp}-${formattedDate}.xlsx`;
//   const filepath = path.join("E:/test/public/excel", "ExcelSheets", filename);
//   const publicUrl = `https://automation.aiqod.com/public/excel/ExcelSheets/${filename}`;

//   XLSX.writeFile(wb, filepath);

//   console.log(" Excel saved to", filepath);

//   return { jsonData: rows, publicUrl };
// }

function convertExcel(jsonData) {
  const timestamp = Date.now();
  const formattedDate = new Date()
    .toLocaleDateString("en-GB")
    .replaceAll("/", "-");

  const rows = [];

  for (const mainRoute in jsonData) {
    const timeBlocks = jsonData[mainRoute];

    // Extract subroute-level static ratings (non-time keys)
    const staticRatings = {};
    for (const key in timeBlocks) {
      if (!/AM|PM/i.test(key) && key !== "Not Found") {
        const subroute = key;
        for (const subTime in timeBlocks[subroute]) {
          const entry = timeBlocks[subroute][subTime];
          staticRatings[`${subroute}-${subTime}`] = {
            paytmBus: entry?.paytmBus ?? "NA",
            abhibus: entry?.abhibus ?? "NA",
            redbus: entry?.redbus ?? "NA", // ✅ Added redbus
            srpRating: entry?.srpRating ?? "NA", // ✅ Added srpRating
          };
        }
      }
    }

    // Time-based ratings block
    for (const mainTime in timeBlocks) {
      if (!/AM|PM/i.test(mainTime) && mainTime !== "Not Found") continue;

      const subroutes = timeBlocks[mainTime];

      for (const subroute in subroutes) {
        const times = subroutes[subroute];

        for (const subTime in times) {
          const entry = times[subTime];
          const key = `${subroute}-${subTime}`;
          const staticEntry = staticRatings[key] || {};

          rows.push({
            "Main Route": mainRoute,
            "Main Time": mainTime,
            Subroute: subroute,
            "Subroute Time": subTime,
            paytmBus: entry?.paytmBus ?? staticEntry.paytmBus ?? "NA",
            abhibus: entry?.abhibus ?? staticEntry.abhibus ?? "NA",
            redbus: entry?.redbus ?? staticEntry.redbus ?? "NA",
            redbus_srp: entry?.srpRating ?? staticEntry.srpRating ?? "NA",
          });
        }
      }
    }
  }

  // Convert to Excel
  const ws = XLSX.utils.json_to_sheet(rows);
  const wb = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(wb, ws, "Bus Ratings");

  const filename = `excel-${timestamp}-${formattedDate}.xlsx`;
  const filepath = path.join("E:/test/public/excel/ExcelSheets", filename);
  const publicUrl = `https://automation.aiqod.com/public/excel/ExcelSheets/${filename}`;

  XLSX.writeFile(wb, filepath);

  console.log("✅ Excel saved to", filepath);
  return { jsonData: rows, publicUrl };
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

app.post("/scrapper/playwright", async (req, res) => {
  try {
    const { orgId, subscriberId, userId, config } = req.body;

    if (!orgId || !subscriberId || !userId) {
      console.error("Missing required fields in request body");

      return res.status(400).json({ error: "Missing required fields" });
    }

    res.status(202).json({ message: "Processing started" });

    let configData;
    try {
      configData = typeof config === "string" ? JSON.parse(config) : config;
    } catch (e) {
      console.error("Failed to parse config JSON:", e.message);
      return res.status(400).json({ error: "Invalid config JSON" });
    }

    console.log(" configData parsed:", configData);

    // console.log("Config Data: ", configData);

    const uriSrc = configData.mongourl;
    const client1 = new MongoClient(uriSrc);
    await client1.connect();

    const dbs = await client1.db(configData.dbname);

    await client1.connect();

    const db = client1.db("aiqod-staging");

    const mongoDocs = await db
      .collection("_prasannaPurpleBuses")
      .find({})
      .toArray();
    const routesdb = await getUniqueRoutes(db, "_prasannaPurpleBuses");

    //const routeRedbus = await getShedulecode(db, "_prasannaPurpleBuses");

    const routes = [
      {
        fromCity: "Nagpur",
        toCity: "Mumbai",
      },
      {
        fromCity: "Nagpur",
        toCity: "Amravati",
      },
      {
        fromCity: "Nagpur",
        toCity: "Akola",
      },
      {
        fromCity: "Akola",
        toCity: "Mumbai",
      },
      {
        fromCity: "Amravati",
        toCity: "Mumbai",
      },
      { fromCity: "Pune", toCity: "Ahmednagar" },
      { fromCity: "Pune", toCity: "Akola" },
      { fromCity: "Pune", toCity: "Aurangabad" },
      { fromCity: "Pune", toCity: "Chikhli" },
      { fromCity: "Pune", toCity: "Khamgaon" },
      { fromCity: "Pune", toCity: "Shegaon" },
      { fromCity: "Ahmednagar", toCity: "Akola" },
      { fromCity: "Ahmednagar", toCity: "Chikhli" },
      { fromCity: "Ahmednagar", toCity: "Khamgaon" },
      { fromCity: "Ahmednagar", toCity: "Shegaon" },
      // {
      //   fromCity: "Pune",
      //   toCity: "Nagpur",
      // },

      // {
      //   fromCity: "Gorakhpur",
      //   toCity: "Indore",
      // },
      // {
      //   fromCity: "Chandrapur",
      //   toCity: "Pune",
      // },
      // {
      //   fromCity: "Pune",
      //   toCity: "Mandu-Ujjain-Omkareshwar Darshan",
      // },
    ];

    let RedbusRoute = [
      {
        "SR No": 1326,
        RouteName:
          "Nagpur To Mumbai via Amravati 2x1(36) AC Sleeper, Prasanna - Purple Bus",
        Time: "09:15 PM",
        "From City": "Amravati",
        "To City": "Mumbai",
        "Schedule Code": "118606-NagpurMumbai6:30 PM",
        "Bus Arrangement Name": "36 BERTH 2X1 AC SLEEPER",
        RouteID: 54694,
        RouteTimeID: 118606,
        "Status ": "Active",
        phone_num: "",
        subscriberId: "5beaabd82ac6767c86dc311c",
        orgId: "5c495dbfffa2a85b2c19a77f",
      },

      // {
      //   "SR No": 1354,
      //   RouteName:
      //     "Pune To Mandu-Ujjain-Omkareshwar Darshan, Prasanna - Purple Bus",
      //   Time: "07:45 PM",
      //   "From City": "Pune",
      //   "To City": "Mandu-Ujjain-Omkareshwar Darshan",
      //   "Schedule Code":
      //     "119254 - Pune To Mandu-Ujjain-Omkareshwar Darshan - 07:45 PM",
      //   "Bus Arrangement Name": "36 BERTH 2X1 AC SLEEPER",
      //   RouteID: 58607,
      //   RouteTimeID: 119254,
      //   "Status ": "Active",
      //   phone_num: "",
      //   subscriberId: "5beaabd82ac6767c86dc311c",
      //   orgId: "5c495dbfffa2a85b2c19a77f",
      // },
      // {
      //   "SR No": 1262,
      //   RouteName:
      //     "Gorakhpur To Indore Via Ayodhya-Lucknow, Prasanna - Purple Bus",
      //   Time: "04:00 PM",
      //   "From City": "Gorakhpur",
      //   "To City": "Guna",
      //   "Schedule Code": "118583-GorakhpurIndore4:00 PM",
      //   "Bus Arrangement Name": "36 BERTH 2X1 AC SLEEPER",
      //   RouteID: 57757,
      //   RouteTimeID: 118583,
      //   "Status ": "Active",
      //   phone_num: "",
      //   subscriberId: "5beaabd82ac6767c86dc311c",
      //   orgId: "5c495dbfffa2a85b2c19a77f",
      // },

      // {
      //   "SR No": 1328,
      //   RouteName:
      //     "Pune To Nagpur AC Sleeper 2x1(30) A/C Sleeper, Prasanna - Purple Bus",
      //   Time: "07:30 PM",
      //   "From City": "Pune",
      //   "To City": "Ahmednagar",
      //   "Schedule Code": "118613-PuneNagpur7:30 PM",
      //   "Bus Arrangement Name": "36 BERTH 2X1 AC SLEEPER",
      //   RouteID: 5150,
      //   RouteTimeID: 118613,
      //   "Status ": "Active",
      //   phone_num: "",
      //   subscriberId: "5beaabd82ac6767c86dc311c",
      //   orgId: "5c495dbfffa2a85b2c19a77f",
      // },

      {
        "SR No": 12,
        RouteName: "Pune To Akola 2x1 (36) Ac Sleeper, Prasanna - Purple Bus",
        Time: "12:15 AM",
        "From City": "Ahmednagar",
        "To City": "Chikhli",
        "Schedule Code": "13181 - Pune To Akola - 10:00 PM",
        "Bus Arrangement Name": "36 BERTH 2X1 AC SLEEPER",
        RouteID: 5250,
        RouteTimeID: 13181,
        "Status ": "Active",
        phone_num: "",
        subscriberId: "5beaabd82ac6767c86dc311c",
        orgId: "5c495dbfffa2a85b2c19a77f",
      },
      //   {
      //     "SR No": 77,
      //     RouteName:
      //       "Chandrapur To Pune 2X1 A/C Sleeper Via Samruddhi Highway, Prasanna - Purple Bus",
      //     Time: "04:00 PM",
      //     "From City": "Bhadrawati",
      //     "To City": "Pune",
      //     "Schedule Code": "13333 - Chandrapur To Pune - 04:30 PM",
      //     "Bus Arrangement Name": "36 BERTH 2X1 AC SLEEPER",
      //     RouteID: 5341,
      //     RouteTimeID: 13333,
      //     "Status ": "Active",
      //     phone_num: "",
      //     subscriberId: "5beaabd82ac6767c86dc311c",
      //     orgId: "5c495dbfffa2a85b2c19a77f",
      //   },
    ];

    function extractFromToFromRouteName(routeName) {
      const match = routeName.match(
        /^(.+?)\s+To\s+(.+?)(?:\s+Via|\s+\d+|\s+AC|\s+Non|,|$)/i
      );
      if (!match) return { from: "Unknown", to: "Unknown" };

      return {
        from: match[1].trim(),
        to: match[2].trim(),
      };
    }

    function extractFromToFromScheduleCode(scheduleCode) {
      try {
        // Case 1: well-formatted with " - Pune To Nagpur - 07:00 PM"
        if (scheduleCode.includes("To")) {
          const parts = scheduleCode.split("-");
          const routePart = parts.slice(1, -1).join("-").trim();

          const match = routePart.match(/(.+?)\s+To\s+(.+)/i);
          if (match) {
            return {
              from: match[1].trim(),
              to: match[2].trim(),
            };
          }
        }

        // Case 2: compressed format e.g. "119060-PuneNagpur8:30 PM"
        const compact = scheduleCode.replace(/^[^A-Za-z]+-/, ""); // Remove ID and dash
        const timeMatch = compact.match(/(\d{1,2}:\d{2}\s*(?:AM|PM))/i);
        const timePart = timeMatch ? timeMatch[0] : "";

        const routeOnly = compact.replace(timePart, "").trim();

        // Try to split compressed route (e.g., PuneNagpur)
        const routeSplit = routeOnly.match(/^([A-Z][a-z]+)([A-Z].+)$/);
        if (routeSplit) {
          return {
            from: routeSplit[1],
            to: routeSplit[2].replace(/([A-Z])/g, " $1").trim(),
          };
        }

        return { from: "Unknown", to: "Unknown" };
      } catch {
        return { from: "Unknown", to: "Unknown" };
      }
    }

    let response = {};
    for (const route of routes) {
      route.paytmBusSource = route["fromCity"];
      route.paytmBusDestination = route["toCity"];
      route.abhiBusSource = route["fromCity"];
      route.abhiBusDestination = route["toCity"];

      try {
        await searchPaytm(route, response, mongoDocs);
      } catch (e) {
        console.log("Error in paytm", e);
        // response["paytm"] = "no buses found";
      }

      try {
        await searchAbhiBus(route, response, mongoDocs);
      } catch (e) {
        console.log("Error in abhibus", e);
        // response["abhibus"] = "no buses found";
      }
    }

    for (const route of RedbusRoute) {
      let MainrouteName = route["Schedule Code"];

      let from, to;

      if (route.RouteName) {
        ({ from, to } = extractFromToFromRouteName(route.RouteName));
      }

      // Step 2: Fallback to Schedule Code if needed
      if (!from || !to || from === "Unknown" || to === "Unknown") {
        ({ from, to } = extractFromToFromScheduleCode(route["Schedule Code"]));
      }

      // Step 3: Assign to route for RedBus search
      route.redBusSource = from;
      route.redBusDestination = to;

      // Step 4: Add key for structured response
      const routeKey = `${from} - ${to}`;

      // // Call RedBus scraper
      try {
        await searchRedBus(route, response, mongoDocs);
      } catch (e) {
        console.log("Error in redbus", e);
        // response[routeKey].redbus = "no buses found";
        // if (!response[routeKey]) response[routeKey] = {};
        // response[routeKey].redbus = "no buses found";
      }
    }

    for (const key in response) {
      if (
        typeof response[key] === "object" &&
        Object.keys(response[key]).length === 0
      ) {
        delete response[key];
      }
    }

    console.log("Scraped  Response: ", JSON.stringify(response, null, 2));

    let convertExceal = convertExcel(response);
    console.log("convertExceal: ", convertExceal);

    let rows = convertExceal["jsonData"];
    console.log("Rows to insert: ", rows.length);
    console.log("Rows to insert: ", rows);
    rows = rows.map((row) => {
      return {
        ...row,
        isDeleted: false,
        createdAt: new Date(),
        updatedAt: new Date(),
        orgId: new ObjectId(orgId),
        subscriberId: new ObjectId(subscriberId),
        userId: new ObjectId(userId),
      };
    });

    if (rows.length > 0) {
      const collection = dbs.collection("purpleRatings_new");
      await collection.insertMany(rows);
      console.log("Ratings inserted successfully");
    }

    // process triggering

    let excelFilePath = convertExceal["publicUrl"];
    console.log("Excel file path ", excelFilePath);

    const url = `${configData.apirUrl}/gibots-api/bots/triggerProcessNew`;
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

    console.log("Excel file path ", excelFilePath);
  } catch (err) {
    console.log("Error: ", err);
  }
});

// reviews part
//     try {
//       const reviews = await readUserReview();

//       if (!reviews || reviews.length === 0) {
//         console.log("No reviews found to process");
//         throw new Error("No reviews found");
//       }
//       const reviewsAboveThree = reviews.filter((review) => review.rating > 3);
//       let reviewsBelowThree = reviews.filter((review) => review.rating <= 3);

//       let reviewsToInsert = reviewsBelowThree.map((review) => {
//         return { ...review, escalate: "yes" };
//       });
//       let responseFromGenAi = await toneAnalysis(reviewsAboveThree);
//       reviewsToInsert = [...reviewsToInsert, ...responseFromGenAi];
//       reviewsToInsert = reviewsToInsert.map((review) => {
//         return {
//           ...review,
//           description: `Mobile : ${review.Mobile},\n
//           PNR: ${review.PNR}, \n
//           Journey SRC: ${review.journeySRC},  Journey DST: ${review.journeyDST},\n
//           Customer Name: ${review.customerName},\n
//           Customer Review: ${review.customerReview},\n
//           Review Posted Date: ${review.reviewPostedDate},\n
//           Journey Date: ${review.journeyDate},\n
//           Rating: ${review.rating}
//           `,
//           passenger_name: review.customerName,
//           isDeleted: false,
//           createdAt: new Date(),
//           updatedAt: new Date(),
//           orgId: new ObjectId(orgId),
//           subscriberId: new ObjectId(subscriberId),
//           userId: new ObjectId(userId),
//         };
//       });
//       console.log("Reviews to insert: ", reviewsToInsert);
//       await db
//         .collection("purpleReviews")
//         .updateMany({}, { $set: { isDeleted: true } });
//       if (reviewsToInsert.length > 0) {
//         const collection = db.collection("purpleReviews");
//         await collection.insertMany(reviewsToInsert);
//         console.log("Reviews inserted successfully");
//       }
//     } catch (e) {
//       console.log("Error in reading reviews", e);
//     }

//     const url = "http://172.168.1.19:7894/gibots-api/bots/triggerProcess";
//     const options = {
//       orgId: orgId,
//       subscriberId: subscriberId,
//       userId: userId,
//       triggerData: {
//         additionalInfo: [
//           {
//             addToTaskList: false,
//             name: "publicUrl",
//             required: false,
//             label: "publicUrl",
//             value: excelFilePath,
//             id: "0",
//           },
//         ],
//         customerId: "5b8fd401b3930517f134c569",
//         processId: "680627c3eff7f475cf839148",
//         projectId: "680627c3eff7f475cf83914e",
//         taskDesc: "",
//         projectName: "Automatic Prassana Automation",
//         username: "Admin",
//         accessControlList: [
//           {
//             permissionsList: {
//               execute: true,
//               view: true,
//               edit: true,
//               add: true,
//             },
//             controlType: "users",
//             controlName: "Admin",
//             controlId: "5beaabd82ac6767c86dc311e",
//             _id: "67729c4be8ea3efa77dfa76a",
//           },
//           {
//             permissionsList: {
//               execute: true,
//               view: true,
//               edit: true,
//               add: true,
//             },
//             controlType: "users",
//             controlName: "Deepa",
//             controlId: "66eac67c4b94159b93983810",
//             _id: "67729c4be8ea3efa77dfa769",
//           },
//         ],
//       },
//     };
//     await axios.post(url, options);
//     console.log("Process is triggered successfully");
//   } catch (error) {
//     console.log("error ", error);
//     // No res.status here, as response is already sent
//   }
// });

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

    return filteredReviews;
  } catch (e) {
    console.error(" Test failed:", e.message);
    return [];
  } finally {
    await browser.close();
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
  // }
  // async function convertExecel(jsonData) {
  //   let timestamp = Date.now();
  //   const formattedDate = new Date()
  //     .toLocaleDateString("en-GB")
  //     .replaceAll("/", "-"); // dd/mm/yyyy
  //   console.log(formattedDate);
  //   const rows = [];
  //   for (const route in jsonData) {
  //     for (const time in jsonData[route]) {
  //       const entry = jsonData[route][time];
  //       rows.push({
  //         route,
  //         time,
  //         paytmBus: entry.paytmBus || "NA",
  //         abhiBus: entry.abhiBus || "NA",
  //         redBus: entry.redBus || "NA",
  //         srpRanking: entry.srpRanking || "NA",
  //       });
  //     }
  //   }

  // Convert JSON data to worksheet
  const ws = XLSX.utils.json_to_sheet(rows);

  // Create a new workbook with the worksheet
  const wb = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(wb, ws, "Bus Ratings");
  let output = {};

  let filepath = path.join(
    "/home/user/code/excel",
    "ExcelSheets",
    `excel-${timestamp}-${formattedDate}.xlsx`
  );
  output["filepath"] = filepath;
  console.log("first path ", filepath);
  // Write the Excel file to disk
  XLSX.writeFile(wb, filepath);
  let publicUrl =
    "https://deployement.aiqod.com/automation/public/excel/ExcelSheets/" +
    `excel-${timestamp}-${formattedDate}.xlsx`;
  output["publicUrl"] = publicUrl;
  output["jsonData"] = rows;
  console.log("Public URL ", publicUrl);

  return output;
}
async function getDistinctFromToFromScheduleCode(db, coll) {
  try {
    const docs = await db
      .collection(coll)
      .aggregate([
        {
          $group: {
            _id: "$Schedule Code", // Get all unique Schedule Codes
          },
        },
        {
          $project: {
            _id: 0,
            scheduleCode: "$_id",
          },
        },
      ])
      .toArray();

    if (docs.length === 0) throw new Error("No schedule codes found");

    // Now extract from/to for each code
    const uniquePairs = new Set();

    for (const doc of docs) {
      const { from, to } = extractFromToFromScheduleCode(doc.scheduleCode);
      if (from !== "Unknown" && to !== "Unknown") {
        uniquePairs.add(`${from}|||${to}`);
      }
    }

    // Convert set to array of objects
    const result = [...uniquePairs].map((entry) => {
      const [fromCity, toCity] = entry.split("|||");
      return { fromCity, toCity };
    });

    return { status: 0, msg: "success", output: result };
  } catch (e) {
    console.error("Error in getDistinctFromToFromScheduleCode:", e);
    return { status: 1, msg: e.message, output: [] };
  }
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

function injectTopLevelRatings(scrapedData) {
  for (const mainRoute in scrapedData) {
    const subrouteBlocks = scrapedData[mainRoute];

    for (const mainTimeKey in subrouteBlocks) {
      const mainTimeObj = DateTime.fromFormat(mainTimeKey, "hh:mm a");
      const timeBlock = subrouteBlocks[mainTimeKey];

      const [from, to] = mainRoute.split(" To ");
      const expectedSubrouteKey = `${from} - ${to}`;

      let bestPaytm = null;
      let bestAbhibus = null;
      let smallestDiff = 60;

      for (const subroute in timeBlock) {
        const subTimes = timeBlock[subroute];

        for (const subTime in subTimes) {
          const subTimeObj = DateTime.fromFormat(subTime, "hh:mm a");
          const diff = Math.abs(
            mainTimeObj.diff(subTimeObj, "minutes").minutes
          );

          if (diff <= 60 && subroute === expectedSubrouteKey) {
            const ratingBlock = subTimes[subTime];

            if (diff < smallestDiff) {
              if (ratingBlock.paytmBus) bestPaytm = ratingBlock.paytmBus;
              if (ratingBlock.abhibus) bestAbhibus = ratingBlock.abhibus;
              smallestDiff = diff;
            }
          }
        }
      }

      if (bestPaytm !== null) {
        scrapedData[mainRoute][mainTimeKey].paytmBus = bestPaytm;
      }
      if (bestAbhibus !== null) {
        scrapedData[mainRoute][mainTimeKey].abhibus = bestAbhibus;
      }
    }
  }

  return scrapedData;
}

async function searchPaytm(route, response, mongoDocs) {
  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext();
  const page = await context.newPage();

  try {
    await page.goto("https://tickets.paytm.com/");
    await page.waitForTimeout(2000);

    await page.click("#Bus");
    console.log("Clicked on Buses");
    await page.waitForTimeout(2000);

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
    const source = "paytmBus";
    for (let i = 0; i < buses.length; i++) {
      console.log("-------------------------------------");
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

      const subArrivalTime = normalizeTime(departure);
      const match = findMatchingSchedule(
        subArrivalTime,
        mongoDocs,
        route["paytmBusSource"],
        route["paytmBusDestination"]
      );

      if (!match) {
        console.log(
          `--No matching schedule found for departure time: ${subArrivalTime}`
        );
        let subrouteKey = `${route["paytmBusSource"]} - ${route["paytmBusDestination"]}`;
        if (!response["Not Found"]) response["Not Found"] = {};
        if (!response["Not Found"]["Not Found"])
          response["Not Found"]["Not Found"] = {};
        if (!response["Not Found"]["Not Found"][subrouteKey])
          response["Not Found"]["Not Found"][subrouteKey] = {};
        if (!response["Not Found"]["Not Found"][subrouteKey][subArrivalTime]) {
          response["Not Found"]["Not Found"][subrouteKey][subArrivalTime] = {};
        }

        response["Not Found"]["Not Found"][subrouteKey][subArrivalTime][
          source
        ] = rating;
        continue;
      }

      let rawMainRouteName = match["ScheduleCode"];
      let mainRouteName = extractMainRouteName(rawMainRouteName);
      let mainDepartureTime = formatTimeFromSchedule(rawMainRouteName);
      let subrouteKey = `${route["paytmBusSource"]} - ${route["paytmBusDestination"]}`;

      if (!response[mainRouteName]) response[mainRouteName] = {};
      if (!response[mainRouteName][mainDepartureTime])
        response[mainRouteName][mainDepartureTime] = {};
      if (!response[mainRouteName][mainDepartureTime][subrouteKey])
        response[mainRouteName][mainDepartureTime][subrouteKey] = {};
      if (
        !response[mainRouteName][mainDepartureTime][subrouteKey][subArrivalTime]
      ) {
        response[mainRouteName][mainDepartureTime][subrouteKey][
          subArrivalTime
        ] = {};
      }

      response[mainRouteName][mainDepartureTime][subrouteKey][subArrivalTime][
        source
      ] = rating;

      // const subrouteKey = `${route["From City"]} - ${route["To City"]}`;

      //   if (!response[mainRouteName]) response[mainRouteName] = {};
      //   if (!response[mainRouteName][subrouteKey])
      //     response[mainRouteName][subrouteKey] = {};
      //   if (!response[mainRouteName][subrouteKey][subArrivalTime])
      //     response[mainRouteName][subrouteKey][subArrivalTime] = {};

      //   response[mainRouteName][subrouteKey][subArrivalTime]["paytmBus"] = rating;
      // }
    }
  } catch (err) {
    console.error("Error:", err);
  } finally {
    // injectTopLevelRatings(response);
    await browser.close();
  }
}

async function searchAbhiBus(route, response, mongoDocs) {
  const browser = await chromium.launch({ headless: false });
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

    await page.getByRole("button", { name: "Tomorrow" }).click();

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

    const source = "abhibus";
    for (const bus of buses) {
      const getText = async (selector) => {
        try {
          const el = await bus.$(selector);
          return el ? await el.textContent() : "NA";
        } catch {
          return "NA";
        }
      };

      const departure = await getText(
        "#travel-distance-source-info div div span"
      );
      const arrival = await getText(
        "#travel-distance-destination-info div div span"
      );
      const rating = await getText("*[id*='rating-card-container'] > div span");

      console.log("-------------------------------------");
      console.log(`Departure: ${normalizeTime(departure)}`);
      console.log(`Arrival: ${normalizeTime(arrival)}`);
      console.log(`Rating: ${rating}`);

      let subArrivalTime = normalizeTime(departure);

      const match = findMatchingSchedule(
        subArrivalTime,
        mongoDocs,
        route["abhiBusSource"],
        route["abhiBusDestination"]
      );

      if (!match) {
        console.log(
          ` No matching schedule found for arrival time: ${subArrivalTime}`
        );
        let subrouteKey = `${route["paytmBusSource"]} - ${route["paytmBusDestination"]}`;
        if (!response["Not Found"]) response["Not Found"] = {};
        if (!response["Not Found"]["Not Found"])
          response["Not Found"]["Not Found"] = {};
        if (!response["Not Found"]["Not Found"][subrouteKey])
          response["Not Found"]["Not Found"][subrouteKey] = {};
        if (!response["Not Found"]["Not Found"][subrouteKey][subArrivalTime]) {
          response["Not Found"]["Not Found"][subrouteKey][subArrivalTime] = {};
        }
        response["Not Found"]["Not Found"][subrouteKey][subArrivalTime][
          source
        ] = rating;
        continue;
      }

      let rawMainRouteName = match["ScheduleCode"];
      let mainRouteName = extractMainRouteName(rawMainRouteName);
      let mainDepartureTime = formatTimeFromSchedule(rawMainRouteName);
      let subrouteKey = `${route["abhiBusSource"]} - ${route["abhiBusDestination"]}`;

      if (!response[mainRouteName]) response[mainRouteName] = {};
      if (!response[mainRouteName][mainDepartureTime])
        response[mainRouteName][mainDepartureTime] = {};
      if (!response[mainRouteName][mainDepartureTime][subrouteKey])
        response[mainRouteName][mainDepartureTime][subrouteKey] = {};
      if (
        !response[mainRouteName][mainDepartureTime][subrouteKey][subArrivalTime]
      ) {
        response[mainRouteName][mainDepartureTime][subrouteKey][
          subArrivalTime
        ] = {};
      }

      response[mainRouteName][mainDepartureTime][subrouteKey][subArrivalTime][
        source
      ] = rating;
    }
  } catch (err) {
    console.error("Error:", err);
  } finally {
    // injectTopLevelRatings(response);
    await browser.close();
  }
}

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
      let targetDiv = null;

      for (const div of allDivs) {
        const className = await div.getAttribute("class");
        if (className.includes("ServiceWise---backGround---2yaYw")) {
          targetDiv = div;
          break;
        }
      }

      // Fallback to the first if no background match
      if (!targetDiv && allDivs.length > 0) {
        targetDiv = allDivs[0];
      }
      const textContent = await targetDiv.textContent();
      let viaArrivalTime = await targetDiv
        .$eval("span:has-text(':')", (el) => el.textContent.trim())
        .catch(() => "N/A");
      viaArrivalTime = normalizeTime(viaArrivalTime);

      const fullRouteName = await targetDiv
        .$eval("span:has-text('-')", (el) => el.getAttribute("title"))
        .catch(() => "N/A");

      let fromCity = fullRouteName?.split("-")[1]?.trim() ?? fullRouteName;
      let toCity = fullRouteName?.split("-")[2]?.trim() ?? fullRouteName;
      fromCity = fromCity.split(" ")[0];
      toCity = toCity.split(" ")[0];

      //matching the original bus main route name
      let match = null;
      match = await findMatchingSchedule(
        viaArrivalTime,
        mongoDocs,
        fromCity,
        toCity
      );
      console.log(
        "Selected Div Text: ",
        `fromCity: ${fromCity}, toCity: ${toCity}, viaArrivalTime: ${viaArrivalTime}`
      );
      const viaBtn = await card.$("span.ServiceWise---viaCnt---28sTm");
      if (viaBtn) {
        await viaBtn.click();
        await page.waitForTimeout(500);

        const viaRoutes = await card.$$("div.ServiceWise---body---1OnfX");
        console.log(`Via Routes: ${viaRoutes.length}`);

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
            const subrouteKey = `${fromCity} - ${toCity}`;

            if (!response["Not Found"]) response["Not Found"] = {};
            if (!response["Not Found"]["Not Found"])
              response["Not Found"]["Not Found"] = {};
            if (!response["Not Found"]["Not Found"][subrouteKey])
              response["Not Found"]["Not Found"][subrouteKey] = {};
            if (
              !response["Not Found"]["Not Found"][subrouteKey][subArrivalTime]
            ) {
              response["Not Found"]["Not Found"][subrouteKey][subArrivalTime] =
                {};
            }
            response["Not Found"]["Not Found"][subrouteKey][subArrivalTime][
              "redbus"
            ] = viaRating;

            response["Not Found"]["Not Found"][subrouteKey][subArrivalTime][
              "srpRating"
            ] = srpRanking;
            continue;
          }

          const rawMainRouteName = match["ScheduleCode"];
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
          ]["srpRating"] = srpRanking;
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

//   for (let j = 0; j < viaRoutes.length; j++) {
//     const via = viaRoutes[j];
//     try {
//       const viaArrivalTime = await via
//         .$eval("span[style*='text-align: left']", (el) =>
//           el.textContent.trim()
//         )
//         .catch(() => "N/A");

//       const fullRouteName = await via
//         .$eval("span[title*='-']", (el) => el.getAttribute("title"))
//         .catch(() => "N/A");

//       const cleaned =
//         fullRouteName?.replace(/^\d+\s*-\s*/, "") || fullRouteName;

//       const [fromCity, toCity] =
//         cleaned?.split(" - ").map((s) => s.trim()) || [];

//       const cleanRouteName =
//         fromCity && toCity
//           ? `${fromCity.trim()} - ${toCity.trim()}`
//           : cleaned;

//       const viaRating = await via
//         .$eval("span[class*='Sub_Rated_space']", (el) =>
//           el.textContent.trim()
//         )
//         .catch(() => "N/A");

//       const trendBtn = await via.$("span:has-text('View trend')");
//       let viaSrpRating = "N/A / out of N/A";

//       if (trendBtn) {
//         try {
//           await trendBtn.scrollIntoViewIfNeeded();
//           await page.waitForTimeout(300);
//           await trendBtn.click();

//           await page.waitForSelector(
//             "div[class*='RNRCalendar---rankTextDiv']",
//             {
//               timeout: 8000,
//             }
//           );

//           const rankText = await page
//             .$eval("div[class*='rankTextDiv']", (el) =>
//               el.textContent.trim()
//             )
//             .catch(() => null);

//           const outOfText = await page
//             .$eval("div[class*='totalTextDiv']", (el) =>
//               el.textContent.trim()
//             )
//             .catch(() => null);

//           console.log(" SRP Rank Text:", rankText);
//           console.log(" SRP OutOf Text:", outOfText);

//           const rankMatch = rankText?.match(/Rank\s*(\d+)/i);
//           const outOfMatch = outOfText?.match(/out of\s*(\d+)/i);

//           const rank = rankMatch ? rankMatch[1] : "N/A";
//           const outOf = outOfMatch ? outOfMatch[1] : "N/A";

//           if (rank !== "N/A" && outOf !== "N/A") {
//             viaSrpRating = `${rank} / out of ${outOf}`;
//           } else if (rank !== "N/A") {
//             viaSrpRating = rank;
//           } else {
//             viaSrpRating = "N/A";
//           }

//           const closeBtn = await page.$(
//             "xpath=//div[contains(@class,'RNRCalendar---headerDiv')]/div[last()]"
//           );
//           if (closeBtn) {
//             await closeBtn.click();
//             await page.waitForTimeout(500);
//           }
//         } catch (e) {
//           console.log(
//             `⚠️ Error extracting full SRP for Via Route [${j + 1}]:`,
//             e.message
//           );
//         }
//       } else {
//         console.log(
//           `❌ No SRP "View Trend" button inside Via Route [${j + 1}]`
//         );
//       }

//       const normalizedViaTime = normalizeTime(viaArrivalTime);

//       const busSlot = response[mainRouteName][mainBusTime];

//       if (
//         cleanRouteName.toLowerCase() !== "n/a" &&
//         cleanRouteName !== undefined &&
//         normalizedViaTime !== "N/A"
//       ) {
//         if (!response[mainRouteName][cleanRouteName]) {
//           response[mainRouteName][cleanRouteName] = {};
//         }
//       }

//       const alreadyExists =
//         response[mainRouteName][cleanRouteName][normalizedViaTime];

//       if (!alreadyExists || alreadyExists.redbus === "N/A") {
//         response[mainRouteName][cleanRouteName][normalizedViaTime] = {
//           redbus: viaRating,
//           srpRating: viaSrpRating,
//         };
//       }
//     } catch (e) {
//       console.log(` Via Route ${j + 1} error: ${e.message}`);
//     }
//   }

//   await viaRoutesBtn.click();
//   await page.waitForTimeout(500);
// } else {
//   console.log(` No via routes for Service ${i + 1}`);
// }
//}

//   const browser = await chromium.launch({ headless: false });

//   const context = await browser.newContext({});

//   const page = await context.newPage();

//   await page.addInitScript(() => {
//     Object.defineProperty(navigator, "webdriver", {
//       get: () => false,
//     });

//     Object.defineProperty(navigator, "plugins", {
//       get: () => [1, 2, 3, 4, 5],
//     });

//     Object.defineProperty(navigator, "languages", {
//       get: () => ["en-US", "en"],
//     });

//     const getParameter = WebGLRenderingContext.prototype.getParameter;
//     WebGLRenderingContext.prototype.getParameter = function (param) {
//       if (param === 37445) return "Intel Inc.";
//       if (param === 37446) return "Intel Iris OpenGL Engine";
//       return getParameter.call(this, param);
//     };
//   });
//   await page.waitForTimeout(1500);

//   try {
//     // Step 1: Login to redbus.pro
//     await page.goto("https://www.redbus.pro/");
//     await page.setViewportSize({ width: 1280, height: 800 });

//     await page.fill("#username", "9748");
//     await page.fill("#password", "prasannapurple");
//     await page.waitForTimeout(1000);
//     await page.click("#loginSubmit");
//     await page.waitForTimeout(5000);

//     // Step 2: Handle SVG Close Icon if present
//     const closeIcon = page.locator(".QuickFundBanner---cross---2Mp_5");

//     if (await closeIcon.isVisible()) {
//       await closeIcon.click();
//     }

//     // Step 3: Open Side Menu and click "R & R"
//     await page.click(".Header---ham_menu---gOm2d");
//     await page.waitForTimeout(2000);

//     const scrollableDiv = await page.locator(
//       "xpath=//body/div[@id='root']/div/div/div/div[3]"
//     );
//     await page.evaluate(
//       (el) => (el.scrollTop = el.scrollHeight),
//       await scrollableDiv.elementHandle()
//     );
//     await page.waitForTimeout(2000);

//     await page.click("xpath=//span[normalize-space()='R & R']");
//     await page.waitForTimeout(5000);

//     // Hide menu with offset click
//     await page.mouse.click(500, 200);
//     await page.waitForTimeout(3000);

//     // Step 4: Skip Intro Coach Mark
//     const skipBtn = page.locator(
//       "xpath=//button[contains(@class,'CoachMarks---btn1') and text()='Skip']"
//     );
//     if ((await skipBtn.count()) > 0 && (await skipBtn.first().isVisible())) {
//       await skipBtn.first().click();
//       console.log("Skip button clicked.");
//     }

//     // Step 5: Input Source/Destination and Apply Filter
//     await page.fill("xpath=//input[@placeholder='Source']", route.redBusSource);
//     await page.waitForTimeout(3000);
//     await page.click(`xpath=//div[contains(text(),'${route.redBusSource}')]`);
//     await page.waitForTimeout(2000);
//     await page.fill(
//       "xpath=//input[@placeholder='Destination']",
//       route.redBusDestination
//     );
//     await page.waitForTimeout(2000);
//     await page.click(
//       `xpath=//div[contains(text(),'${route.redBusDestination}')]`
//     );
//     await page.waitForTimeout(2000);
//     await page.click("xpath=//button[normalize-space()='Filter']");
//     await page.waitForTimeout(3000);

//     // Step 6: Extract Data
//     await page.waitForSelector("xpath=//span[contains(text(),'View trend')]");

//     try {
//       const targetSelector = ".ServiceWise---noScroll---2s4RK";
//       await scrollUntilVisible(page, targetSelector);
//     } catch (e) {
//       console.error("Error scrolling to target:", e.message);
//     }
//     const serviceCards = await page.$$(
//       "xpath=//div[contains(@class,'CardV2---card')]"
//     );
//     console.log(`Total services found: ${serviceCards.length}`);

//     const count = serviceCards.length;
//     for (let i = 0; i < count; i++) {
//       const card = serviceCards[i]; // <-- Use array indexing

//       try {
//         const getText = async (card, selector) => {
//           // Use page.locator with card's element handle as the parent
//           const element = await card.$(selector);
//           return element
//             ? (
//                 await (await element.getProperty("textContent")).jsonValue()
//               ).trim()
//             : "NA";
//         };

//         const arrivalTime = await getText(
//           card,
//           "span[style*='text-align: left']"
//         );
//         const rating = await getText(card, "span[class*='Sub_Rated_space']");

//         console.log(`\nService ${i + 1} Arrival Time: ${arrivalTime}`);
//         console.log(`Service ${i + 1} Rating: ${rating}`);
//         if (!response[normalizeTime(arrivalTime)]) {
//           response[normalizeTime(arrivalTime)] = {};
//         }
//         response[normalizeTime(arrivalTime)]["redBus"] = rating;

//         // Click calendar icon
//         const calendarIcons = await page.$$(
//           "xpath=//img[contains(@alt,'calendar')]"
//         );
//         if (calendarIcons[i]) {
//           await calendarIcons[i].click();

//           // Wait for rank popup
//           await page.waitForSelector(
//             "xpath=//div[contains(@class,'RNRCalendar---rankTextDiv')]",
//             { timeout: 5000 }
//           );

//           let todayRank = "NA";
//           let outOf = "NA";

//           const todayRankElem = await page.$(
//             "xpath=(//div[contains(@class,'rankTextDiv')])[1]"
//           );
//           if (todayRankElem) {
//             todayRank = (await todayRankElem.textContent())?.trim() || "NA";
//           }

//           const outOfElem = await page.$(
//             "xpath=(//div[contains(@class,'totalTextDiv')])[1]"
//           );
//           if (outOfElem) {
//             outOf = (await outOfElem.textContent())?.trim() || "NA";
//           }

//           console.log(`Service ${i + 1} Today's Rank: ${todayRank} ${outOf}`);
//           response[normalizeTime(arrivalTime)]["srpRanking"] =
//             todayRank + " " + outOf;

//           // Close popup
//           const closeButton = await page.locator(
//             "xpath=//div[contains(@class,'RNRCalendar---headerDiv')]/div[last()]"
//           );
//           await closeButton.click();
//           await page.waitForTimeout(1500);
//         }
//       } catch (err) {
//         console.log(`Error in Service ${i + 1}: ${err.message}`);
//       }
//     }
//   } catch (e) {
//     console.error("❌ Test failed:", e.message);
//   } finally {
//     await browser.close();
//   }
// }

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
