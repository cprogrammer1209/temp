const { chromium } = require('playwright');
const { convert } = require('html-to-text');
const fs = require('fs/promises');
const path = require('path');


// const [source, destination,timestamp] = process.argv.slice(2); // like: "Pune" "Mumbai"
console.log(`Source: ${source}, Destination: ${destination}, TIme Stamp: ${timestamp}`);
(async () => {
  const browser = await chromium.launch(
    { headless: false ,
    args: ['--window-size=1280,800', '--window-position=100,100']
    }
  );
  const context = await browser.newContext();
  const page = await context.newPage();

  await page.goto('https://tickets.paytm.com/bus/');
  await page.getByRole('textbox', { name: 'From' }).click();
  await page.getByRole('textbox', { name: 'From' }).fill(source);
  // await page.getByText('PuneMaharashtra', { exact: true }).click();
  await page.waitForSelector('#source-section .dcrjM');
  await page.click('#source-section .dcrjM >> nth=0');
  await page.getByRole('textbox', { name: 'To' }).click();
  await page.getByRole('textbox', { name: 'To' }).fill(destination);
  await page.waitForTimeout(1000)


  await page.waitForSelector('#destination-section .dcrjM');
  await page.click('#destination-section .dcrjM >> nth=0');

  // await page.getByText('NagpurMaharashtra', { exact: true }).click();
  await page.getByRole('button', { name: 'Search Buses' }).click();
  await page.waitForTimeout(5000)
  await page.getByRole('textbox', { name: 'Search Operators' }).click();
  await page.getByRole('textbox', { name: 'Search Operators' }).fill('pras');
  await page.locator('div').filter({ hasText: /^Bus operatorsPrasanna - Purple Bus$/ }).getByLabel('unchecked').click();


  let count = 0;
  while (count < 3) {
    count++
    await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));      
    await page.waitForTimeout(1000);      
  }
  const busCard = await page.locator('div.-iAp6').innerHTML();
  // console.log(busCard)
  const text = convert(busCard, {
    wordwrap: false, // optional: prevents line breaks
    selectors: [
      { selector: 'a', options: { hideLinkHrefIfSameAsText: true } }
    ]
  });
  await fs.writeFile(path.join(__dirname, 'extracted', `paytm_${timestamp}.txt`), text);

  console.log(text);

  await browser.close();
})();

