const { MongoClient } = require('mongodb');

// Source and target MongoDB connection URIs
const sourceUri = 'mongodb://debug-nodelete:ThsnYU@172.168.1.232:27017/?authSource=debug-db'; // Replace with your source server URI
const targetUri = 'mongodb://domo-1:domonodel@172.168.1.199:27017/?authSource=demo'; // Replace with your target server URI

// Database and collection names
const sourceDBName = 'debug-db';
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

    // Access source and target databases and collections
    const sourceDB = sourceClient.db(sourceDBName);
    const targetDB = targetClient.db(targetDBName);

    const sourceCollection = sourceDB.collection(collectionName);
    const targetCollection = targetDB.collection(collectionName);

    // Fetch all documents from the source collection
    const documents = await sourceCollection.find().toArray();
    console.log(documents.length + '      Nsdfasdfasdf asdfa sfasd documents found in the source collection.');

    // Insert documents into the target collection
    if (documents.length > 0) {
      const result = await targetCollection.insertMany(documents);
      console.log(`${result.insertedCount} documents copied to ${targetDBName}.${collectionName}`);
    } else {
      console.log('No documents found in the source collection.');
    }
  } catch (error) {
    console.error('Error while copying collection between servers:', error);
  } finally {
    // Close both connections
    await sourceClient.close();
    await targetClient.close();
    console.log('Connections to both servers closed.');
  }
}

// Run the function
copyCollectionBetweenServers();
