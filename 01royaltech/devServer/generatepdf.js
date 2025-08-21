const express = require("express");
const bodyParser = require("body-parser");
const cors = require("cors");

const multer = require("multer");
const axios = require("axios");
const FormData = require("form-data");
const https = require("https");


const agent = new https.Agent({ rejectUnauthorized: false });

const app = express();
const PORT = 6969;
const storage = multer.memoryStorage();
const upload = multer({ storage });const { MongoClient, ObjectId } = require("mongodb");
let db 
async () => {
  const uriSrc = "mongodb://dev-SU:mdhdiIQTS@172.168.1.199:27017/?authSource=aiqod-dev"; //db url
    const client1 = new MongoClient(uriSrc);
    await client1.connect();
     db = await client1.db("aiqod-dev");
}

const wait = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

// Middleware
app.use(bodyParser.json({ limit: "10mb" })); // Allows sending large HTML content
app.use(cors()); // Enable CORS for external requests

const API_1 = "https://dev.aiqod.com:843/gibots-api/bots/triggerProcess"; // replace with real URL
const API_2 = "https://dev.aiqod.com:843/gibots-api/bots/extractionStatus"; // replace with real URL
const API_3 = "https://dev.aiqod.com:843/gibots-api/bots/getJSON";

app.post("/aiqod-api/process-file", upload.any(), async (req, res) => {
  console.log("Inside the API ",req.body);
  try {
    if (!req.files || req.files.length === 0) {
      return res.status(400).json({ error: "No files uploaded" });
    }
    if(!req.body || !req.body.PdfClientName || req.body.PdfClientName =="" ) {
      return res.status(400).json({ error: "PdfClientName is not in request body" });
    }
     if(!req.body || !req.body.JobType || req.body.JobType =="") {
      return res.status(400).json({ error: "JobType is not in request body"  });
    }
    let body = req.body
    const uriSrc = "mongodb://dev-SU:mdhdiIQTS@172.168.1.199:27017/?authSource=aiqod-dev"; //db url
    const client1 = new MongoClient(uriSrc);
    await client1.connect();
    const db = await client1.db("aiqod-dev");
    let response = await db.collection("Genai_Prompt_Templates").findOne({template_name:{ $regex: `^${body.PdfClientName}$`, $options: 'i' },type:{ $regex: `^${body.JobType}$`, $options: 'i' }});
    console.log("response ",response)
    if(!response || response==undefined || response==null){
      return res.status(400).json({error : "No templates found"})
    }
    req.body.PdfClientName = response.template_name
    req.body.JobType = response.type
    console.log("req.body ",req.body)
    console.log("length ", response.type);
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
	console.log('response ',uploadRes.data)
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
      if (count > 25) {
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
    res.json(finalRes.data.json);
  } catch (err) {
    console.error("Error:", err.message);
    res.status(500).json({ error: "Processing failed" });
  }
});

// Start the Server
const tempServer = app.listen(PORT, () => {
  console.log(`🚀 Server running on http://localhost:${PORT}`);
});


tempServer.setTimeout(1800000);