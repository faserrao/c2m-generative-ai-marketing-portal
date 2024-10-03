"""Lambda that fetches interacts with Pinpoint through APIGateway."""

#########################
#   LIBRARIES & LOGGER
#########################

import json
import logging
import os
import sys

import boto3
from botocore.exceptions import ClientError

LOGGER = logging.Logger("Content-generation", level=logging.DEBUG)
HANDLER = logging.StreamHandler(sys.stdout)
HANDLER.setFormatter(logging.Formatter("%(levelname)s | %(name)s | %(message)s"))
LOGGER.addHandler(HANDLER)

JSON_CONTENT_TYPE = {"Content-Type": "application/json"}

#########################
#        HELPER
#########################

PINPOINT_PROJECT_ID = os.environ["PINPOINT_PROJECT_ID"]

#########################
#        HANDLER
#########################


def lambda_handler(event, context):
    """Handle HTTP requests to interact with Pinpoint segments.

    This handler responds to GET requests and returns a list of all segments
    in the specified Pinpoint project.

    Args:
        event (dict): API Gateway event object
        context (dict): AWS Lambda context object

    Returns:
        dict: API Gateway response object
    """
    # Get the HTTP method from the event object
    http_method = event["requestContext"]["http"]["method"]

    # Check if the request is a GET request
    if http_method == "GET":
        # Get the Pinpoint project ID from the environment variable
        pinpoint_project_id = os.environ["PINPOINT_PROJECT_ID"]

        # Create a Pinpoint client
        client = boto3.client("pinpoint")

        try:
            # Perform the get-segments operation
            response = client.get_segments(ApplicationId=pinpoint_project_id)

            # Extract the segments
            segments = response["SegmentsResponse"]["Item"]

            # Return the segments as a JSON response
            return {"statusCode": 200, "body": json.dumps(segments), "headers": JSON_CONTENT_TYPE}

        except ClientError as e:
            # Handle any errors that occur
            print(e)
            return {
                "statusCode": 500,
                "body": "An error occurred while fetching the segments",
                "headers": JSON_CONTENT_TYPE,
            }
    else:
        # Return an error response for unsupported HTTP methods
        return {"statusCode": 400, "body": "Unsupported HTTP method", "headers": JSON_CONTENT_TYPE}
