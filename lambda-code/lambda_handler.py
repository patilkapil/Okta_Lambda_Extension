import json
import os
import base64


# 3import pandas as pd

def lambda_handler(event, context):
    print('read the temp okta json file')

    with open('/tmp/okta-token.json', 'rb') as fp:
        print(fp.read())
    # print(my_file.read().decode())
    return {
        'statusCode': 200,
        # 'body': json.dumps('Hello from Pandas, max value is  ' + str(series.max()) )
        'body': json.dumps('Hello from Pandas, max value is')
    }