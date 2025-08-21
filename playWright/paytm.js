const { chromium } = require('playwright');
const { convert } = require('html-to-text');


async function searchBuses(source, destination, operator = null) {
  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext();
  const page = await context.newPage();

  await page.goto('https://tickets.paytm.com/bus/');
  await page.getByRole('textbox', { name: 'From' }).click();
  await page.getByRole('textbox', { name: 'From' }).fill('pune');
  
  await page.waitForSelector('#source-section .dcrjM');
await page.click('#source-section .dcrjM >> nth=0');
  await page.getByRole('textbox', { name: 'To' }).click();
  await page.getByRole('textbox', { name: 'To' }).fill('nagpur');
  await page.getByText('NagpurMaharashtra', { exact: true }).click();
  await page.getByRole('button', { name: 'Search Buses' }).click();
  await page.getByRole('textbox', { name: 'Search Operators' }).click();
  await page.getByRole('textbox', { name: 'Search Operators' }).fill('pras');
  await page.locator('div').filter({ hasText: /^Bus operatorsPrasanna - Purple Bus$/ }).getByLabel('unchecked').click();

  const busCard = await page.locator('div.-iAp6').innerHTML();
  // console.log(busCard)
  const text = convert(busCard, {
    wordwrap: false, // optional: prevents line breaks
    selectors: [
      { selector: 'a', options: { hideLinkHrefIfSameAsText: true } }
    ]
  });
  console.log(text);

  await browser.close();
}


const routes = [
    { source: 'Pune', destination: 'Goa', operator: 'Prasanna - Purple Bus' },
    { source: 'Mumbai', destination: 'Goa' }
  ];
  
  (async () => {
    for (const route of routes) {
      await searchBuses(route.source, route.destination, route.operator);
    }
  })();
  