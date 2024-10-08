"""Lambda that gets Fetches file from S3 (used by both Pinpoint and
Personalize)"""

#########################
#   LIBRARIES & LOGGER
#########################

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
#        HELPER
#########################


#########################
#        HANDLER
#########################


def lambda_handler(event, context):
    """Handle S3 file fetching requests for Pinpoint and Personalize.

    :param event: AWS Lambda event object
    :param context: AWS Lambda context object
    :return: HTTP response with fetched file paths or error message
    """
    # Get the HTTP method from the event object
    http_method = event["requestContext"]["http"]["method"]

    # Check if the request is a GET request
    if http_method == "GET":
        # Initialize the S3 client
        s3_client = boto3.client("s3")

        # Parse the event object
        event = json.loads(event["body"])

        # Get S3 url prefix and total number of pieces from the event
        s3_url_prefix = event["s3-url-prefix"]
        total_pieces = event["total-pieces"]

        # Extract bucket name and folder path from the S3 URL prefix
        bucket_name = s3_url_prefix.split("/")[2]
        folder_path = "/".join(s3_url_prefix.split("/")[3:])

        # Check if the total pieces is not 0
        if total_pieces != 0:
            # Total Pieces is not 0, therefore this is used by Pinpoint to fetch files
            try:
                # List objects in the specified S3 bucket folder
                response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=folder_path)

                # Filter out the specified files and sort by LastModified timestamp
                sorted_files = sorted(
                    [
                        obj
                        for obj in response.get("Contents", [])
                        if obj["Key"] not in [folder_path + "COMPLETED", folder_path + "EXPORT_VALIDATED"]
                    ],
                    key=lambda x: x["LastModified"],
                    reverse=True,
                )

                # Get the latest files according to total number of pieces
                latest_files = sorted_files[:total_pieces]

                # Extract full S3 URIs for the result
                file_paths = [f"{bucket_name}/{file['Key']}" for file in latest_files]

                # Return the latest files as a JSON response
                return {
                    "statusCode": 200,
                    "body": json.dumps(file_paths),
                    "headers": {"Content-Type": CONTENT_TYPE_JSON},
                }

            except ClientError as e:
                # Handle any errors that occur
                print(e)
                # Return an error response
                return {
                    "statusCode": 500,
                    "body": "An error occurred while fetching the files",
                    "headers": {"Content-Type": CONTENT_TYPE_JSON},
                }

        else:
            # Total Pieces is 0, therefore this is used by Personalize to fetch files
            try:
                # List objects in the specified S3 bucket folder
                response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=folder_path)

                # Filter out the specified files and sort by LastModified timestamp
                sorted_files = sorted(
                    [
                        obj
                        for obj in response.get("Contents", [])
                        if obj["Key"] not in [folder_path + "COMPLETED", folder_path + "EXPORT_VALIDATED"]
                    ],
                    key=lambda x: x["LastModified"],
                    reverse=True,
                )

                # Extract full S3 URIs for the result
                file_paths = [f"{bucket_name}/{file['Key']}" for file in sorted_files]

                # Return the latest files as a JSON response
                return {
                    "statusCode": 200,
                    "body": json.dumps(file_paths),
                    "headers": {"Content-Type": CONTENT_TYPE_JSON},
                }

            except ClientError as e:
                # Handle any errors that occur
                print(e)
                # Return an error response
                return {
                    "statusCode": 500,
                    "body": "An error occurred while fetching the files",
                    "headers": {"Content-Type": CONTENT_TYPE_JSON},
                }

    else:
        # Return an error response for unsupported HTTP methods
        return {"statusCode": 400, "body": "Unsupported HTTP method", "headers": {"Content-Type": CONTENT_TYPE_JSON}}
