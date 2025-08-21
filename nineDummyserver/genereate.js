const express = require("express");
const bodyParser = require("body-parser");
const cors = require("cors");
const path = require("path");
const fs = require('fs/promises');
const axios = require('axios');
const { MongoClient,ObjectId } = require("mongodb");
const uriSrc = "mongodb://staging:stage789@172.168.1.19:27017/?authSource=aiqod-staging"; //stage
const client1 = new MongoClient(uriSrc);


const app = express();
const PORT = 3000;

// Middleware
app.use(bodyParser.json({ limit: "10mb" })); // Allows sending large HTML content
app.use(cors()); // Enable CORS for external requests

app.post("/scrapper/testing", async (req, res) => {
    try {
        await client1.connect();
        const db = await client1.db("aiqod-staging"); //stage   
        console.log(`Running Node.js version: ${process.version}`);
        
        const data = await db.collection("prasannaPurpleBuses").find({}).toArray();
        console.log(data)

        return res.status(200).json("Hello");
        

    } catch (error) {
        res.status(500).json({ error: "Error generating PDF", details: error.message });
    }
});

app.get("/scrapper/check",async (req, res) => {
    try {
        console.log(`Running Node.js version: ${process.version}`);
        
        console.log("shdjshdg")
        return res.status(200).json("uHGDFUASHDFLKJASHDLASHDFASHDFHU");
        

    } catch (error) {
        res.status(500).json({ error: "Error generating PDF", details: error.message });
    }
})


