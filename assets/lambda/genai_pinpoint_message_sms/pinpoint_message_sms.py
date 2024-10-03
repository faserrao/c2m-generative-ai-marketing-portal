import json
import os

import boto3
from factory_module import MessageConfigFactoryCreator

CONTENT_TYPE_JSON = "application/json"


def lambda_handler(event, context):
    """Handle Lambda function invocation for sending SMS via Pinpoint.

    This function is responsible for sending a message using Pinpoint based on the
    channel specified in the request. The channel is expected to be "SMS".

    Args:
        event (dict): The API Gateway event object.
        context (object): The AWS Lambda context object.

    Returns:
        dict: The response object.
    """
    event_body = json.loads(event["body"])
    address = event_body["address"]
    message_body_text = event_body["message-body-text"]
    # Preface the SMS address with +1
    address = "+1" + address

    try:
        try:
            # Create a message request using the factory
            factory = MessageConfigFactoryCreator.create_factory("SMS")
            message_request = factory.create_message_request(address, None, None, message_body_text)
        except ValueError as e:
            # Handle any errors that occur while parsing the request
            return {"statusCode": 400, "body": str(e), "headers": {"Content-Type": CONTENT_TYPE_JSON}}

        # Create a Pinpoint client
        client = boto3.client("pinpoint")

        # Send the message using the Pinpoint client
        response = client.send_messages(ApplicationId=os.environ["PINPOINT_PROJECT_ID"], MessageRequest=message_request)

        # Return the response from Pinpoint
        return {"statusCode": 200, "body": json.dumps(response), "headers": {"Content-Type": CONTENT_TYPE_JSON}}
    except Exception as e:
        # Handle any other errors
        return {"statusCode": 500, "body": str(e), "headers": {"Content-Type": CONTENT_TYPE_JSON}}
