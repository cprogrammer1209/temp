const { MongoClient,ObjectId } = require('mongodb');

// Source and target MongoDB connection URIs
const sourceUri = 'mongodb://ACHECK-DEV:DEV1VZJ@172.168.0.235:27017/?authSource=ACHECK-DB'; // Replace with your source server URI
const targetUri = 'mongodb://domo-1:domonodel@172.168.1.199:27017/?authSource=demo'; // Replace with your target server URI

// Database and collection names
const sourceDBName = 'ACHECK-DB';
const targetDBName = 'demo';
const collectionName = 'products';

async function copyCollectionBetweenServers() {
    const sourceClient = new MongoClient(sourceUri);
    const targetClient = new MongoClient(targetUri);
  
    try {
      // Connect to both servers
      await sourceClient.connect();
      await targetClient.connect();
      console.log('Connected to both MongoDB servers.');
  
      // Access source and target databases
      const sourceDb = sourceClient.db(sourceDBName);
      const targetDb = targetClient.db(targetDBName);
  
      const toSearch = {
        _id: {
          $in: [
            new ObjectId("666306e4f0c9eab1874208f0"),
            new ObjectId("6663067df0c9eab1874208e4"),
            new ObjectId("66a8c84db0f927547e0591ee"),
            new ObjectId("6704d943358281ce7b8cb8c9"),
            new ObjectId("66ed1f9e45bd0636b1fa274e"),
          ],
        },
      };
  
      // Fetch documents from source collections
      const documents = await sourceDb.collection("dynamicreportsqueries").find(toSearch).toArray();
  
      if (documents.length === 0) {
        console.log('No documents found in the source collection.');
        return;
      }
  
      console.log(`${documents.length} documents found in dynamicreportsqueries.`);
  
      const queryDescrIds = documents.map((item) => item.queryDescrId);
      const tableNames = documents.map((item) => item.table);
  
      const queryDescriptors = await sourceDb.collection("querydescriptors").find({
        _id: { $in: queryDescrIds },
      }).toArray();
  
      const tableMetadatas = await sourceDb.collection("tablemetadatas").find({
        tableName: { $in: tableNames },
      }).toArray();
  
      console.log(`${queryDescriptors.length} querydescriptors found.`);
      console.log(`${tableMetadatas.length} tablemetadatas found.`);
  
      // Prepare upsert operations for target collections
      const dynamicReportsOps = documents.map((doc) => ({
        replaceOne: {
          filter: { _id: doc._id },
          replacement: doc,
          upsert: true,
        },
      }));
  
      const queryDescriptorOps = queryDescriptors.map((doc) => ({
        replaceOne: {
          filter: { _id: doc._id },
          replacement: doc,
          upsert: true,
        },
      }));
  
      const tableMetadataOps = tableMetadatas.map((doc) => ({
        replaceOne: {
          filter: { tableName: doc.tableName },
          replacement: doc,
          upsert: true,
        },
      }));
  
      // Perform bulk upserts in target collections
      if (dynamicReportsOps.length > 0) {
        const result = await targetDb.collection("dynamicreportsqueries").bulkWrite(dynamicReportsOps);
        console.log(`${result.modifiedCount + result.upsertedCount} documents upserted in dynamicreportsqueries.`);
      }
  
      if (queryDescriptorOps.length > 0) {
        const result = await targetDb.collection("querydescriptors").bulkWrite(queryDescriptorOps);
        console.log(`${result.modifiedCount + result.upsertedCount} documents upserted in querydescriptors.`);
      }
  
      if (tableMetadataOps.length > 0) {
        const result = await targetDb.collection("tablemetadatas").bulkWrite(tableMetadataOps);
        console.log(`${result.modifiedCount + result.upsertedCount} documents upserted in tablemetadatas.`);
      }
  
    } catch (error) {
      console.error('Error while copying collections between servers:', error);
    } finally {
      // Close both connections
      await sourceClient.close();
      await targetClient.close();
      console.log('Connections to both servers closed.');
    }
  }
  

// Run the function
copyCollectionBetweenServers();
