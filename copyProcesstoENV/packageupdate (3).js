const { MongoClient } = require("mongodb");
const mongoose = require("mongoose");
const ObjectId = mongoose.Types.ObjectId;
let db1
async function main() {
  const uriSrc = "mongodb://dev-SU:mdhdiIQTS@server.gibots.com:2400/aiqod-dev";  //dev
  // const uriSrc = "mongodb://staging-SU:insjWTERY@server.gibots.com:2400/?authSource=aiqod-staging"; //stage
  // const uriSrc = "mongodb://pprod:prOd121233@103.58.164.118:27017/prod-DB";  //prod
  const client1 = new MongoClient(uriSrc);

  try {
    // Connect to the MongoDB cluster
    await client1.connect();
    db1 = await client1.db("aiqod-dev");  //dev
    // db1 = await client1.db("aiqod-staging"); //stage
    // db1 = await client1.db("prod-DB"); //prod
    await copyDB();
  } catch (e) {
    console.error(e);
  } finally {
    await client1.close();
  }
}

main().catch(console.error);


//can add subscribers_number and for all subscribers enter "All User"
let selected_Subscribers_Mobile = ["0558908908"]

// ["Import  API","Export  API","Royal Tech Smart AP Extractions"]
//for adding new process;
let NewProcess_Name = ["Import  API","Export  API","Royal Tech Smart AP Extractions"]

//for adding new report;
let newReport_Name = []

//change report name
/* Object structure
  {
    "old_report_name":"xyz",
    "new_report_name":"xyz"
  }
*/
// let ReportchangeName = [{
//   "old_report_name": "xyz",
//   "new_report_name": "xyz"
// }]

//change process name
/* Object structure
  {
    "old_process_name":"xyz",
    "new_process_name":"xyz"
  }
*/
// let processchangeName = [{
//   "old_report_name": "xyz",
//   "new_report_name": "xyz"
// }]

async function copyDB() {
  let subscribersList
  if (selected_Subscribers_Mobile.includes('All User')) {

  }
  else {
    subscribersList = await db1
      .collection("subscribers")
      .find({
        mobile: { $in: selected_Subscribers_Mobile },
        isDelete:false
      })
      .toArray();
  }


  let srcrepInfo = await db1
    .collection("dynamicreportsqueries")
    .find({
      name: { $in: newReport_Name },
    })
    .toArray();
  let prrepInfo = await db1
    .collection("processes")
    .find({
      processName: { $in: NewProcess_Name },isDeleted:false
    })
    .toArray();
 
  
  for (let index = 0; index < subscribersList.length; index++) {
    let reparr = subscribersList[index]['features'][0]['reportList']
    let prArr = subscribersList[index]['features'][0]['processList']
    //console.log(reparr.length);

    for (let inn = 0; inn < srcrepInfo.length; inn++) {
      let fea = subscribersList[index]['features']

      reparr.push({
        "name": srcrepInfo[inn]['name'],
        "category": srcrepInfo[inn]['reportCategory'],
        "used": 0,
        "limit": 100,
        "_id": srcrepInfo[inn]['_id']
      })
      fea[0]['reportList'] = reparr
      // console.log(fea);

      await db1.collection("subscribers").updateOne({
        _id: subscribersList[index]['_id']
      }, {
        $set: { features: fea }
      })
    }
    for (let inn = 0; inn < prrepInfo.length; inn++) {
      let fea = subscribersList[index]['features']

      prArr.push({
        "processName": prrepInfo[inn]['processName'],
        "used": 0,
        "limit": 500,
        "chatLimit": null,
        "metaDataList": [],
        "_id": prrepInfo[inn]['_id'],
        "additionalInfo": []
      })
      fea[0]['processList'] = prArr

      await db1.collection("subscribers").updateOne({
        _id: subscribersList[index]['_id']
      }, {
        $set: { features: fea }
      })
    }
  }


}
