"""Lambda that interacts with Amazon Personalize to fetch all Batch segment
jobs."""

#########################
#   LIBRARIES & LOGGER
#########################

import datetime
import json
import logging
import sys

import boto3
from botocore.exceptions import ClientError

CONTENT_TYPE_JSON = "application/json"

LOGGER = logging.Logger("Content-generation", level=logging.DEBUG)
HANDLER = logging.StreamHandler(sys.stdout)
HANDLER.setFormatter(logging.Formatter("%(levelname)s | %(name)s | %(message)s"))
LOGGER.addHandler(HANDLER)

#########################
#        HANDLER
#########################


def lambda_handler(event, context):
    """Handle incoming requests for Personalize batch segment jobs."""

    # Get the HTTP method from the event object
    http_method = event["requestContext"]["http"]["method"]

    # Create personalize client
    personalize = boto3.client(service_name="personalize")

    # Check if the request is a GET request
    if http_method == "GET":
        try:
            # Call the list_batch_segment_jobs method
            response = personalize.list_batch_segment_jobs()

            # Return the list of batch segment jobs as a JSON response
            return {
                "statusCode": 200,
                "body": json.dumps(response, default=datetime_handler),
                "headers": {"Content-Type": CONTENT_TYPE_JSON},
            }

        except ClientError:
            # Handle any errors that occur

            return {
                "statusCode": 500,
                "body": "An error occurred while fetching the batch segment jobs",
                "headers": {"Content-Type": CONTENT_TYPE_JSON},
            }

    else:
        # Return an error response for unsupported HTTP methods
        return {"statusCode": 400, "body": "Unsupported HTTP method", "headers": {"Content-Type": CONTENT_TYPE_JSON}}


def datetime_handler(x):
    """Convert datetime objects to ISO format string."""
    if isinstance(x, datetime.datetime):
        return x.isoformat()
    raise TypeError("Unknown type")
