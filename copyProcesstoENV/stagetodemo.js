const { MongoClient } = require("mongodb");
const mongoose = require("mongoose");
const ObjectId = mongoose.Types.ObjectId;
const fs = require("fs");
const path = require("path");
const request = require("request");
const { pipeline } = require("stream");
const json2csv = require("json2csv").parse;

let db1, db2;

async function main() {
  // const uriSrc = "mongodb://debug-nodelete:ThsnYU@172.168.1.232:27017/?authSource=debug-db";
  // mongodb://domo-1:domonodel@172.168.1.199:27017/?authSource=demo
  const uriSrc =
    // "mongodb://domo-1:domonodel@172.168.1.199:27017/?authSource=demo";
    "mongodb://staging-SU:insjWTERY@server.gibots.com:2400/?authSource=aiqod-staging";  //prod

  //destination db
  // const uriDest = "mongodb://dev-SU:mdhdiIQTS@172.168.1.199:27017/?authSource=aiqod-dev";
  // const uriDest = "mongodb://dev-SU:mdhdiIQTS@172.168.1.199:27017/?authSource=aiqod-dev";
  // const uriDest = "mongodb://staging-SU:insjWTERY@server.gibots.com:2400/?authSource=aiqod-staging";
  const uriDest =
  "mongodb://domo-1:domonodel@172.168.1.199:27017/?authSource=demo"
    // "mongodb://pprod:prOd121233@172.168.0.146:27017/?authSource=prod-DB";
    // "mongodb://staging-SU:insjWTERY@server.gibots.com:2400/?authSource=aiqod-staging";

  //uriSrc
  //uriDest

  const client1 = new MongoClient(uriSrc);
  const client2 = new MongoClient(uriDest);

  try {
    // Connect to the MongoDB cluster
    await client1.connect();

    db1 = await client1.db("aiqod-staging");

    await client2.connect();

    // db2 = await client2.db("prod-DB");
    // db2 = await client2.db("prod-DB");
    db2 = await client2.db("demo");

    await copyDB();
  } catch (e) {
    console.error(e);
  } finally {
    await client1.close();
    await client2.close();
  }
}

main().catch(console.error);

let routesMapping = {
  "http://localhost:8990/adhigam-api": "http://localhost:7891/adhigam-api",
  "http://localhost:1008/gibots-ocr": "http://localhost:1008/gibots-ocr",
  "http://localhost:4056/gibots-pyimg": "http://localhost:4056/gibots-pyimg",
};

//staging path for data ingestion bot : {'requestURL':'http://172.168.1.19:7895/gibots-orch/orchestrator/botsiowrite','acknowledgeURL':'http://172.168.1.19:7895/gibots-orch/orchestrator/acknowledge', 'mountpath':'/home/ubuntu/new_ssd/publicfolder/liberty-fs/handbook/'}

let addInfos = ["handbookData","My Knowledge Hub","Handbook Approval Form", "My Knowledge Hub File","Handbook Documents Approval Form",];

let processes = [];

let reports = []

let collections = [];

let metadata = [];

let warningcode = [];

let package = [];

var viewNamesToCopy = []
let scanningfields = [];

// let link = 'https://staging.aiqod.com:843'

