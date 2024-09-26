import json
import os

import boto3
from factory_module import MessageConfigFactoryCreator  # Import your factory module

CONTENT_TYPE_JSON = "application/json"


def lambda_handler(event, context):
    """Handle Lambda function for sending Pinpoint email messages.

    :param event: AWS Lambda event object
    :param context: AWS Lambda context object
    :return: API Gateway response
    """
    try:
        event_body = json.loads(event["body"])
        address = event_body["address"]
        message_subject = event_body["message-subject"]
        message_body_html = event_body["message-body-html"]
        message_body_text = event_body["message-body-text"]

        try:
            factory = MessageConfigFactoryCreator.create_factory("EMAIL")
            message_request = factory.create_message_request(
                address, message_subject, message_body_html, message_body_text
            )
        except ValueError as e:
            return {"statusCode": 400, "body": str(e), "headers": {"Content-Type": CONTENT_TYPE_JSON}}

        client = boto3.client("pinpoint")
        response = client.send_messages(ApplicationId=os.environ["PINPOINT_PROJECT_ID"], MessageRequest=message_request)

        return {"statusCode": 200, "body": json.dumps(response), "headers": {"Content-Type": CONTENT_TYPE_JSON}}
    except Exception as e:
        return {"statusCode": 500, "body": str(e), "headers": {"Content-Type": CONTENT_TYPE_JSON}}
