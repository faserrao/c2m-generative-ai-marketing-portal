"""Lamda that sends a custom message"""
import json
import logging
import sys

from factory_module import MessageConfigFactoryCreator  # Import your factory module

LOGGER = logging.Logger("Content-generation", level=logging.DEBUG)
HANDLER = logging.StreamHandler(sys.stdout)
HANDLER.setFormatter(logging.Formatter("%(levelname)s | %(name)s | %(message)s"))
LOGGER.addHandler(HANDLER)


def lambda_handler(event, context):
    """Handle Lambda function invocation for custom Pinpoint message
    generation.

    Args:
        event (dict): AWS Lambda event object
        context (object): AWS Lambda context object

    Returns:
        dict: A dictionary containing the response status code, body, and headers
    """

    print(f"event = {event}")
    print(f"context = {context}")

    # Parse the event object
    event_body = json.loads(event["body"])
    address = event_body["address"]
    message_subject = event_body["message-subject"]
    message_body_html = event_body["message-body-html"]
    message_body_text = event_body["message-body-text"]

    # Create a message request using the factory module
    try:
        factory = MessageConfigFactoryCreator.create_factory("CUSTOM")
        message_request = factory.create_message_request(address, message_subject, message_body_html, message_body_text)
    except ValueError as e:
        return {"statusCode": 400, "body": str(e), "headers": {"Content-Type": "application/json"}}

    # Return the message request as a JSON response
    return {"statusCode": 200, "body": json.dumps(message_request), "headers": {"Content-Type": "application/json"}}
