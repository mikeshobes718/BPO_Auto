const chromium = require('chrome-aws-lambda');
const puppeteer = require('puppeteer-core');

exports.handler = async (event, context) => {
  let result = null;
  let browser = null;

  try {
    // Set up Puppeteer
    browser = await puppeteer.launch({
      args: chromium.args,
      defaultViewport: chromium.defaultViewport,
      executablePath: await chromium.executablePath,
      headless: chromium.headless,
      ignoreHTTPSErrors: true,
    });

    // Create a new page
    let page = await browser.newPage();

    // Go to the specified URL
    await page.goto('https://valuationops.homegenius.com', { waitUntil: 'networkidle0' });

    // Click the login button using its ID
    await page.click('#signIn');

    // Wait for the email input field to be available
    await page.waitForSelector('#sso-signin-email-input', { visible: true });

    // Enter username and password
    await page.type('#sso-signin-email-input', 'bpo@unitedinvestmentsfirm.com');
    await page.waitForSelector('#sso-signin-password-input', { visible: true });
    await page.type('#sso-signin-password-input', 'Americ@2023');

    // Click the login button
    await page.waitForSelector('#btnLogin', { visible: true });
    await page.click('#btnLogin');

    // Wait for navigation after logging in
    await page.waitForNavigation({ waitUntil: 'networkidle0' });

    // Open a new page (tab) for the Google Sheets document
    const newPage = await browser.newPage();

    // Navigate to the Google Sheets URL in the new tab
    await newPage.goto('https://docs.google.com/spreadsheets/d/e/2PACX-1vQqgrIDmnVC0yCvOz9UaG6siqX5iwc3TKK8ADvojjhDeU98k5QbyLD-PgT5n7xA7pvAc968bT_BcMnm/pubhtml', { waitUntil: 'networkidle0' });

    // Wait for the cell with the specific class to be rendered in the new tab
    await newPage.waitForSelector('td.s1', { visible: true });

    // Get the text content of the cell in the new tab
    const value = await newPage.evaluate(() => {
      const cell = document.querySelector('td.s1[dir="ltr"]');
      return cell ? cell.innerText.trim() : null;
    });

    if (value) {
      console.log('Value retrieved:', value);
    } else {
      console.log('Value not found or cell not rendered properly.');
    }

    // Close the Google Sheets tab as we no longer need it
    await newPage.close();

    // Switch back to the original tab
    await page.bringToFront();

    // Enter the retrieved value into the input field on the original tab
    await page.waitForSelector('#sso-verification-code-input', { visible: true });
    await page.type('#sso-verification-code-input', value);

    // Continue with any other actions you need to perform

    result = { statusCode: 200, body: 'Automations script completed successfully.' };
  } catch (error) {
    console.error('An error occurred during the automation:', error);
    result = {
      statusCode: 500,
      body: JSON.stringify({ error: error.message }),
    };
  } finally {
    // Clean up: close the browser
    if (browser !== null) {
      await browser.close();
    }
  }

  return result;
};
