"""Lambda that gets Export Job from Pinpoint."""

#########################
#   LIBRARIES & LOGGER
#########################

import json
import logging
import os
import sys

import boto3
from botocore.exceptions import ClientError

CONTENT_TYPE_JSON = "application/json"

LOGGER = logging.Logger("Content-generation", level=logging.DEBUG)
HANDLER = logging.StreamHandler(sys.stdout)
HANDLER.setFormatter(logging.Formatter("%(levelname)s | %(name)s | %(message)s"))
LOGGER.addHandler(HANDLER)


#########################
#        HELPER
#########################

PINPOINT_PROJECT_ID = os.environ["PINPOINT_PROJECT_ID"]
PINPOINT_EXPORT_ROLE_ARN = os.environ["PINPOINT_EXPORT_ROLE_ARN"]
S3_BUCKET_NAME = os.environ["BUCKET_NAME"]

#########################
#        HANDLER
#########################


def lambda_handler(event, context):
    """Handle GET and POST requests for Pinpoint export jobs.

    GET /pinpoint/export-jobs/{job-id}:
        Fetch the export job with the given job ID from Pinpoint.

    POST /pinpoint/export-jobs:
        Create a new export job for the given segment ID in Pinpoint.

    :param event: AWS Lambda event object
    :param context: AWS Lambda context object
    :return: API Gateway response
    """
    # Get the HTTP method from the event object
    http_method = event["requestContext"]["http"]["method"]

    # Check if the request is a GET request
    if http_method == "GET":
        # Get the Pinpoint project ID from the environment variable
        pinpoint_project_id = os.environ["PINPOINT_PROJECT_ID"]
        # parse event
        event = json.loads(event["body"])
        # Get Pinpoint Export Job ID from the event
        export_job_id = event["job-id"]

        # Create a Pinpoint client
        client = boto3.client("pinpoint")

        try:
            # Perform the get-export-job operation
            response = client.get_export_job(ApplicationId=pinpoint_project_id, JobId=export_job_id)

            # Extract the job status
            export_job_response = response["ExportJobResponse"]

            # Return the export job response as a JSON response
            return {
                "statusCode": 200,
                "body": json.dumps(export_job_response),
                "headers": {"Content-Type": CONTENT_TYPE_JSON},
            }

        except ClientError as e:
            # Handle any errors that occur
            print(e)
            return {
                "statusCode": 500,
                "body": "An error occurred while fetching the export job",
                "headers": {"Content-Type": CONTENT_TYPE_JSON},
            }

    # Check if the request is a POST request
    elif http_method == "POST":
        print("Pinpoint Create Export Job Event")
        print(event)
        # Create a Pinpoint client
        client = boto3.client("pinpoint")
        # parse event
        event = json.loads(event["body"])
        segment_id = event["segment-id"]
        try:
            # Perform the create-export-job operation
            response = client.create_export_job(
                ApplicationId=PINPOINT_PROJECT_ID,
                ExportJobRequest={
                    "RoleArn": PINPOINT_EXPORT_ROLE_ARN,
                    "S3UrlPrefix": f"s3://{S3_BUCKET_NAME}/exported-segments/{segment_id}/",
                    "SegmentId": segment_id,
                },
            )
            # Extract the job status

            export_job_response = response["ExportJobResponse"]

            # Return the export job response as a JSON response
            return {
                "statusCode": 200,
                "body": json.dumps(export_job_response),
                "headers": {"Content-Type": CONTENT_TYPE_JSON},
            }

        except ClientError as e:
            # Handle any errors that occur
            print(e)
            return {
                "statusCode": 500,
                "body": "An error occurred while creating the export job",
                "headers": {"Content-Type": CONTENT_TYPE_JSON},
            }
    else:
        # Return an error response for unsupported HTTP methods
        return {
            "statusCode": 400,
            "body": "Unsupported HTTP method",
            "headers": {"Content-Type": CONTENT_TYPE_JSON},
        }
