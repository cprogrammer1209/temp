const { MongoClient, ObjectId } = require("mongodb");

const sourceUrl = "mongodb://IAMdebugSUPER:iejYTshn@172.168.1.232:27017/?authSource=debug-db";
const targetUrl = "mongodb://gibotsdev:gibotsdev112233@172.168.0.235:27017/gibots-uat"

const run = async () => {
    try {
      const mClient = await MongoClient.connect(sourceUrl);
      const db = mClient.db("debug-db");


      const db1 = (await MongoClient.connect(targetUrl)).db("gibots-uat")

      const docs = await db.collection("events").find({},{sort : {_id:1}},{skip:0},{limit:1432}).toArray()

    console.log("first")
    
      await db1.collection("events").insertMany(docs)
      console.log("second")
    } catch (e) {
      console.log("error in the execution ", e);
    }
  };
  run();
  