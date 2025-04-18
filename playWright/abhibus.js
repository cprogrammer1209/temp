const { chromium } = require('playwright');
const { convert } = require('html-to-text');


async function searchBuses(source, destination, operator = null) {
  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext();
  const page = await context.newPage();

  await page.goto('https://www.abhibus.com/');
  await page.getByRole('textbox', { name: 'From Station' }).click();
  await page.getByRole('textbox', { name: 'From Station' }).fill('PUne');
  await page.getByText('Pune', { exact: true }).click();
  await page.getByRole('textbox', { name: 'To Station' }).click();
  await page.getByRole('textbox', { name: 'To Station' }).fill('Nagpur');
  await page.getByRole('listitem').filter({ hasText: 'NagpurMaharashtra' }).locator('small').click();
  await page.getByRole('button', { name: 'Today' }).click();
  await page.getByText('Bus Partner').click();
  await page.getByRole('textbox', { name: 'Search here' }).click();
  await page.getByRole('textbox', { name: 'Search here' }).fill('pra');
  await page.locator('#list-filter-option-container').getByRole('checkbox').check();

  const busCard = await page.locator('div#service-cards-container').innerHTML();
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
    // { source: 'Mumbai', destination: 'Goa' }
  ];
  
  (async () => {
    for (const route of routes) {
      await searchBuses(route.source, route.destination, route.operator);
    }
  })();
  