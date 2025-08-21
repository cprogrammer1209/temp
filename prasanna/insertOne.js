import xlsx from "xlsx";
import { MongoClient } from "mongodb";
import readline from "readline";
import { DateTime } from "luxon";

const mongoURI =
  "mongodb://pprod:prOd121233@192.168.28.131:27017/prod-DB";
const dbName = "prod-DB";
const collectionName = "_prasannaPurpleBuses";
const filePath =
  "/home/yuvaraj/Downloads/Telegram Desktop/Ujjain_pune.xlsx";

async function previewAndInsert() {
  try {
    const workbook = xlsx.readFile(filePath);
    const sheetName = workbook.SheetNames[0];
    const sheet = workbook.Sheets[sheetName];
    let jsonData = xlsx.utils.sheet_to_json(sheet, { defval: "" });

    const currentTimestamp = new Date();

    jsonData = jsonData.map((doc) => {
      // Remove all __EMPTY columns
      const cleanedDoc = Object.fromEntries(
        Object.entries(doc).filter(([key, _]) => !key.startsWith("__EMPTY"))
      );

      let formattedTime = null;
      let formattedRouteTime = null;
      let formattedDate = null;

      // Convert Time (Excel decimal to "hh:mm a")
      if (!isNaN(cleanedDoc.Time) && typeof cleanedDoc.Time === "number") {
        const totalMinutes = cleanedDoc.Time * 24 * 60;
        const hours = Math.floor(totalMinutes / 60);
        const minutes = Math.round(totalMinutes % 60);
        formattedTime = DateTime.fromObject({
          hour: hours,
          minute: minutes,
        }).toFormat("hh:mm a");
      }

      // Convert RouteTime (Excel decimal to "hh:mm a")
      if (
        !isNaN(cleanedDoc.RouteTime) &&
        typeof cleanedDoc.RouteTime === "number"
      ) {
        const totalMinutes = cleanedDoc.RouteTime * 24 * 60;
        const hours = Math.floor(totalMinutes / 60);
        const minutes = Math.round(totalMinutes % 60);
        formattedRouteTime = DateTime.fromObject({
          hour: hours,
          minute: minutes,
        }).toFormat("hh:mm a");
      }

      // Convert Excel Date to JS Date
      if (
        !isNaN(cleanedDoc["Schedule Date"]) &&
        typeof cleanedDoc["Schedule Date"] === "number"
      ) {
        formattedDate = DateTime.fromObject({ year: 1900, month: 1, day: 1 })
          .plus({ days: cleanedDoc["Schedule Date"] - 2 })
          .toJSDate();
      }

      return {
        ...cleanedDoc,
        Time: formattedTime ?? null,
        "Schedule Date": formattedDate,
        RouteTimeFormatted: formattedRouteTime ?? null,
        phone_num: String(cleanedDoc.phone_num ?? ""),
        subscriberId: "5beaabd82ac6767c86dc311c",
        orgId: "5c495dbfffa2a85b2c19a77f",
        createdAt: currentTimestamp,
        updatedAt: currentTimestamp,
      };
    });

    console.log(
      "Preview of first 5 rows:",
      JSON.stringify(jsonData.slice(0, 5), null, 2)
    );

    const rl = readline.createInterface({
      input: process.stdin,
      output: process.stdout,
    });
    rl.question(
      "Do you want to insert all data into MongoDB? (yes/no): ",
      async (answer) => {
        rl.close();
        if (answer.toLowerCase() !== "yes") {
          console.log("Operation cancelled.");
          return;
        }

        const client = new MongoClient(mongoURI);
        await client.connect();
        console.log("Connected to MongoDB");

        const db = client.db(dbName);
        const collection = db.collection(collectionName);
        const result = await collection.insertMany(jsonData, {
          ordered: false,
        });

        console.log(`Inserted ${result.insertedCount} records into MongoDB`);
        await client.close();
      }
    );
  } catch (error) {
    console.error("Error:", error);
  }
}

previewAndInsert();