app.post("/scrapper/playwright", async (req, res) => {
    
    try {
        console.log("Request body ",req.body)
        await client1.connect();
        const db = await client1.db("aiqod-staging"); 
        const { input,orgId, subscriberId,userId} = req.body;
	console.log("hello ", input,orgId, subscriberId,userId)
        console.log(`Running Node.js version: ${process.version}`);
        
        if (input== '' || !input) {
            throw new Error("Missing htmlContent in request body" );
        }
        if (orgId== '' || !orgId) {
            throw new Error( "Missing orgId in request body" );
        }
        if (subscriberId== '' || !subscriberId) {
            throw new Error( "Missing subscriberId in request body" );
        }
        if (userId== '' || !userId) {
            throw new Error({ error: "Missing userId in request body" });
        }
        res.status(200).json("Success FUlly done");
        let route = input.route;
        console.log("Route",route)
        if(route.length == 0){
            throw new Error({ error: "Missing route in request body" });
        }
        let response = {}
        console.log("Before paytm")
        try{
            const resData= await searchPaytm(route);
            response['paytm'] =resData.data
        }catch(e){
            console.log("Error in paytm",e)
            response['paytm'] ="no buses found";
        }
        console.log("After paytm")
        console.log("Before searchAbhiBus")
        
        try{
            const resData= await searchAbhiBus(route);
            response['abhibus'] =resData.data
        }catch(e){
            console.log("Error in paytm",e)
            response['abhibus'] ="no buses found";
        }
        console.log("After searchAbhiBus")
        console.log("Before searchRedBus")
        
        try{
            const resData= await searchRedBus(route);
            response['redbus'] =resData.data
        }catch(e){
            console.log("Error in paytm",e)
            response['redbus'] ="no buses found";
        }
        console.log("After searchRedBus")

        const formattedDate = new Date().toLocaleDateString('en-GB').replaceAll('/', '-'); 

        // console.log("+++++++++++++++++++++++   ",response,"____________+++++++++++++++");
        let prompt =`
        You are given raw scrapped data from the different booking websites that contains information about multiple bus services on various routes. Each bus entry includes a departure time and ratings from different platforms such as Redbus, Paytm, and AbhiBus.

        Your task is to extract structured data from the scrapped data  and format it as a valid JSON object using the schema provided below.

        Scrapped data : ${JSON.stringify(response)}
        Today's date is ${formattedDate}.  


        Input Details:
        Each row in the table represents a bus trip on a specific route.
        Departure times are listed alongside platform ratings.
        Ratings are associated with platform names, typically as columns labeled Redbus, Paytm, and AbhiBus.
        For the Redbus platfoem, there is a field called srpRanking, which is the ranking of the bus in the redbus platform. 
        for each route, there will be a srpRanking will be available along with the scrapped data. 
        the srp ranking will have around exactly 7 values. the first value is the ranking for today and the rest of the values are for the next 6 days. So you need to take only the first value for today and ignore the rest of the values.
        The srp raking will be like 'Bus 1 Ranking', 'Bus 2 Ranking' and so on. This will contain extactly as count as the bus count which is scrapped.
        It is very crucial that the srp ranking should be mapped according to the bus. Becuase the scrapped bus data and the srp ranking will be in the same order. So you need to map the srp ranking according to the bus. 
        Dates may appear as section headers in the table (e.g., "21 Apr", "22 Apr") and apply to all entries beneath them until the next date header appears.
        
        
        Output Requirements:
        Group all trips under the correct route name.
        For each route, list the departure time and the corresponding platform ratings for each bus trip.
        It is very crucial that  the departure time will be mapped correctly since the departure time is in both railway and 12-hour format in different booking platforms.
        It is very crucial that the time should be in correct format, usally it will be in 12 hour format, if it is in 24 hour format then convert it to 12 hour format.
        ANd also it is very crucial that am and pm should be correct
        Only extract the following fields: startTime, date, and ratings per platform.
        Ensure platform ratings are mapped correctly to their respective departure times.
        Skip any rating fields that are empty or marked as unavailable.
        For the Redbus platfoem, there is a field called srpRanking, which is the ranking of the bus in the redbus platform. 
        for each route, there will be a srpRanking will be available along with the scrapped data. 
        the srp ranking will have around exactly 7 values. the first value is the ranking for today and the rest of the values are for the next 6 days. So you need to take only the first value for today and ignore the rest of the values.
        The srp raking will be like 'Bus 1 Ranking', 'Bus 2 Ranking' and so on. This will contain extactly as count as the bus count which is scrapped.
        It is very crucial that the srp ranking should be mapped according to the bus. Becuase the scrapped bus data and the srp ranking will be in the same order. So you need to map the srp ranking according to the bus. 
        The final output must be a valid JSON object.

        Instructions :
        Do not include any additional commentary or explanation—only return the JSON object.
        For the Redbus platfoem, there is a field called srpRanking, which is the ranking of the bus in the redbus platform. 
        for each route, there will be a srpRanking will be available along with the scrapped data. 
        the srp ranking will have around exactly 7 values. the first value is the ranking for today and the rest of the values are for the next 6 days. So you need to take only the first value for today and ignore the rest of the values.
        The srp raking will be like 'Bus 1 Ranking', 'Bus 2 Ranking' and so on. This will contain extactly as count as the bus count which is scrapped.
        It is very crucial that the srp ranking should be mapped according to the bus. Becuase the scrapped bus data and the srp ranking will be in the same order. So you need to map the srp ranking according to the bus. 
        There are three bus platform, redbus, paytm and abhibus. All three will have the same route ,time but the ratings will be different.
        So you need to extract the data from all three platforms and then you need to create a json object with the route with time as key  and the ratings as value.
        If in three platforms, the time for the route is same. So dont create a new entry for same route with same time.
        It is very very crucial that the route and the time entries should be duplicated, carefully analyse and give it.
        Make sure the number fields are in number type(It is very crucial to be the number field be in number type)

         Sample Output(Just for reference, never use the below data.you need to take reference to create the json from the scrapped data) 
        (It is very crucial that the output should be in the same format as below): 
        {
            "From-To": [
                { "startTime": "","srpRanking":"",  "ratings": { "Redbus": "", "Paytm": "", "AbhiBus": "" } },
            ],
            "From-To": [
            { "startTime": "", "srpRanking":"", "ratings": { "Redbus": "", "Paytm": "", "AbhiBus": "" } },
            ],
            "From-To": [
            { "startTime": "", "srpRanking":"", "ratings": { "Redbus": "", "Paytm": "", "AbhiBus": "" } },
            ]
        }

        Populate the output in the following json format : {'output':{\"responseData\": {...}}}
        `
        console.log("Prompt ",prompt)
        const openaiRes = await callopenAI(prompt);
        // let jsonData = openaiRes.output;
        let jsonData = JSON.parse(JSON.stringify(openaiRes));

        console.log(typeof jsonData, " openaiRes "+jsonData.responseData) 
        jsonData = jsonData.responseData

        
        console.log("OPenai response ", jsonData)
        
        let output = await convertExecel(jsonData);
        let excelFilePath = output['publicUrl']
        console.log("Excel file path ", excelFilePath)
        console.log("Excel json ", output['jsonData'])
        try{

            output['jsonData'] = output['jsonData'].map(item => {
                return {...item,
                    isDeleted:false,
                    createdAt:new Date(),
                    updatedAt:new Date(),
                    orgId:new ObjectId(orgId),
                    subscriberId:new ObjectId(subscriberId),
                    userId:new ObjectId(userId),
                }
            });
    
            await db.collection("purpleRatings").updateMany({},{$set:{isDeleted:true}});
            await db.collection("purpleRatings").insertMany(output['jsonData'])
        }catch(e){
            console.log("Error in inserting data ",e)
        }


        


        let userReview = await readUserReview(route);
        let reviewPrompt = `
        You are given raw, unstructured bus travel review data. Each review starts with the passenger's name, followed by details such as date and time of the trip, source and destination, rating, and review text along with the review date and time.
        Scrapped Data : ${JSON.stringify(userReview.data)}
        Today's date is ${formattedDate}

        Instructions;
        1) this is scrapped user review data from redbus, so always the platform is redbus only
        2) You need extract only the user reviews which is related to today and yesterday date,others are not needed.
        3) And also you need to alanyse the user review tone. according to the review and review tone, you have to mention whether need to esclate or not.
        4) If the review is positive or neutral then mention "no" and if the review is negative then mention "yes"
            positive scenerios :
                1) user may tell about the expirence and all
                2) user may tell about the bus and all
            Negative scenerios :
                1) User may feel that these things are not there, if added then it will be good
                2) All new features related quries,
                3) And also if the user is not happy with the service and all
                4) Sometimes, the user give above 3 star rating, but the review is negative, so you need to analyse this as well by user tone and need to determine to esclate or not.
                4) and other negative scenerios
            You need to analyse this regardless of the rating by the user,
        5) The date will be any format, so you must need to give it only in DD/MM/YYYY format 
        6) If there is no scrappped data then return "no reviews found"
        7) If the user review have like this, 
                    'Reply disabled
                    You have replied to the review'
            Then it is already replied by the execute so, no need to extract again. just ignore. 
        7) It is very crucial not extract the replied reviews

        Your task is to extract and return the following fields in a structured JSON format:
        passenger_name
        date(time of the journey)
        time (date of the journey)
        source
        destination
        rating (as a number)
        review_text
        review_date_time (when the review was written)
        platrform (e.g., Redbus)
        decription
        esclate

        Expected JSON format:
        {
        "reviews": [
            {
            "passenger_name": "Name",
            "date" : "DD/MMM/YYYY",
            time": "hh:mm AM/PM",
            "source": "SourceCity",
            "destination": "DestinationCity",
            "rating": 5,
            "review_text": "Review content",
            "review_date" : "DD/MMM/YYYY",
            "review_time": "hh:mm AM/PM",
            "platform": "Redbus",
            "description": "description",
            "esclate": "yes/no"
            },
            
            // Repeat for other reviews
        ]
        }

        In the description field, you need to give like the user review, mobile number, date and time, need like generated from the ai. It should comphrensive to understand at single read.
        It is very crucial that the description must have the mobile number, if it is mentioned.
        Use the structure of the text to identify when each new review begins. Assume that names are at the top of each review section, and that the format is consistent.
        Make sure the number fields are in number type(It is very crucial to be the number field be in number type)
        Populate the output in the following json format : {'output':{\"responseData\": {...}}}
        `

        console.log("reviewPrompt ",reviewPrompt)
        const openaiReview = await callopenAI(reviewPrompt);
        // let jsonData = openaiRes.output;
        let jsonReview = JSON.parse(JSON.stringify(openaiReview));
        console.log("Review data ",jsonReview)
        console.log(typeof jsonReview, " openaiRes "+jsonReview.responseData) 
        jsonReview = jsonReview.responseData
        jsonReview.reviews = jsonReview.reviews.map(item => {
            return {...item,
                isDeleted:false,
                createdAt:new Date(),
                updatedAt:new Date(),
                orgId:new ObjectId(orgId),
                subscriberId:new ObjectId(subscriberId),
                userId:new ObjectId(userId),
            }
        })
        console.log("Final insert data ",jsonReview.reviews)
        try{

            await db.collection("purpleReviews").updateMany({},{$set:{isDeleted:true}});
            await db.collection("purpleReviews").insertMany(jsonReview.reviews)
        }catch(e){
            console.log("Error in inserting data for review ",e)}
        
        console.log("OPenai response ", jsonReview)




        const url = "http://172.168.1.19:7894/gibots-api/bots/triggerProcess"
        const options = {
            "orgId":orgId,
            "subscriberId":subscriberId,
            "userId":userId,
            "triggerData":{
                            "additionalInfo": [
                                {
                                    "addToTaskList": false,
                                    "name": "publicUrl",
                                    "required": false,
                                    "label": "publicUrl",
                                    "value": excelFilePath,
                                    "id": "0"
                                }
                            ],
                            "customerId": "5b8fd401b3930517f134c569",
                            "processId": "680627c3eff7f475cf839148",
                            "projectId": "680627c3eff7f475cf83914e",
                            "taskDesc": "",
                            "projectName": "Automatic Prassana Automation",
                            "username": "Admin",
                            "accessControlList": [
                                {
                                    "permissionsList": {
                                        "execute": true,
                                        "view": true,
                                        "edit": true,
                                        "add": true
                                    },
                                    "controlType": "users",
                                    "controlName": "Admin",
                                    "controlId": "5beaabd82ac6767c86dc311e",
                                    "_id": "67729c4be8ea3efa77dfa76a"
                                },
                                {
                                    "permissionsList": {
                                        "execute": true,
                                        "view": true,
                                        "edit": true,
                                        "add": true
                                    },
                                    "controlType": "users",
                                    "controlName": "Deepa",
                                    "controlId": "66eac67c4b94159b93983810",
                                    "_id": "67729c4be8ea3efa77dfa769"
                                }
                            ]
                        }
        }
        await axios.post(url, options)
        console.log("Process is triggered successfully")

    } catch (error) {
        console.log("error ",error)
        res.status(400).json({ error: "Error generating PDF", details: error.message });
    }
});

