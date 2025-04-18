const { MongoClient } = require("mongodb");
const mongoose = require("mongoose");
const ObjectId = mongoose.Types.ObjectId;
const fs = require('fs/promises');
// const EJSON = require('ejson');
// const superjson = require("superjson");


let db1, db2;

async function main() {
    const uriSrc =    "mongodb://domo-1:domonodel@172.168.1.199:27017/?authSource=demo";
    const client1 = new MongoClient(uriSrc);
    const superjson = await import("superjson");

    try {
        // Connect to the MongoDB cluster
        await client1.connect();
    
        db1 = await client1.db("demo");
        console.log("Connected to source database");


        const response = await db1.collection("scanningfields").find({documentType:"Income_Certificate"}).toArray();
        console.log(response.length);
        console.log(response);

        if(response.length > 0){
            for(let i=0; i<response.length; i++){
                const document = response[i];
                const jsonString = superjson.stringify(document);
                await fs.writeFile(`./backup/${document.documentType}.json`, JSON.stringify(jsonString, null, 2));

                const jsonData = await fs.readFile(`./backup/${document.documentType}.json`, "utf-8");
                console.log(jsonData)
                
            }
        }
        client1.close();
    } catch (e) {
        console.error(e);
    }
}


function convertObjectIds(doc) {
    if (Array.isArray(doc)) {
        return doc.map(convertObjectIds);
    } else if (doc && typeof doc === 'object') {
        return Object.keys(doc).reduce((acc, key) => {
            if (doc[key] instanceof ObjectId) {
                acc[key] = { "$oid": doc[key].toHexString() };
            } else {
                acc[key] = convertObjectIds(doc[key]);
            }
            return acc;
        }, {});
    }
    return doc;
}
main().catch(console.error);