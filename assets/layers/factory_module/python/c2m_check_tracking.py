"""Lambda that prompts Pinpoint to send a message based on channel."""

#########################
#   LIBRARIES & LOGGER
#########################

import requests
from print_response import print_response

CONTENT_TYPE_JSON = "application/json"

CHECK_TRACKING_URL = "https://stage-rest.click2mail.com/molpro/jobs/"

# Define credentials
MY_USERNAME = "stellario"
MY_PASSWORD = "Babushka1!"

#########################
#        HANDLER
#########################


def c2m_check_tracking(tracking_type: str = "IMB", job_id: str = ""):
    """Check tracking information for a given job.

    Args:
        tracking_type (str): Type of tracking. Defaults to "IMB".
        job_id (str): ID of the job to check. Defaults to "".

    Returns:
        dict: Response containing status code, body, and headers.
    """

    headers = {"user-agent": "my-app/0.0.1"}
    url = CHECK_TRACKING_URL + job_id + "/tracking?tracking_type=" + tracking_type

    try:
        response = requests.get(url, headers=headers, auth=(MY_USERNAME, MY_PASSWORD))
        response.raise_for_status()  # Raise an exception for HTTP errors
        if response.status_code == 200:
            print_response("Check tracking call successful", response)
            return {"statusCode": 200, "body": response.text, "headers": {"Content-Type": CONTENT_TYPE_JSON}}
        print_response("Check tracking call failed", response)
        return {"statusCode": 400, "body": response.text, "headers": {"Content-Type": CONTENT_TYPE_JSON}}
    except requests.exceptions.RequestException as e:
        exception_string = f"Check tracking http request failed: {e}, {str(e)}"
        print_response(exception_string)
        return {"statusCode": 400, "body": str(e), "headers": {"Content-Type": CONTENT_TYPE_JSON}}
