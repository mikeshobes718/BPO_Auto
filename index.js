const { google } = require('googleapis');
const AWS = require('aws-sdk');
const crypto = require('crypto');

// Configure AWS
AWS.config.update({ region: 'us-east-1' });
const s3 = new AWS.S3();

// Function to get Google service account credentials from S3
async function getGoogleCredentials() {
    const params = {
        Bucket: 'unitedrealestatebpos',
        Key: 'credentials/nimble-park-404921-5a21a0691571.json'
    };

    // Retrieve the credentials file from S3
    const data = await s3.getObject(params).promise();
    return JSON.parse(data.Body.toString());
}

// Function to authenticate with Google Sheets using the retrieved credentials
async function authenticateGoogleSheets(credentials) {
    const auth = new google.auth.GoogleAuth({
        credentials: credentials,
        scopes: ['https://www.googleapis.com/auth/spreadsheets.readonly'],
    });

    const client = await auth.getClient();
    google.options({ auth: client });
}

// Handler function for AWS Lambda
exports.handler = async (event) => {
    // Log the incoming event to debug
    console.log('Received event:', JSON.stringify(event, null, 2));

    // Extract the 'To' field from the JSON data if present
    const emailTo = (event.To || 'No To field').toLowerCase(); // Convert email to lowercase
    console.log(`Email to: ${emailTo}`);

    // Authenticate and search for the email in Google Sheets
    try {
        const credentials = await getGoogleCredentials();
        await authenticateGoogleSheets(credentials);

        const sheets = google.sheets({ version: 'v4' });
        const range = 'Sheet1';

        const response = await sheets.spreadsheets.values.get({
            spreadsheetId: '1Eko1zD65X0XntfyTYFYmX6vQGEFjWu_3UvszKRoNSPE',
            range: range,
        });

        const rows = response.data.values;
        const emailColumnIndex = rows[0].indexOf('EMAIL');
        if (emailColumnIndex !== -1) {
            const foundRowIndex = rows.findIndex(row => row[emailColumnIndex].toLowerCase() === emailTo);
            if (foundRowIndex !== -1) {
                const foundRow = rows[foundRowIndex].reduce((obj, val, index) => {
                    obj[rows[0][index]] = val;
                    return obj;
                }, {});
                console.log(JSON.stringify(foundRow, null, 4));

                // Generate a unique filename for the JSON file using crypto
                const filename = `emails/${crypto.randomUUID()}.json`;

                // Put the object in S3
                await s3.putObject({
                    Bucket: 'unitedrealestatebpos',
                    Key: filename,
                    Body: JSON.stringify(foundRow, null, 4)
                }).promise();

                return {
                    statusCode: 200,
                    body: JSON.stringify({
                        message: 'JSON stored successfully!',
                        row: foundRow
                    }, null, 4)
                };
            } else {
                console.log('Email not found in the sheet.');
                return {
                    statusCode: 404,
                    body: JSON.stringify({
                        message: 'Email not found in the sheet.'
                    }, null, 4)
                };
            }
        } else {
            console.log('EMAIL column not found in the sheet.');
            return {
                statusCode: 404,
                body: JSON.stringify({
                    message: 'EMAIL column not found in the sheet.'
                }, null, 4)
            };
        }
    } catch (error) {
        console.error('Error:', error);
        return {
            statusCode: 500,
            body: JSON.stringify({
                message: 'An error occurred.',
                error: error.message
            }, null, 4)
        };
    }
};
