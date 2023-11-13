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

        // Log the name of the file that triggered the Lambda function
        const bucketName = event.Records[0].s3.bucket.name;
        const fileKey = event.Records[0].s3.object.key;
        console.log("Triggered by the file: " + fileKey);

        // Retrieve the actual data from the S3 object that triggered the Lambda function
        const s3Params = {
            Bucket: bucketName,
            Key: fileKey
        };
        const s3Data = await s3.getObject(s3Params).promise();
        const fileDataString = s3Data.Body.toString('utf-8');
        const fileData = JSON.parse(fileDataString); // Parse the JSON string into an object

        // Extract the From and To values
        const fromValue = fileData.From || 'Not available';
        const toValue = fileData.To || 'Not available';
        console.log("From:", fromValue);
        console.log("To:", toValue);

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
            message: 'First row data from Google Sheet and S3 file data retrieved successfully',
            firstRowData: firstRowData, // Include the first row data from Google Sheet in the response
            from: fromValue, // The "From" value extracted from fileData
            to: toValue // The "To" value extracted from fileData
        };

        // Return a successful response containing only the 'from' and 'to' values
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
