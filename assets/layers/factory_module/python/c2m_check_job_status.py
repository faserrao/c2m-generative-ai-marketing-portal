"""Lambda that prompts Pinpoint to send a message based on channel."""

#########################
#   LIBRARIES & LOGGER
#########################


import requests
from print_response import print_response

CONTENT_TYPE_JSON = "application/json"

CHECK_JOB_STATUS_URL = "https://stage-rest.click2mail.com/molpro/jobs/"

# Define credentials
USERNAME = "stellario"
PASSWORD = "Babushka1!"

#########################
#        HANDLER
#########################


def c2m_check_job_status(job_id: str = None):
    """Check the status of a Click2Mail job."""
    url = CHECK_JOB_STATUS_URL + job_id
    headers = {"user-agent": "my-app/0.0.1"}

    try:
        response = requests.get(url, headers=headers, auth=(USERNAME, PASSWORD))
        response.raise_for_status()  # Raise an exception for HTTP errors
        if response.status_code == 201:
            print_response("Check job status call successful", response)
            return {"statusCode": 200, "body": response.text, "headers": {"Content-Type": CONTENT_TYPE_JSON}}
        print_response("Add credit call failed", response)
        return {"statusCode": 400, "body": response.text, "headers": {"Content-Type": CONTENT_TYPE_JSON}}
    except requests.exceptions.RequestException as e:
        exception_string = f"Add credit http request failed: {e}, {str(e)}"
        print_response(exception_string)
        return {"statusCode": 400, "body": str(e), "headers": {"Content-Type": CONTENT_TYPE_JSON}}
