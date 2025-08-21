const express = require("express");
const bodyParser = require("body-parser");
const cors = require("cors");
const path = require("path");
const fs = require('fs/promises');
const axios = require('axios');


const app = express();
const PORT = 3000;

// Middleware
app.use(bodyParser.json({ limit: "10mb" })); // Allows sending large HTML content
app.use(cors()); // Enable CORS for external requests

app.post("/scrapper/testing", async (req, res) => {
    try {
        console.log(`Running Node.js version: ${process.version}`);
        

        return res.status(200).json("Hello");
        

    } catch (error) {
        res.status(500).json({ error: "Error generating PDF", details: error.message });
    }
});

app.get("/scrapper/check",async (req, res) => {
    try {
        console.log(`Running Node.js version: ${process.version}`);
        

        return res.status(200).json("Hello");
        

    } catch (error) {
        res.status(500).json({ error: "Error generating PDF", details: error.message });
    }
})


app.post("/scrapper/playwright", async (req, res) => {
    try {
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


        // console.log("+++++++++++++++++++++++   ",response,"____________+++++++++++++++");
        let prompt =`
        You are given raw scrapped data from the different booking websites that contains information about multiple bus services on various routes. Each bus entry includes a departure time and ratings from different platforms such as Redbus, Paytm, and AbhiBus.

        Your task is to extract structured data from the scrapped data  and format it as a valid JSON object using the schema provided below.

        Scrapped data : ${JSON.stringify(response)}

        

        Sample Output(Just for reference, never use the below data, need to create the json from the scrapped data) : 
        {
            "From-To": [
                { "startTime": "", "ratings": { "Redbus": "", "Paytm": "", "AbhiBus": "" } },
            ],
            "From-To": [
            { "startTime": "", "ratings": { "Redbus": "", "Paytm": "", "AbhiBus": "" } },
            ],
            "From-To": [
            { "startTime": "", "ratings": { "Redbus": "", "Paytm": "", "AbhiBus": "" } },
            ]
        }

        Input Details:
        Each row in the table represents a bus trip on a specific route.
        Departure times are listed alongside platform ratings.
        Ratings are associated with platform names, typically as columns labeled Redbus, Paytm, and AbhiBus.
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
        The final output must be a valid JSON object.

        Do not include any additional commentary or explanation—only return the JSON object.
        It is very very crucial that the route and the time entries should be duplicated, carefully analyse and give it.
        Populate the output in the following json format : {'output':{\"responseData\": {...}}}
        `
        // console.log("Prompt ",prompt)
        const openaiRes = await callopenAI(prompt);
        // let jsonData = openaiRes.output;
        let jsonData = JSON.parse(JSON.stringify(openaiRes));

        console.log(typeof jsonData, " openaiRes "+jsonData.responseData) 
        jsonData = jsonData.responseData

        
        console.log("OPenai response ", jsonData)

        let excelFilePath = await convertExecel(jsonData);
        console.log("Excel file path ", excelFilePath)
        const url = "https://staging.aiqod.com:843/gibots-api/bots/triggerProcess"
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
async function convertExecel(jsonData) {
    const XLSX = require('xlsx');
    const fs = require('fs');   
    const sheetData = [];
    let timestamp = Date.now();
    const formattedDate = new Date().toLocaleDateString('en-GB').replaceAll('/', '-');; // dd/mm/yyyy
    console.log(formattedDate);

    console.log("timestamp ",timestamp)
    Object.keys(jsonData).forEach(route => {
      jsonData[route].forEach(item => {
        sheetData.push({
          Route: route,
          Time: item.startTime,
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
    let filepath = path.join("E:/test/public/excel", 'ExcelSheets', `excel-${timestamp}-${formattedDate}.xlsx`)
    console.log("first path ",filepath)
    // Write the Excel file to disk
    XLSX.writeFile(wb, filepath);

    let publicUrl = "https://automation.aiqod.com/public/excel/ExcelSheets/"+`excel-${timestamp}-${formattedDate}.xlsx`
    console.log("Public URL ",publicUrl)

    return publicUrl;

    
}
async function searchPaytm(routes){
    try{
        const { chromium } = require('playwright');
        const { convert } = require('html-to-text');    
        let response = {};
        for (const route of routes) {
            response[route.source+"-"+route.destination] = ""
            console.log("route",route)
            try{
                    const browser = await chromium.launch(
                        { headless: false ,
                        args: ['--window-size=1280,800', '--window-position=100,100']
                        }
                    );
                    const context = await browser.newContext();
                    const page = await context.newPage();
                    
                    await page.goto('https://tickets.paytm.com/bus/');
                    await page.getByRole('textbox', { name: 'From' }).click();
                    await page.getByRole('textbox', { name: 'From' }).fill(route.source);
                    // await page.getByText('PuneMaharashtra', { exact: true }).click();
                    await page.waitForSelector('#source-section .dcrjM');
                    await page.click('#source-section .dcrjM >> nth=0');
                    await page.getByRole('textbox', { name: 'To' }).click();
                    await page.getByRole('textbox', { name: 'To' }).fill(route.destination);
                    await page.waitForTimeout(1000)
                    
                    
                    await page.waitForSelector('#destination-section .dcrjM');
                    await page.click('#destination-section .dcrjM >> nth=0');
                    
                    // await page.getByText('NagpurMaharashtra', { exact: true }).click();
                    await page.getByRole('button', { name: 'Search Buses' }).click();
                    await page.waitForTimeout(5000)
                    await page.getByRole('textbox', { name: 'Search Operators' }).click();
                    await page.getByRole('textbox', { name: 'Search Operators' }).fill('pras');
                    await page.locator('div').filter({ hasText: /^Bus operatorsPrasanna - Purple Bus$/ }).getByLabel('unchecked').click();
                    
                    const busCard = await page.locator('div.-iAp6').innerHTML();
                    // console.log(busCard)
                    const text = convert(busCard, {
                    wordwrap: false, // optiresponseonal: prevents line breaks
                    selectors: [
                        { selector: 'a', options: { hideLinkHrefIfSameAsText: true } }
                    ]
                    });

                    response[`${route.source}-${route.destination}`] = text;
            }catch(e)   {
                console.log("Error in paytm",e)
                response[`${route.source}-${route.destination}`] = "no buses found";
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
            response[route.source+"-"+route.destination] = ""
            console.log("route",route)
            try{
                    const browser = await chromium.launch({ headless: false });
                    const context = await browser.newContext();
                    const page = await context.newPage();

                    await page.goto('https://www.abhibus.com/');
                    await page.getByRole('textbox', { name: 'From Station' }).click();
                    await page.getByRole('textbox', { name: 'From Station' }).fill(route.source);
                    await page.waitForTimeout(5000)
                        await page.waitForSelector('div.auto-complete-drop-down .auto-complete-list');
                    await page.click('.auto-complete-list .auto-complete-list-item >> nth=0');
                    //   await page.getByText('Pune', { exact: true }).click();
                    await page.getByRole('textbox', { name: 'To Station' }).click();
                    await page.getByRole('textbox', { name: 'To Station' }).fill(route.destination);
                    await page.waitForTimeout(5000)
                        await page.waitForSelector('div.auto-complete-drop-down .auto-complete-list');
                    await page.click('.auto-complete-list .auto-complete-list-item >> nth=0');
                    //   await page.getByRole('listitem').filter({ hasText: 'NagpurMaharashtra' }).locator('small').click();
                    await page.getByRole('button', { name: 'Today' }).click();
                    await page.waitForTimeout(3000)

                    await page.getByText('Bus Partner').click();
                    await page.getByRole('textbox', { name: 'Search here' }).click();
                    await page.waitForTimeout(3000)

                    await page.getByRole('textbox', { name: 'Search here' }).fill('Prasanna - Purple Bus');
                    await page.waitForTimeout(3000)

                    await page.locator('#list-filter-option-container').getByRole('checkbox').check();
                    await page.waitForTimeout(1500)


                    const busCard = await page.locator('div#service-cards-container').innerHTML();
                    // console.log(busCard)
                    const text = convert(busCard, {
                        wordwrap: false, // optional: prevents line breaks
                        selectors: [
                        { selector: 'a', options: { hideLinkHrefIfSameAsText: true } }
                        ]
                    });

                    response[`${route.source}-${route.destination}`] = text;
                }catch(e){
                    console.log("Error in abhibus",e)
                    response[`${route.source}-${route.destination}`] = "no buses found";
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
            response[route.source+"-"+route.destination] = ""
            console.log("route",route)
            try{
                            const browser = await chromium.launch({ headless: false }); // Run headful to avoid detection
                            const context = await browser.newContext({
                            userAgent:
                                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
                            viewport: { width: 1280, height: 720 },
                            locale: 'en-US',
                            });
                        
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
                        
                            await page.goto('https://accounts.redbus.com/login?continue=https://www.redbus.pro/');
                            await page.getByRole('textbox', { name: 'Username' }).click();
                            await page.getByRole('textbox', { name: 'Username' }).fill('9748');
                            await page.getByRole('textbox', { name: 'Username' }).press('Tab');
                            await page.getByRole('textbox', { name: 'Password' }).click();
                            await page.getByRole('textbox', { name: 'Password' }).fill('prasannapurple');
                            await page.getByRole('button', { name: 'Login', exact: true }).click();
                        
                            await page.locator('role=button[name="Skip"]').click();
                        
                            await page.hover('aside.SideNav---sideNav---3QZiY ');
                        
                            await page.locator('role=link[name="R & R"]').click();
                            await page.waitForTimeout(5000);
                            // await page.click("#servicewise_tab")
                            await page.waitForTimeout(1000);
                            const inputSelector = 'input[placeholder="Source"]'; 
                            await page.waitForSelector(inputSelector);
                            await page.click(inputSelector);
                            await page.waitForTimeout(2000);
                            await page.fill(inputSelector, route.source);
                            await page.waitForTimeout(2000);
                            await page.locator('#react-autowhatever-1 #react-autowhatever-1--item-0').click();
                            await page.waitForTimeout(2000);
                        
                        
                            const inputSelector1 = 'input[placeholder="Destination"]'; 
                        
                            await page.waitForSelector(inputSelector1);
                            await page.click(inputSelector1);
                            await page.waitForTimeout(2000);
                            await page.fill(inputSelector1, route.destination);
                            await page.locator('#react-autowhatever-1 #react-autowhatever-1--item-0').click();
                            await page.waitForTimeout(2000);
                        
                        
                            const filterBtnSelector = 'button:has-text("Filter")';
                            await page.waitForSelector(filterBtnSelector, { state: 'visible' });
                            await page.click(filterBtnSelector);
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

                    response[`${route.source}-${route.destination}`] = text;
                }catch(e){
                    console.log("Error in abhibus",e)
                    response[`${route.source}-${route.destination}`] = "no buses found";
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


