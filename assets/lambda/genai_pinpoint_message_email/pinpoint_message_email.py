import json
import os

import boto3
from factory_module import MessageConfigFactoryCreator  # Import your factory module

CONTENT_TYPE_JSON = "application/json"


def lambda_handler(event, context):
    """Handle Lambda function for sending Pinpoint email messages.

    This Lambda function takes an API Gateway request and sends a message
    to the specified recipient using Amazon Pinpoint.

    :param event: AWS Lambda event object
    :param context: AWS Lambda context object
    :return: API Gateway response
    """
    try:
        # Parse the request body
        event_body = json.loads(event["body"])

        # Extract the recipient's address and message subject and body
        address = event_body["address"]
        message_subject = event_body["message-subject"]
        message_body_html = event_body["message-body-html"]
        message_body_text = event_body["message-body-text"]

        # Create a message request using the factory
        factory = MessageConfigFactoryCreator.create_factory("EMAIL")
        message_request = factory.create_message_request(address, message_subject, message_body_html, message_body_text)

        # Send the message using the Pinpoint client
        client = boto3.client("pinpoint")
        response = client.send_messages(ApplicationId=os.environ["PINPOINT_PROJECT_ID"], MessageRequest=message_request)

        # Return the response from Pinpoint
        return {"statusCode": 200, "body": json.dumps(response), "headers": {"Content-Type": CONTENT_TYPE_JSON}}
    except ValueError as e:
        # Handle invalid input
        return {"statusCode": 400, "body": str(e), "headers": {"Content-Type": CONTENT_TYPE_JSON}}
    except Exception as e:
        # Handle any other errors
        return {"statusCode": 500, "body": str(e), "headers": {"Content-Type": CONTENT_TYPE_JSON}}
