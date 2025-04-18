const { chromium } = require('playwright');


async function delayedClick(locator,page, delay = 1000) {
  await page.waitForTimeout(delay);
  await locator.click();
}

async function searchBuses(source, destination, operator = null) {
  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext();
  const page = await context.newPage();
  await page.goto('https://www.redbus.in/');
  await page.getByRole('textbox', { name: 'From' }).click();
  await page.getByRole('textbox', { name: 'From' }).fill('nagpur');
  await page.waitForSelector('ul.sc-dnqmqq');

   await page.$$eval('ul.sc-dnqmqq li .placeHolderMainText', elements =>
    elements.map(el => el.textContent.trim())
  );
  await page.getByRole('textbox', { name: 'To' }).click();
  await page.getByRole('textbox', { name: 'To' }).fill('Pune');
  await page.waitForSelector('ul.sc-dnqmqq');

  await page.$$eval('ul.sc-dnqmqq li .placeHolderMainText', elements =>
    elements.map(el => el.textContent.trim())
  );
  await page.getByRole('button', { name: ' Date' }).click();

const today = new Date().getDate().toString();



// // Find and click the span element that matches today's date
await page.$$eval('.DayTiles__CalendarDaysSpan-sc-1xum02u-1', (elements, today) => {
  const el = elements.find(e => e.textContent.trim() === today);
  if (el) el.click();
}, today);



await page.locator(".sc-cvbbAY.gDXYez").click();
await page.waitForLoadState('load');
await page.getByRole('textbox', { name: 'OPERATOR' }).click();
await page.locator('input[name="inpFilter"]').click();
await page.click('li[data-value="Prasanna - Purple Bus"] input[type="checkbox"]');



  
await page.getByText('APPLY', { exact: true }).click();


  // const busCard = await page.locator('div.result-sec').innerHTML();
  //   // console.log(busCard)
  //   const text = convert(busCard, {
  //     wordwrap: false, // optional: prevents line breaks
  //     selectors: [
  //       { selector: 'a', options: { hideLinkHrefIfSameAsText: true } }
  //     ]
  //   });
  //   console.log(text);


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
  