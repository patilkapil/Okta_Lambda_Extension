# Example Extension in Python
The provided code sample demonstrates how to sewtup a basic Okta extension written in Python 3  
This is an example for the demonstration purposes, and this code has not been tested in a production environment.
> Note: This extension is inspired from https://github.com/aws-samples/aws-lambda-extensions/tree/main/python-example-extension


## Layer Setup Process
The extensions .zip file should contain a root directory called `extensions/`, where the extension executables are located and another root directory called `python-example-extension/`, where the core logic of the extension  and its dependencies are located.

Creating zip package for the extension:
```bash
$ chmod +x extensions/python-example-extension
$ zip -r extension.zip .
```

Ensure that you have aws-cli v2 for the commands below.
Publish a new layer using the `extension.zip`. The output of the following command should provide you a layer arn.
```bash
aws lambda publish-layer-version \
 --layer-name "python-example-extension" \
 --region <use your region> \
 --zip-file  "fileb://extension.zip"
```
Note the LayerVersionArn that is produced in the output.
eg. `"LayerVersionArn": "arn:aws:lambda:<region>:123456789012:layer:<layerName>:1"`

Add the newly created layer version to a Python 3.8 runtime Lambda function.


## Function Invocation and Extension Details
Extension reads clientID,clientSecret and Oauthtoken URL.Make sure you have 3 environment variables in the Lambda environment. 
client_id 
client_secret	 
okta_token_url

Extension reads environment values and creates a token .json file in a /tmp location
Lambda code can read the json file & access token for any further downstream applications 

## Architecture Diagram 

![image](https://user-images.githubusercontent.com/2838125/161128097-4dcc4b99-e5fc-4f66-be1f-9ed72869ddf4.png)


## Assumptions: 
* Lambda function is dependent on a backend API to complete the operation
* Lambda function can rely on the Lambda Extension to hand over an access token

## Step by step flow
* Step 1: The client sends a request to a lambda function
* Step 2: Lambda extension reads configuration parameters from a lambda function.
* Step 3: Lambda extensions interact with OAuth server to generate access token
* Step 4: Lambda extensions genertes access token and stores them into a temp storage 
* Step 5: The lambda function will use access tokens from a temp storage location
* Step 6: Retrieved access tokens are sent to the resource provider with the appropriate header format to get the desired data
