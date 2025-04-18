
const { MongoClient } = require("mongodb");
input =  [
    "Number of Unavailable Products",
    "Average Response Time",
    "Order Placement Rate",
    "Customer Satisfaction Score (CSAT)",
    "Total RC Processed",
    "Alternative Product Suggestion Rate",
    "Distribution of Parts by Make",
    "Order Placement Rate by Car Model",
    "Customer Query Distribution by Product",
    "Top unavailable Products",
    "Location Wise Query Distribution",
    "Location Wise Order Distribution",
    "TVS Pending Order Details"
  ];

  let output=[]

  async function getTablefromReports(input){
    try{
  const uriDest =
    "mongodb://pprod:prOd121233@172.168.0.146:27017/?authSource=prod-DB";
    const client2 = new MongoClient(uriDest);
    await client2.connect();

    db2 = await client2.db("prod-DB");


    let tables = await db2.collection("dynamicreportsqueries").find({name:{$in:input}},{projection:{table:1}}).toArray();
    console.log(tables)
    tables.forEach((table)=>{
        output.push(table.table)
    }
    )
    console.log(output)
    }catch(e){
        console.log(e)
    }
  }

  getTablefromReports(input)