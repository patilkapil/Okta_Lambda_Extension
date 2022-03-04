#!/usr/bin/env python3
# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

import json
import os
import requests
import signal
import sys
from pathlib import Path
import base64



# global variables
# extension name has to match the file's parent directory name)
LAMBDA_EXTENSION_NAME = Path(__file__).parent.name


# custom extension code
def execute_custom_processing(event):
    # perform custom per-event processing here
    print('custom processing')

    print(f"[{LAMBDA_EXTENSION_NAME}] Received event: {json.dumps(event)}", flush=True)



# boiler plate code
def handle_signal(signal, frame):
    # if needed pass this signal down to child processes
    print(f"[{LAMBDA_EXTENSION_NAME}] Received signal={signal}. Exiting.", flush=True)
    sys.exit(0)


def create_token():
    client_id = os.environ['client_id']
    client_secret = os.environ['client_secret']
    oauth_url = os.environ['okta_token_url']
    encodedData = base64.b64encode(bytes(f"{client_id}:{client_secret}", "ISO-8859-1")).decode("ascii")
    headers = {
        'Accept': '*/*',
        'Authorization': 'Basic ' + encodedData,
        'Cache-Control': 'no-cache',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    data = {
        'grant_type': 'client_credentials'
    }

    cookies = {
        'JSESSIONID': 'C4178E6BB95095E2E6652D69CC3B716A',
    }

    # Make a request to an Okta APi endpoint
    response = requests.post(oauth_url, headers=headers, cookies=cookies, data=data)
    response.raise_for_status()
    print("Creating Okta token file")
    data = response.json()
    with open('/tmp/okta-token.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print('JWT token')
    print(data)
    print('Token Compleye')


def register_extension():
    print(f"[{LAMBDA_EXTENSION_NAME}] Registering...", flush=True)
    headers = {
        'Lambda-Extension-Name': LAMBDA_EXTENSION_NAME,
    }
    payload = {
        'events': [
            'INVOKE',
            'SHUTDOWN'
        ],
    }
    response = requests.post(
        url=f"http://{os.environ['AWS_LAMBDA_RUNTIME_API']}/2020-01-01/extension/register",
        json=payload,
        headers=headers
    )
    print(response)
    ext_id = response.headers['Lambda-Extension-Identifier']

    print(f"[{LAMBDA_EXTENSION_NAME}] Registered with ID: {ext_id}", flush=True)
    create_token()
    return ext_id


def process_events(ext_id):
    headers = {
        'Lambda-Extension-Identifier': ext_id
    }
    while True:
        print(f"[{LAMBDA_EXTENSION_NAME}] Waiting for event...", flush=True)
        response = requests.get(
            url=f"http://{os.environ['AWS_LAMBDA_RUNTIME_API']}/2020-01-01/extension/event/next",
            headers=headers,
            timeout=None
        )
        event = json.loads(response.text)

        if event['eventType'] == 'SHUTDOWN':
            print(f"[{LAMBDA_EXTENSION_NAME}] Received SHUTDOWN event. Exiting.", flush=True)
            sys.exit(0)
        else:
            execute_custom_processing(event)
            print('execute custom process ')


def main():
    # handle signals
    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)

    # execute extensions logic
    extension_id = register_extension()

    process_events(extension_id)


if __name__ == "__main__":
    main()