async function callopenAI(prompt) { // last parameters contains info from headerParams
    const requestId = Date.now().toString();
    try {
        
        const response = await fetch('https://api.openai.com/v1/chat/completions', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer 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`,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                model: "gpt-4o-mini",
                response_format: { "type": "json_object" },
                messages: [
                    { role: "user", content: prompt }
                ],
            }),
        });

        const data = await response.json();
        console.log(data);
        const promptTokens = data.usage.prompt_tokens;
        const completionTokens = data.usage.completion_tokens;
        console.log(data.choices[0].message.content)
        const parsedData = JSON.parse(data.choices[0].message.content);
        
        const output = parsedData.output;
        console.log(output)

        
        
        return output
        
        
    } catch (error) {
        console.error('Error:', error);
        return { message: 'There was an error running this function' };
    }
}

async function readUserReview(routes) {
    try{
        const { chromium } = require('playwright');
        const { convert } = require('html-to-text');    
        let data = {};
        for (const route of routes) {
            data[route.source+"-"+route.destination] = ""
            console.log("route",route)
            const browser = await chromium.launch({ headless: false }); // Run headful to avoid detection

            try{
                const context = await browser.newContext({ });

              
                const page = await context.newPage();
              
                await page.addInitScript(() => {
                  Object.defineProperty(navigator, 'webdriver', {
                    get: () => false,
                  });
              
                  Object.defineProperty(navigator, 'plugins', {
                    get: () => [1, 2, 3, 4, 5],
                  });
              
                  Object.defineProperty(navigator, 'languages', {
                    get: () => ['en-US', 'en'],
                  });
              
                  const getParameter = WebGLRenderingContext.prototype.getParameter;
                  WebGLRenderingContext.prototype.getParameter = function (param) {
                    if (param === 37445) return 'Intel Inc.';
                    if (param === 37446) return 'Intel Iris OpenGL Engine';
                    return getParameter.call(this, param);
                  };
                });
                await page.waitForTimeout(1500);
                console.log(1)
                await page.goto('https://accounts.redbus.com/login?continue=https://www.redbus.pro/');
                await page.waitForTimeout(5000);
                console.log(2)

                await page.getByRole('textbox', { name: 'Username' }).click();
                await page.getByRole('textbox', { name: 'Username' }).fill('9748');
                await page.getByRole('textbox', { name: 'Username' }).press('Tab');
                await page.getByRole('textbox', { name: 'Password' }).click();
                await page.getByRole('textbox', { name: 'Password' }).fill('prasannapurple');
                await page.getByRole('button', { name: 'Login', exact: true }).click();
                console.log(3)
                
                  await page.locator('role=button[name="Skip"]').click();
              
                  await page.hover('aside.SideNav---sideNav---3QZiY ');
              
                  await page.locator('role=link[name="R & R"]').click();
                  await page.waitForTimeout(5000);
                  console.log(4)
                
                  await page.click("#reviews_tab")
                  const response = await page.waitForResponse(response =>
                    response.url().includes('https://www.redbus.pro/win/api/ratingsReviews/getAllReviewsRnR/0') && response.status() === 200
                  );
                  await page.waitForTimeout(1000);
                  const inputSelector = 'input[placeholder="Source"]'; 
                  console.log(5)
              
                  await page.waitForSelector(inputSelector);
                  await page.click(inputSelector);
                  await page.waitForTimeout(2000);
                  await page.fill(inputSelector, route.redBusSource);
                  await page.waitForTimeout(2000);
                  await page.locator('#react-autowhatever-1 #react-autowhatever-1--item-0').click();
                  await page.waitForTimeout(2000);
                console.log(6)
                  
              
                  const inputSelector1 = 'input[placeholder="Destination"]'; 
              
                  await page.waitForSelector(inputSelector1);
                  await page.click(inputSelector1);
                  await page.waitForTimeout(2000);
                  await page.fill(inputSelector1, route.redBusDestination);
                  await page.locator('#react-autowhatever-1 #react-autowhatever-1--item-0').click();
                  await page.waitForTimeout(2000);
                console.log(7)
                  
              
                  const filterBtnSelector = 'button:has-text("Filter")';
                  await page.waitForSelector(filterBtnSelector, { state: 'visible' });
                  await page.click(filterBtnSelector);
                  await page.waitForTimeout(2000);
                console.log(8)
                  
                  let count = 0;
                  while (count < 3) {
                    count++
                    await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));      
                    await page.waitForTimeout(1000);  
                    
                  }
                console.log(9)
                  
                  const busCard = await page.locator('div.AllRatings---containerDomestic---3_5gZ').innerHTML();
                    // console.log(busCard)
                    const text = convert(busCard, {
                      wordwrap: false, // optional: prevents line breaks
                      selectors: [
                        { selector: 'a', options: { hideLinkHrefIfSameAsText: true } },
                        {            selector: 'div',            format: 'block'          }
                      ]
                    });
                console.log(10)

                    data[`${route.source}-${route.destination}`] = text;
                    await browser.close();
            }catch(e)   {
                console.log("Error in paytm",e)
                data[`${route.source}-${route.destination}`] = "no buses found";
                await browser.close();

            }
            // console.log("res 1234 ",response)
        }

        return {status:0,msg:"success",data:data};

    }catch(e){
        console.log("Error in reading user review",e);
        return {status:1,msg:"error",data:e};
    }
}
async function convertExecel(jsonData) {
    const XLSX = require('xlsx');
    const fs = require('fs');   
    const sheetData = [];
    let timestamp = Date.now();
    const formattedDate = new Date().toLocaleDateString('en-GB').replaceAll('/', '-'); // dd/mm/yyyy
    console.log(formattedDate);

    console.log("timestamp ",timestamp)
    Object.keys(jsonData).forEach(route => {
      jsonData[route].forEach(item => {
        sheetData.push({
          Route: route,
          Time: item.startTime,
          'SRP Ranking': item.srpRanking,
          Redbus_Rating: item.ratings.Redbus,
          Paytm_Rating: item.ratings.Paytm,
          AbhiBus_Rating: item.ratings.AbhiBus
        });
      });
    });
    
    // Convert JSON data to worksheet
    const ws = XLSX.utils.json_to_sheet(sheetData);
    
    // Create a new workbook with the worksheet
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, 'Bus Ratings');
    let output={}

    let filepath= path.join("E:/test/public/excel", 'ExcelSheets', `excel-${timestamp}-${formattedDate}.xlsx`)
    output['filepath'] =filepath
    console.log("first path ",filepath)
    // Write the Excel file to disk
    XLSX.writeFile(wb, filepath);
    publicUrl= "https://172.168.1.22/public/excel/ExcelSheets/"+`excel-${timestamp}-${formattedDate}.xlsx`
     output['publicUrl'] =publicUrl
     output['jsonData'] = sheetData
    console.log("Public URL ",publicUrl)

    return output;

    
}
async function searchPaytm(routes){
    try{
        const { chromium } = require('playwright');
        const { convert } = require('html-to-text');    
        let response = {};
        for (const route of routes) {
            response[route.paytmBusSource+"-"+route.paytmBusDestination] = ""
            console.log("route",route)
            const browser = await chromium.launch({ headless: false }); // Run headful to avoid detection

            try{
                const context = await browser.newContext({ });

              
                const page = await context.newPage();
                await page.waitForTimeout(1500);
                console.log(1)
                    
                    await page.goto('https://tickets.paytm.com/bus/');
                await page.waitForTimeout(5000);
                console.log(2)

                    await page.getByRole('textbox', { name: 'From' }).click();
                    await page.getByRole('textbox', { name: 'From' }).fill(route.paytmBusSource);
                    await page.waitForTimeout(3000)
                    console.log(1)

                    // await page.getByText('PuneMaharashtra', { exact: true }).click();
                    await page.waitForSelector('#source-section .dcrjM');
                    await page.click('#source-section .dcrjM >> nth=0');
                    await page.getByRole('textbox', { name: 'To' }).click();
                    await page.getByRole('textbox', { name: 'To' }).fill(route.paytmBusDestination);
                    await page.waitForTimeout(3000)
                console.log(3)

                    
                    await page.waitForSelector('#destination-section .dcrjM');
                    await page.click('#destination-section .dcrjM >> nth=0');
                console.log(4)

                    // await page.getByText('NagpurMaharashtra', { exact: true }).click();
                    await page.getByRole('button', { name: 'Search Buses' }).click();
                    await page.waitForTimeout(5000)
                    await page.getByRole('textbox', { name: 'Search Operators' }).click();
                    await page.getByRole('textbox', { name: 'Search Operators' }).fill('prasanna');
                    await page.locator('div').filter({ hasText: /^Bus operatorsPrasanna - Purple Bus$/ }).getByLabel('unchecked').click();
                console.log(5)

                    let count = 0;
                    while (count < 3) {
                    console.log("count scroll",count)
                    count++
                    await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));      
                    await page.waitForTimeout(1000);      
                    }
                    
                    const busCard = await   page.locator('div.-iAp6').innerHTML();
                    // console.log(busCard)
                    const text = convert(busCard, {
                    wordwrap: false, // optiresponseonal: prevents line breaks
                    selectors: [
                        { selector: 'a', options: { hideLinkHrefIfSameAsText: true } }
                    ]
                    });
                console.log(6)

                    response[`${route.paytmBusSource}-${route.paytmBusDestination}`] = text;
                    await browser.close();
            }catch(e)   {
                console.log("Error in paytm",e)
                response[`${route.paytmBusSource}-${route.paytmBusDestination}`] = "no buses found";
                await browser.close();

            }
            // console.log("res 1234 ",response)
        }

        return {status:0,msg:"success",data:response};
    }catch(e){
        console.log(e);
        return {status:1,msg:"error",data:e};
    }
}

async function searchAbhiBus(routes){
    try{
        const { chromium } = require('playwright');
        const { convert } = require('html-to-text');    
        let response = {};
        for (const route of routes) {
            response[route.abhiBusSource+"-"+route.abhiBusDestination] = ""
            console.log("route",route)
            const browser = await chromium.launch({ headless: false }); // Run headful to avoid detection

            try{
                const context = await browser.newContext({ });
              
                const page = await context.newPage();
                await page.waitForTimeout(1500);
                console.log(1)

                    await page.goto('https://www.abhibus.com/');
                await page.waitForTimeout(5000);
                console.log(2)

                    await page.getByRole('textbox', { name: 'Leaving From' }).click();
                    await page.getByRole('textbox', { name: 'Leaving From' }).fill(route.abhiBusSource);
                    await page.waitForTimeout(5000)

                        await page.waitForSelector('div.auto-complete-drop-down .auto-complete-list');
                    await page.click('.auto-complete-list .auto-complete-list-item >> nth=0');
                console.log(3)

                    //   await page.getByText('Pune', { exact: true }).click();
                    await page.getByRole('textbox', { name: 'Going To' }).click();
                    
                    await page.getByRole('textbox', { name: 'Going To' }).fill(route.abhiBusDestination);
                    await page.waitForTimeout(5000)
                        await page.waitForSelector('div.auto-complete-drop-down .auto-complete-list');
                    await page.click('.auto-complete-list .auto-complete-list-item >> nth=0');
                    //   await page.getByRole('listitem').filter({ hasText: 'NagpurMaharashtra' }).locator('small').click();
                    // await page.getByRole('button', { name: 'Today' }).click();
                    await page.click('text=Today');

                    await page.waitForTimeout(3000)
                console.log(4)


                    await page.getByText('Bus Partner').click();
                    await page.getByRole('textbox', { name: 'Search here' }).click();
                    await page.waitForTimeout(3000)
                    console.log(5)

                    await page.getByRole('textbox', { name: 'Search here' }).fill('Prasanna - Purple Bus');
                    await page.waitForTimeout(3000)
                    console.log(6)

                    await page.locator('#list-filter-option-container').getByRole('checkbox').check();
                    await page.waitForTimeout(1500)
                console.log(7)

                    let count = 0;
                    while (count < 3) {
                        console.log("count scroll",count)
                        count++
                        await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));      
                        await page.waitForTimeout(1000);      
                    }


                    const busCard = await page.locator('div#service-cards-container').innerHTML();
                    // console.log(busCard)
                    const text = convert(busCard, {
                        wordwrap: false, // optional: prevents line breaks
                        selectors: [
                        { selector: 'a', options: { hideLinkHrefIfSameAsText: true } }
                        ]
                    });
                console.log(8)

                    response[`${route.abhiBusSource}-${route.abhiBusDestination}`] = text;
                    await browser.close();
                }catch(e){
                    console.log("Error in abhibus",e)
                    response[`${route.abhiBusSource}-${route.abhiBusDestination}`] = "no buses found";
                    await browser.close();

                }
            // console.log("res 1234 ",response)
        }

        return {status:0,msg:"success",data:response};
    }catch(e){
        console.log(e);
        return {status:1,msg:"error",data:e};
    }
}
async function searchRedBus(routes){
    try{
        const { chromium } = require('playwright');
        const { convert } = require('html-to-text');    
        let response = {};
        for (const route of routes) {
            response[route.redBusSource+"-"+route.redBusDestination] = {}
            console.log("route",route)
            const browser = await chromium.launch({ headless: false }); // Run headful to avoid detection

            try{
                const context = await browser.newContext({ });

              
                const page = await context.newPage();
                        
                            await page.addInitScript(() => {
                            Object.defineProperty(navigator, 'webdriver', {
                                get: () => false,
                            });
                        
                            Object.defineProperty(navigator, 'plugins', {
                                get: () => [1, 2, 3, 4, 5],
                            });
                        
                            Object.defineProperty(navigator, 'languages', {
                                get: () => ['en-US', 'en'],
                            });
                        
                            const getParameter = WebGLRenderingContext.prototype.getParameter;
                            WebGLRenderingContext.prototype.getParameter = function (param) {
                                if (param === 37445) return 'Intel Inc.';
                                if (param === 37446) return 'Intel Iris OpenGL Engine';
                                return getParameter.call(this, param);
                            };
                            });
                await page.waitForTimeout(1500);
                console.log(1)
                            
                            await page.goto('https://accounts.redbus.com/login?continue=https://www.redbus.pro/');
                await page.waitForTimeout(5000);

                            await page.getByRole('textbox', { name: 'Username' }).click();
                            await page.getByRole('textbox', { name: 'Username' }).fill('9748');
                            await page.getByRole('textbox', { name: 'Username' }).press('Tab');
                            await page.getByRole('textbox', { name: 'Password' }).click();
                            await page.getByRole('textbox', { name: 'Password' }).fill('prasannapurple');
                            await page.getByRole('button', { name: 'Login', exact: true }).click();
                console.log(2)
                        
                            await page.locator('role=button[name="Skip"]').click();
                console.log(3)
                            
                            await page.hover('aside.SideNav---sideNav---3QZiY ');
                        
                            await page.locator('role=link[name="R & R"]').click();
                            await page.waitForTimeout(5000);
                console.log(4)
                            
                            // await page.click("#servicewise_tab")
                            await page.waitForTimeout(1000);
                            const inputSelector = 'input[placeholder="Source"]'; 
                            await page.waitForSelector(inputSelector);
                            await page.click(inputSelector);
                console.log(5)
                            
                            await page.waitForTimeout(2000);
                            await page.fill(inputSelector, route.redBusSource);
                            await page.waitForTimeout(2000);
                            await page.locator('#react-autowhatever-1 #react-autowhatever-1--item-0').click();
                            await page.waitForTimeout(2000);
                        
                        
                            const inputSelector1 = 'input[placeholder="Destination"]'; 
                        
                            await page.waitForSelector(inputSelector1);
                            await page.click(inputSelector1);
                console.log(6)
                            
                            await page.waitForTimeout(2000);
                            await page.fill(inputSelector1, route.redBusDestination);
                            await page.locator('#react-autowhatever-1 #react-autowhatever-1--item-0').click();
                            await page.waitForTimeout(2000);
                        
                        
                            const filterBtnSelector = 'button:has-text("Filter")';
                            await page.waitForSelector(filterBtnSelector, { state: 'visible' });
                            await page.click(filterBtnSelector);
                console.log(7)
                            
                            await page.waitForTimeout(2000);
                            
                            let count = 0;
                            while (count < 3) {
                                count++
                                await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));      
                                await page.waitForTimeout(1000);      
                            }
                            
                        
                            const busCard = await page.locator('#serviceWiseScroll').innerHTML();
                            
                                const text = convert(busCard, {
                                wordwrap: false, 
                                selectors: [
                                    { selector: 'a', options: { hideLinkHrefIfSameAsText: true } },
                                    {            selector: 'div',            format: 'block'          }
                                ]
                                });
                console.log(8)

                    response[`${route.redBusSource}-${route.redBusDestination}`] = {};
                    response[`${route.redBusSource}-${route.redBusDestination}`]['BusRatings'] = text;

                    console.log('srp ranking extraction started');

                    await page.waitForSelector('span:has-text("View trend")');

                    const calendarIcons = await page.locator('img[alt*="calendar"]').all();
                  
                    console.log(`Total calendar icons found: ${calendarIcons.length}`);
                        response[`${route.redBusSource}-${route.redBusDestination}`]['srpRanking'] = {};
                            
                    for (let i = 0; i < calendarIcons.length; i++) {
                      try {
                    console.log('srp ranking extraction started ',i);

                        const calendarIcon = calendarIcons[i];
                        // await calendarIcon.click();
                  
                        await Promise.all([
                          // Trigger the API call
                          calendarIcon.click(),
                        
                          // Wait for the specific API call to complete
                          page.waitForResponse(response =>
                            response.url().includes('/win/api/ratingsReviews/getSrpRank') &&
                            response.status() === 200
                          )
                        ]);
                        
                  
                        // Wait for ranking popup
                        const rankSelector = 'div[class*="RNRCalendar---rankTextDiv"]';
                        await page.waitForSelector(rankSelector, { timeout: 5000 });
                  
                        const rankElements = await page.locator(rankSelector).allTextContents();
                        console.log(`\nService ${i + 1} Rankings:`);
                        rankElements.forEach(rank => console.log(rank));
                        response[`${route.redBusSource}-${route.redBusDestination}`]['srpRanking'][`Bus ${i + 1} Rankings`] = rankElements;


                  
                        // Close the popup RNRCalendar---closeDiv---20D9a
                        await page.locator('div[class*="RNRCalendar---headerDiv"] >> nth=-1').click();
                        await page.locator('div.RNRCalendar---closeDiv---20D9a').click();
                        await page.waitForTimeout(1000);
                      } catch (err) {
                        console.error(`Error in Service ${i + 1}: ${err.message}`);
                      }
                    }
                    
                    await browser.close();
                }catch(e){
                    console.log("Error in abhibus",e)
                    response[`${route.redBusSource}-${route.redBusDestination}`] = "no buses found";
                    await browser.close();

                }
            // console.log("res 1234 ",response)
        }

        return {status:0,msg:"success",data:response};
    }catch(e){
        console.log(e);
        return {status:1,msg:"error",data:e};
    }
}


// Start the Server
app.listen(PORT, () => {
    console.log(`🚀 Server running on http://localhost:${PORT}`);
});


