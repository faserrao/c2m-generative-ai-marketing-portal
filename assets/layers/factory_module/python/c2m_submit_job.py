"""
Lambda that prompts Pinpoint to send a message based on channel
"""

#########################
#   LIBRARIES & LOGGER
#########################


import requests
from print_response import print_response

submit_job_url = "https://stage-rest.click2mail.com/molpro/jobs/"

# Define credentials
myusername = "stellario"
mypassword = "Babushka1!"

#########################
#        HANDLER
#########################


def c2m_submit_job(billing_type: str = "User Credit", job_id: str = ""):

    url = submit_job_url + job_id + "/submit"
    headers = {"user-agent": "my-app/0.0.1"}
    values = {"billingType": billing_type}

    try:
        response = requests.post(url, data=values, headers=headers, auth=(myusername, mypassword))
        response.raise_for_status()  # Raise an exception for HTTP errors
        print_response("Submit job successful", response)
        if response.status_code == 200:
            return {"statusCode": 200, "body": response.text, "headers": {"Content-Type": "application/json"}}
        print_response("Submit job failed:", response)
        return {"statusCode": 400, "body": response.text, "headers": {"Content-Type": "application/json"}}
    except requests.exceptions.RequestException as e:
        exception_string = f"Submit job http request failed:: {e}, {str(e)}"
        print_response(exception_string)
        return {"statusCode": 400, "body": str(e), "headers": {"Content-Type": "application/json"}}
