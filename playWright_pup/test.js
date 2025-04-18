const puppeteer = require('puppeteer-extra');
const StealthPlugin = require('puppeteer-extra-plugin-stealth');

puppeteer.use(StealthPlugin());

(async () => {
  const browser = await puppeteer.launch({
    headless: false,
    slowMo: 100,
    defaultViewport: null,
    args: ['--start-maximized']
  });

  const page = await browser.newPage();

  await page.goto('https://accounts.redbus.com/login?continue=https://www.redbus.pro/');

  console.log('>> Chrome launched with stealth.');
  console.log('>> Press F12 to open DevTools, go to Recorder tab, click "Start recording".');

  // Keep it open until you close the browser
})();
