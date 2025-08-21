const { chromium } = require('playwright');
const { DateTime } = require('luxon');
async function paytmTravelBusSearch() {
  const browser = await chromium.launch({ headless: false }); // set to true for headless
  const context = await browser.newContext();
  const page = await context.newPage();

  try {
    await page.goto('https://tickets.paytm.com/');
    await page.waitForTimeout(2000);

    await page.click('#Bus');
    await page.waitForTimeout(2000);

    // await page.click('#oneway');
    // await page.waitForTimeout(2000);

    const sourceInput = page.locator('#dwebSourceInput');
    await sourceInput.fill('Pune');
    await page.waitForTimeout(2000);
    await page.locator("(//div[@class='+2ajg'])[1]").click();

    const destinationInput = page.locator('#dwebDestinationInput');
    await destinationInput.fill('Chnadrapur');
    await page.waitForTimeout(2000);
    await page.locator("(//div[@class='+2ajg'])[1]").click();

    await page.waitForTimeout(2000);
    await page.locator("//div[@aria-label='Today']").click();

    await page.waitForTimeout(2000);
    await page.click("button:has-text('Search Buses')");
    await page.waitForTimeout(5000);

    await page.evaluate(() => window.scrollBy(0, 900));
    await page.waitForTimeout(2000);

    const viewMore = await page.$("//div[normalize-space()='View More(3)']");
    if (viewMore) await viewMore.click();
    await page.waitForTimeout(5000);
    await page
          .getByRole("textbox", { name: "Search Operators" })
          .fill("prasanna");
    const prasannaBus = await page.$("(//div[contains(text(),'Prasanna - Purple Bus')])[1]");
    if (prasannaBus) await prasannaBus.click();

    await page.waitForTimeout(5000);
    await page.evaluate(() => window.scrollBy(0, -1400));

    // Extract bus data
    await page.waitForSelector('div.IHKeM', { timeout: 20000 });
    const buses = await page.$$('div.IHKeM');

    console.log(`Total buses found: ${buses.length}`);

    for (let i = 0; i < buses.length; i++) {
      console.log('-------------------------------------');
      console.log(`Bus ${i + 1}`);

      const bus = buses[i];

      const rating = await bus.$eval('span.QJoiM', el => el.textContent).catch(() => 'NA');
      const departure = await bus.$eval('div.wYtCy div._4rWgi', el => el.textContent).catch(() => 'NA');
      const arrival = await bus.$eval('div.EjC2U div._4rWgi', el => el.textContent).catch(() => 'NA');
      const price = await bus.$eval('span.A2eT9', el => el.textContent).catch(() => 'NA');

      console.log(`Rating: ${rating}`);
      console.log(`Departure: ${normalizeTime(departure)}`);
      console.log(`Arrival: ${normalizeTime(arrival)}`);
      console.log(`Price: ${price}`);
    }

  } catch (err) {
    console.error('Error:', err);
  } finally {
    await browser.close();
  }
}

// Run the function
paytmTravelBusSearch();


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
    throw new Error(`Invalid time format: ${input}`);
  }
}
