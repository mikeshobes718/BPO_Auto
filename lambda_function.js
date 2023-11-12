const AWS = require('aws-sdk');
const { google } = require('googleapis');
const s3 = new AWS.S3();

// Initialize the Google Sheets API
const sheets = google.sheets({ version: 'v4' });

// Function to get Google service account credentials from S3
async function getGoogleCredentials() {
    const params = {
        Bucket: 'unitedrealestatebpos', // Replace with your S3 bucket name
        Key: 'credentials/nimble-park-404921-5a21a0691571.json' // Replace with the full path to your JSON file in the bucket
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

// Main Lambda function
exports.handler = async (event) => {
    try {
        // Load Google credentials from S3
        const credentials = await getGoogleCredentials();
        await authenticateGoogleSheets(credentials);

        // Specify the Google Sheet ID and the range you want to read from
        const spreadsheetId = '1Eko1zD65X0XntfyTYFYmX6vQGEFjWu_3UvszKRoNSPE'; // The provided Google Sheet ID
        const range = 'Sheet1!A2:C2'; // Accesses the first row of data in 'Sheet1'

        // Read data from the specified range in the Google Sheet
        const response = await sheets.spreadsheets.values.get({
            spreadsheetId,
            range,
        });

        const firstRowData = response.data.values;

        // Construct the response body with the retrieved data
        const responseBody = {
            message: 'First row data from Google Sheet retrieved successfully',
            firstRowData: firstRowData // Include the first row data from Google Sheet in the response
        };

        // Return a successful response containing the first row data
        return {
            statusCode: 200,
            body: JSON.stringify(responseBody, null, 2)
        };
    } catch (err) {
        console.error("Error:", err);
        // Return an error response
        return {
            statusCode: 500,
            body: JSON.stringify({
                error: 'Error retrieving data',
                details: err.message
            }, null, 2)
        };
    }
};
