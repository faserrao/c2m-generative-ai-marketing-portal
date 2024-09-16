"""
Lambda that prompts Pinpoint to send a message based on channel
"""

#########################
#   LIBRARIES & LOGGER
#########################

import requests
from print_response import print_response

check_tracking_url = "https://stage-rest.click2mail.com/molpro/jobs/"

# Define credentials
myusername = "stellario"
mypassword = "Babushka1!"

#########################
#        HANDLER
#########################


def c2m_check_tracking(tracking_type: str = "IMB", job_id: str = ""):

    headers = {"user-agent": "my-app/0.0.1"}
    tracking_type = tracking_type
    url = check_tracking_url + job_id + "/tracking?tracking_type=" + tracking_type

    try:
        response = requests.get(url, headers=headers, auth=(myusername, mypassword))
        response.raise_for_status()  # Raise an exception for HTTP errors
        if response.status_code == 200:
            print_response("Check tracking call successful", response)
            return {"statusCode": 200, "body": response.text, "headers": {"Content-Type": "application/json"}}
        print_response("Check tracking call failed", response)
        return {"statusCode": 400, "body": response.text, "headers": {"Content-Type": "application/json"}}
    except requests.exceptions.RequestException as e:
        exception_string = f"Check tracking http request failed: {e}, {str(e)}"
        print_response(exception_string)
        return {"statusCode": 400, "body": str(e), "headers": {"Content-Type": "application/json"}}
