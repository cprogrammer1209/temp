const mongoURI =
  "mongodb://staging:stage789@server.gibots.com:2400/?authSource=aiqod-staging"; // Change this if needed

const xlsx = require("xlsx");
const { MongoClient, ObjectId } = require("mongodb"); // Import ObjectId
const readline = require("readline");

// MongoDB Connection URI
const dbName = "aiqod-staging";
const collectionName = "_prasannaPurpleBuses";

// Path to the Excel file
const filePath =
  "/home/yuvaraj/Downloads/Bus Schedule Details (173) (1)(1).xlsx";

async function previewAndInsert() {
  try {
    // Read the Excel file
    const workbook = xlsx.readFile(filePath);
    const sheetName = workbook.SheetNames[0];
    const sheet = workbook.Sheets[sheetName];

    // Convert Excel to JSON
    let jsonData = xlsx.utils.sheet_to_json(sheet, { defval: "" });

    const currentTimestamp = new Date();

    // ✅ Add extra fields with ObjectId to each document
    jsonData = jsonData.map((doc) => ({
      ...doc,
      subscriberId: ObjectId("67c80f3d1fa7aaf2a359cee0"), // Add ObjectId field 1
      orgId: ObjectId("67c80f3d1fa7aaf2a359cede"), // Add ObjectId field 2
      createdAt: currentTimestamp, // Add createdAt timestamp
      updatedAt: currentTimestamp, // Add updatedAt timestamp
    }));
     jsonData = jsonData.map((row) => {
      if (typeof row.Time === "number") {
        row.Time = excelTimeToAmPm(row.Time);
      }
      return row;
    });

    // Show a sneak peek (first 5 rows)
    console.log(
      "Preview of first 5 rows:",
      JSON.stringify(jsonData.slice(0, 5), null, 2)
    );

    // Ask user if they want to proceed
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

        // Connect to MongoDB
        const client = new MongoClient(mongoURI);
        await client.connect();
        console.log("Connected to MongoDB");

        // Insert data into collection
        const db = client.db(dbName);
        const collection = db.collection(collectionName);
        const result = await collection.insertMany(jsonData);

        console.log(`Inserted ${result.insertedCount} records into MongoDB`);

        // Close connection
        await client.close();
      }
    );
  } catch (error) {
    console.error("Error:", error);
  }
}

// Run the function
previewAndInsert();
function excelTimeToAmPm(serial) {
  const totalMinutes = Math.round(24 * 60 * serial);
  let hours = Math.floor(totalMinutes / 60);
  const minutes = totalMinutes % 60;

  const ampm = hours >= 12 ? "PM" : "AM";
  hours = hours % 12;
  if (hours === 0) hours = 12;

  return `${hours}:${minutes.toString().padStart(2, "0")} ${ampm}`;
}
