const { MongoClient, ObjectId } = require("mongodb");
const fs = require("fs");

const url = "mongodb://domo-1:domonodel@172.168.1.199:27017/?authSource=demo";

const filePaths = [];
const imgPaths = [];

const run = async () => {
  try {
    const mClient = await MongoClient.connect(url);
    const db = mClient.db("demo");
    const userId = "6666b0495febf1ebac5d5343";

    const result = await db
      .collection("fileuploadhistories")
      .find(
        { userId: new ObjectId("6666b0495febf1ebac5d5343") },
        { projection: { filePath: 1, imagesPath: 1, _id: 0 } }
      )
      // .limit(1)
      .toArray();

    // console.log(result)
    result.forEach((item) => {
      filePaths.push(item.filePath);

      if (item.imagesPath) {
        item.imagesPath.forEach((e) => {
          imgPaths.push(e.imageFilePath);
        });
      }
    });

    fs.writeFileSync("filePath.txt", filePaths.join());
    fs.writeFileSync("imagePath.txt",imgPaths.join());
    console.log("Data has been appended to the file successfully!");
  } catch (e) {
    console.log("error in the execution ", e);
  }
};
run();
