const MongoClient = require("mongodb").MongoClient;

const run = async () => {

    try{
        const mClient = await MongoClient.connect(
          "mongodb://domo-1:domonodel@172.168.1.199:27017/?authSource=demo"//"mongodb://staging:stage789@server.gibots.com:2400/?authSource=aiqod-staging"
        );
        const db = mClient.db("demo")//"aiqod-staging");
        const tableData = await db
          .collection("tablemetadatas")
          .find({})
          .toArray();
        console.log(tableData);

    }
    catch(err){
        console.log(err)
    }
};

run();
