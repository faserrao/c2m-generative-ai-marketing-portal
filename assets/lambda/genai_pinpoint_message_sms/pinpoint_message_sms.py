import json
import os

import boto3
from factory_module import MessageConfigFactoryCreator

CONTENT_TYPE_JSON = "application/json"


def lambda_handler(event, context):
    """Handle Lambda function invocation for sending SMS via Pinpoint."""

    event_body = json.loads(event["body"])
    address = event_body["address"]
    message_body_text = event_body["message-body-text"]
    address = "+1" + address

    try:
        try:
            factory = MessageConfigFactoryCreator.create_factory("SMS")
            message_request = factory.create_message_request(address, None, None, message_body_text)
        except ValueError as e:
            return {"statusCode": 400, "body": str(e), "headers": {"Content-Type": CONTENT_TYPE_JSON}}

        client = boto3.client("pinpoint")
        response = client.send_messages(ApplicationId=os.environ["PINPOINT_PROJECT_ID"], MessageRequest=message_request)

        return {"statusCode": 200, "body": json.dumps(response), "headers": {"Content-Type": CONTENT_TYPE_JSON}}
    except Exception as e:
        return {"statusCode": 500, "body": str(e), "headers": {"Content-Type": CONTENT_TYPE_JSON}}