async function copyDB() {
  let ruleIds = [];

  //--------------copying addinfo templates-----------------
  let srcAddInfo = await db1
    .collection("additionalinfos")
    .find({
      templateName: { $in: addInfos },
    })
    .toArray();

  console.log("Templates-----", srcAddInfo.length);

  for (let add of srcAddInfo) {
    if (add["ruleId"]) {
      ruleIds.push(add["ruleId"]);
    }
    let _id = add["_id"];
    delete add["_id"];

    await db2.collection("additionalinfos").updateOne(
      {
        _id: ObjectId(_id),
      },
      {
        $set: add,
      },
      {
        upsert: true,
      }
    );
  }
  //----------------------------------------------------------

  //--------------copying Processes Projects -----------------
  let srcProcesses = await db1
    .collection("processes")
    .find({
      processName: { $in: processes },
      isDeleted: false,
    })
    .toArray();

  let srcProjects = await db1
    .collection("projects")
    .find({
      name: { $in: processes },
      isDeleted: false,
    })
    .toArray();

  console.log("Processes-----", srcProcesses.length);

  //if collab pro then this code is required
  //   for(let proc of (srcProcesses)){
  //     let mastervarlist = proc['masterVariableList']
  //     let stringifiedmvl = JSON.stringify(mastervarlist)
  //     let regex = /https:\/\/dev\.aiqod\.com:843/g;
  //     let newText = stringifiedmvl.replace(regex, link);
  //     let newMasterVarList = JSON.parse(newText)
  //     proc['masterVariableList'] = newMasterVarList
  //   }

  for (let proc of srcProcesses) {
    let _idPs = proc["_id"];
    delete proc["_id"];

    let pjD = srcProjects.find((a) => String(a._id) == String(proc.projectId));

    for (let bot of proc["processTaskList"]) {
      if (bot["remoteUrl"]) {
        for (let key in routesMapping) {
          bot["remoteUrl"] = bot["remoteUrl"].replace(key, routesMapping[key]);
        }
      }
      if (bot["selectedRulesList"] && bot["selectedRulesList"].length) {
        ruleIds = ruleIds.concat(bot["selectedRulesList"]);
      }
    }

    await db2.collection("processes").updateOne(
      {
        _id: ObjectId(_idPs),
      },
      {
        $set: proc,
      },
      {
        upsert: true,
      }
    );

    if (pjD) {
      let _idPj = pjD["_id"];
      delete pjD["_id"];

      for (let bot of pjD["projectTaskList"]) {
        if (bot["remoteUrl"]) {
          for (let key in routesMapping) {
            bot["remoteUrl"] = bot["remoteUrl"].replace(
              key,
              routesMapping[key]
            );
          }
        }
      }

      await db2.collection("projects").updateOne(
        {
          _id: ObjectId(_idPj),
        },
        {
          $set: pjD,
        },
        {
          upsert: true,
        }
      );
    }
  }
  //----------------------------------------------------------

  console.log("Rules--", ruleIds);

  //--------------copying rules-----------------
  let srcRule = await db1
    .collection("rules")
    .find({
      _id: { $in: ruleIds.map((a) => ObjectId(a)) },
    })
    .toArray();

  console.log("Rules-----", srcAddInfo.length);

  for (let add of srcRule) {
    let _id = add["_id"];
    delete add["_id"];

    await db2.collection("rules").updateOne(
      {
        _id: ObjectId(_id),
      },
      {
        $set: add,
      },
      {
        upsert: true,
      }
    );
  }

  //----------------------------------------------------------

  //--------------copying Reports Projects -----------------

  let srcReportsDRQ = await db1
    .collection("dynamicreportsqueries")
    .find({
      name: { $in: reports },
    })
    .toArray();

  let srcReportsQD = await db1
    .collection("querydescriptors")
    .find({
      name: { $in: reports },
    })
    .toArray();

  for (let add of srcReportsDRQ) {
    let _id = add["_id"];
    delete add["_id"];

    await db2.collection("dynamicreportsqueries").updateOne(
      {
        _id: ObjectId(_id),
      },
      {
        $set: add,
      },
      {
        upsert: true,
      }
    );
  }

  for (let add of srcReportsQD) {
    let _id = add["_id"];
    delete add["_id"];

    await db2.collection("querydescriptors").updateOne(
      {
        _id: ObjectId(_id),
      },
      {
        $set: add,
      },
      {
        upsert: true,
      }
    );
  }

  //----------------------------------------------------------

  //--------------copying Collections -----------------

  for (let collection of collections) {
    let toCopy = await db1.collection(collection).find({}).toArray();

    for (let add of toCopy) {
      let _id = add["_id"];
      delete add["_id"];

      await db2.collection(collection).updateOne(
        {
          _id: ObjectId(_id),
        },
        {
          $set: add,
        },
        {
          upsert: true,
        }
      );
    }
  }

  //----------------------------------------------------------

  //--------------copying Metadata -----------------

  let metadatatocopy = await db1
    .collection("tablemetadatas")
    .find({
      tableName: { $in: metadata },
    })
    .toArray();

  console.log(metadata.length);

  for (let add of metadatatocopy) {
    let _id = add["_id"];
    delete add["_id"];

    await db2.collection("tablemetadatas").updateOne(
      {
        _id: ObjectId(_id),
      },
      {
        $set: add,
      },
      {
        upsert: true,
      }
    );
  }

  // -------------copying scanningfields--------

  let scanningfieldstocopy = await db1
    .collection("scanningfields")
    .find({
      documentType: { $in: scanningfields },
    })
    .toArray();

  for (let add of scanningfieldstocopy) {
    let _id = add["_id"];
    delete add["_id"];

    await db2.collection("scanningfields").updateOne(
      {
        _id: ObjectId(_id),
      },
      {
        $set: add,
      },
      {
        upsert: true,
      }
    );
  }

  //----------------------------------------------------------

  //--------------copying Custom Views -----------------

  for (let viewNameToCopy of viewNamesToCopy) {
    // Retrieve the view information from the source database
    var viewInfo = await db1
      .listCollections({ name: viewNameToCopy })
      .toArray();

    for (let i = 0; i < viewInfo.length; i++) {
      let PipelineArray = viewInfo[i].options.pipeline;
      let viewName = viewInfo[i].name;
      let sourceCollection = viewInfo[i].options.viewOn;
      const options = { viewOn: sourceCollection, pipeline: PipelineArray };

      const collections = await db2
        .listCollections({}, { nameOnly: true })
        .toArray();
      const collectionNames = collections.map((c) => c.name);

      collectionName = viewName;

      if (collectionNames.includes(collectionName)) {
        await db2.collection(collectionName).drop();
      }

      // Create the view
      await db2.createCollection(viewName, options);
    }
  }

  //----------------------------------------------------------

  //--------------copying errorcodes -----------------

  let errorcodesToCopy = await db1
    .collection("errwarnmasters")
    .find({
      code: { $in: warningcode },
    })
    .toArray();

  for (let add of errorcodesToCopy) {
    let _id = add["_id"];
    delete add["_id"];

    await db2.collection("errwarnmasters").updateOne(
      {
        _id: ObjectId(_id),
      },
      {
        $set: add,
      },
      {
        upsert: true,
      }
    );
  }

  //----------------------------------------------------------

  //--------------copying Packages -----------------

  let packagesTocopy = await db1
    .collection("products")
    .find({
      productName: { $in: package },
    })
    .toArray();

  for (let add of packagesTocopy) {
    let _id = add["_id"];
    delete add["_id"];

    await db2.collection("products").updateOne(
      {
        _id: ObjectId(_id),
      },
      {
        $set: add,
      },
      {
        upsert: true,
      }
    );
  }
}
