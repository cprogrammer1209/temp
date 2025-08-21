const { chromium } = require('playwright');
const { convert } = require('html-to-text');


const [source, destination,timestamp] = process.argv.slice(2); // like: "Pune" "Mumbai"
console.log(`Source: ${source}, Destination: ${destination}, TIme Stamp: ${timestamp}`);
(async () => {
  const route = {
      source: "Pune",
      destination: "Nagpur",
      timestamp: timestamp
  }

  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext();
  const page = await context.newPage();

  await page.goto('https://www.abhibus.com/');
  await page.getByRole('textbox', { name: 'Leaving From' }).click();
  await page.getByRole('textbox', { name: 'Leaving From' }).fill(route.source);
  await page.waitForTimeout(5000)
      await page.waitForSelector('div.auto-complete-drop-down .auto-complete-list');
  await page.click('.auto-complete-list .auto-complete-list-item >> nth=0');
  //   await page.getByText('Pune', { exact: true }).click();
  await page.getByRole('textbox', { name: 'Going To' }).click();
  await page.getByRole('textbox', { name: 'Going To' }).fill(route.destination);
  await page.waitForTimeout(5000)
      await page.waitForSelector('div.auto-complete-drop-down .auto-complete-list');
  await page.click('.auto-complete-list .auto-complete-list-item >> nth=0');
  //   await page.getByRole('listitem').filter({ hasText: 'NagpurMaharashtra' }).locator('small').click();
//   await page.getByRole('textbox', { name: 'Today' }).click();
await page.click('text=Today');

  await page.waitForTimeout(3000)

  await page.getByText('Bus Partner').click();
  await page.getByRole('textbox', { name: 'Search here' }).click();
  await page.waitForTimeout(3000)

  await page.getByRole('textbox', { name: 'Search here' }).fill('Prasanna - Purple Bus');
  await page.waitForTimeout(3000)

  await page.locator('#list-filter-option-container').getByRole('checkbox').check();
  await page.waitForTimeout(1500)

  let count = 0;
  while (count < 3) {
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

  console.log(text);
})();