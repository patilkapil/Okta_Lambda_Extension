# Example Extension in Python
The provided code sample demonstrates how to sewtup a basic Okta extension written in Python 3  

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