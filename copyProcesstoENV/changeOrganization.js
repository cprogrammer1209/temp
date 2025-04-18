const { MongoClient, ObjectId } = require('mongodb');

// Connection string and database details
const connectionString = 
 "mongodb://domo-1:domonodel@172.168.1.199:27017/?authSource=demo"
// 'mongodb://staging-SU:insjWTERY@server.gibots.com:2400/?authSource=aiqod-staging';
const dbName = 
'demo';
// 'aiqod-staging';

// Variables for the operation
const processName = 'My Knowledge Hub (Upload)';
const newOrgId = new ObjectId('662b515be421fedde2247c47');
const newSubscriberId = new ObjectId('5beaabd82ac6767c86dc311c');
// const newOrgId = new ObjectId('66e97e7fce7c93be4809b43d');
// const newSubscriberId = new ObjectId('66e97e7fce7c93be4809b43c');

// Async function to perform the update
async function updateDocuments() {
    const client = new MongoClient(connectionString, { useNewUrlParser: true, useUnifiedTopology: true });

    try {
        // Connect to MongoDB
        await client.connect();
        console.log('Connected to MongoDB');

        const db = client.db(dbName);

        // Update in the processes collection
        const processesCollection = db.collection('processes');
        const processResult = await processesCollection.updateOne(
            { processName: processName },
            { $set: { orgId: newOrgId, subscriberId: newSubscriberId } }
        );

        console.log(`Matched ${processResult.matchedCount} document(s) and modified ${processResult.modifiedCount} in the processes collection.`);

        // Update in the projects collection
        const projectsCollection = db.collection('projects');
        const projectResult = await projectsCollection.updateOne(
            { name: processName },
            { $set: { orgId: newOrgId, subscriberId: newSubscriberId } }
        );

        console.log(`Matched ${projectResult.matchedCount} document(s) and modified ${projectResult.modifiedCount} in the projects collection.`);
    } catch (error) {
        console.error('Error updating documents:', error);
    } finally {
        // Ensure that the client will close when you finish/error
        await client.close();
    }
}

// Execute the function
updateDocuments();
