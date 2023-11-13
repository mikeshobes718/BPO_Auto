const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch({
    headless: false, // Running the browser in non-headless mode so you can see what's happening
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  try {
    const page = await browser.newPage();

    // Go to the specified URL
    await page.goto('https://valuationops.homegenius.com', { waitUntil: 'networkidle0' });
    console.log('Page loaded.');

    // Optionally, wait a moment to observe the loaded page
    // await page.waitForTimeout(5000); // Wait for 5 seconds

    // Click the login button using its ID
    await page.click('#signIn');
    console.log('Login button clicked.');

    // Wait for the email input field to be available
    await page.waitForSelector('#sso-signin-email-input', { visible: true });

    // Enter demonstration credentials
    const demoEmail = 'bpo@unitedinvestmentsfirm.com';
    const demoPassword = 'Americ@2023';
    await page.type('#sso-signin-email-input', demoEmail);
    await page.waitForSelector('#sso-signin-password-input', { visible: true });
    await page.type('#sso-signin-password-input', demoPassword);

    // Retrieve all open pages (tabs)
    const pages = await browser.pages();
    // Close the first tab if there is more than one tab
    if (pages.length > 1) {
      await pages[0].close();
      console.log('First tab closed.');
    }

    // Click the login button
    await page.waitForSelector('#btnLogin', { visible: true });
    await page.click('#btnLogin');
    console.log('Submit button clicked.');

    // Continue with the rest of your script on the current page or open new pages as needed

  } catch (error) {
    console.error('Error running puppeteer script:', error);
  } finally {
    // Uncomment the line below if you want the browser to close regardless of errors
    // await browser.close();
  }
})();
