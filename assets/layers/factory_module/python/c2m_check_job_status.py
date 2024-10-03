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
    """Check the status of a Click2Mail job.

    Args:
        job_id (str): ID of the job to check. Defaults to None.

    Returns:
        dict: Response containing status code, body, and headers.
    """
    url = CHECK_JOB_STATUS_URL + job_id
    headers = {"user-agent": "my-app/0.0.1"}

    try:
        # Make a GET request to the Click2Mail API
        response = requests.get(url, headers=headers, auth=(USERNAME, PASSWORD))
        # Raise an exception if the request fails
        response.raise_for_status()
        # If the request is successful, return a 200 status code, the response body, and the JSON content type
        if response.status_code == 201:
            print_response("Check job status call successful", response)
            return {"statusCode": 200, "body": response.text, "headers": {"Content-Type": CONTENT_TYPE_JSON}}
        # If the request fails, return a 400 status code, the response body, and the JSON content type
        print_response("Check job status call failed", response)
        return {"statusCode": 400, "body": response.text, "headers": {"Content-Type": CONTENT_TYPE_JSON}}
    except requests.exceptions.RequestException as e:
        # If there is an exception, return a 400 status code, the exception string, and the JSON content type
        exception_string = f"Check job status http request failed: {e}, {str(e)}"
        print_response(exception_string)
        return {"statusCode": 400, "body": str(e), "headers": {"Content-Type": CONTENT_TYPE_JSON}}
