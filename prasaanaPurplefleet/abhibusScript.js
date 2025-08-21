const { chromium } = require('playwright');
const { DateTime } = require('luxon');

async function abhiBusTravelFlow() {
  const browser = await chromium.launch({ headless: false }); // set headless: true for automation
  const context = await browser.newContext();
  const page = await context.newPage();

  try {
    // Step 1: Login to AbhiBus Travel (navigate)
    await page.goto('https://www.abhibus.com/');
    await page.waitForTimeout(5000);

    // Step 2: Click "Buses"
    await page.click("//div[contains(@class,'lob-actions col')]//span[contains(text(),'Buses')]");
    await page.waitForTimeout(2000);

    // Step 3: Enter source - Pune
    await page.fill("//input[@placeholder='Leaving From']", 'Pune');
    await page.waitForSelector("//div[contains(@class,'auto-complete-drop-down')]//div[contains(text(),'Pune')]");
    await page.click("//div[contains(@class,'auto-complete-drop-down')]//div[contains(text(),'Pune')]");
    await page.waitForTimeout(2000);

    // Step 4: Enter destination - Chandrapur
    await page.fill("//input[@placeholder='Going To']", 'Chandrapur');
    await page.waitForSelector("//div[contains(@class,'auto-complete-drop-down')]//div[contains(text(),'Chandrapur')]");
    await page.click("//div[contains(@class,'auto-complete-drop-down')]//div[contains(text(),'Chandrapur')]");
    await page.waitForTimeout(2000);

    // Step 5: Click Search
    await page.click("//span[normalize-space()='Search']");
    await page.waitForTimeout(10000);

    // Step 6: Apply Bus Partner Filter
    await page.click("//div[contains(text(),'Bus Partner')]");
    await page.waitForTimeout(2000);
    await page.fill("//input[@placeholder='Search here']", 'Prasanna');
    await page.waitForTimeout(2000);
    await page.click("//input[@type='checkbox']"); // Select the checkbox

    // Step 7: Extract Bus Data
    const buses = await page.$$("div[id^='service-card-body-']");
    console.log(`Total buses found: ${buses.length}`);

    let count = 1;
    for (const bus of buses) {
      console.log('-------------------------------------');
      console.log(`Bus ${count}`);

      const getText = async (selector) => {
        try {
          const el = await bus.$(selector);
          return el ? await el.textContent() : 'NA';
        } catch { return 'NA'; }
      };

      const busType = await getText("*[id*='service-operator-agent-name-'] > div");
      const departure = await getText("#travel-distance-source-info div div span");
      const arrival = await getText("#travel-distance-destination-info div div span");
      const price = await getText("*[id*='service-operator-fare-info-'] div div:nth-child(1) div:nth-child(2) span:nth-child(2)");
      const rating = await getText("*[id*='rating-card-container'] > div span");

      console.log(`Bus Type: ${busType}`);
      console.log(`Departure: ${normalizeTime(departure)}`);
      console.log(`Arrival: ${normalizeTime(arrival)}`);
      console.log(`Price: ${price}`);
      console.log(`Rating: ${rating}`);

      count++;
    }

  } catch (err) {
    console.error('❌ Error:', err);
  } finally {
    await browser.close();
  }
}

// Run the function
abhiBusTravelFlow();


function normalizeTime(input) {
      input = input.trim().toLowerCase()
    .replace(/\.|–|—/g, ':')      // Replace dots and other separators with colon
    .replace(/\s+/g, ' ')         // Normalize spaces
    .replace(/\s*([ap]m)/, ' $1') // Ensure space before am/pm
  let dt;

  // Try parsing as 12-hour format with AM/PM
  if (input.toLowerCase().includes('am') || input.toLowerCase().includes('pm')) {
    dt = DateTime.fromFormat(input.trim(), 'hh:mm a');
  } else {
    // Try parsing as 24-hour format
    dt = DateTime.fromFormat(input.trim(), 'HH:mm');
  }

  // Return in 24-hour format (HH:mm) or throw if invalid
  if (dt.isValid) {
    return dt.toFormat('HH:mm');
  } else {
    return input;
  }
}