#!/bin/bash

# Replace with your actual Lambda function name
FUNCTION_NAME=add your function name here

# Navigate to the directory containing your Lambda function
cd /Users/mike/Documents/Development/BPOs

# Zip the function and dependencies
echo "Zipping the function and dependencies..."
zip -r function.zip lambda_function.js node_modules

# Upload the zip to AWS Lambda
echo "Uploading the function to AWS Lambda..."
/usr/local/bin/aws lambda update-function-code --function-name $FUNCTION_NAME --zip-file fileb://function.zip

echo "Deployment complete."
