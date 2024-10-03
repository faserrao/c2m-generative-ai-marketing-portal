"""Lambda that prompts Pinpoint to send a message based on channel."""

#########################
#   LIBRARIES & LOGGER
#########################


import requests
from print_response import print_response

CONTENT_TYPE_JSON = "application/json"

SUBMIT_JOB_URL = "https://stage-rest.click2mail.com/molpro/jobs/"

# Define credentials
USERNAME = "stellario"
PASSWORD = "Babushka1!"

#########################
#        HANDLER
#########################


def c2m_submit_job(billing_type: str = "User Credit", job_id: str = "") -> dict:
    """Submit a job to Click2Mail.

    Args:
        billing_type (str): Type of billing. Defaults to "User Credit".
        job_id (str): ID of the job to submit.

    Returns:
        dict: Response containing status code, body, and headers.
    """
    url = SUBMIT_JOB_URL + job_id + "/submit"
    headers = {"user-agent": "my-app/0.0.1"}
    values = {"billingType": billing_type}

    try:
        # Make POST request to submit the job
        response = requests.post(url, data=values, headers=headers, auth=(USERNAME, PASSWORD))
        # Raise an exception if request fails
        response.raise_for_status()
        if response.status_code == 200:
            # Return success response
            print_response("Submit job successful", response)
            return {"statusCode": 200, "body": response.text, "headers": {"Content-Type": CONTENT_TYPE_JSON}}
        else:
            # Return failure response
            print_response("Submit job failed:", response)
            return {"statusCode": 400, "body": response.text, "headers": {"Content-Type": CONTENT_TYPE_JSON}}
    except requests.exceptions.RequestException as e:
        # Handle any exceptions that occur
        exception_string = f"Submit job http request failed:: {e}, {str(e)}"
        print_response(exception_string)
        return {"statusCode": 400, "body": str(e), "headers": {"Content-Type": CONTENT_TYPE_JSON}}
