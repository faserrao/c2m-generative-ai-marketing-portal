import json
import logging
import sys

from factory_module import MessageConfigFactoryCreator  # Import your factory module

LOGGER = logging.Logger("Content-generation", level=logging.DEBUG)
HANDLER = logging.StreamHandler(sys.stdout)
HANDLER.setFormatter(logging.Formatter("%(levelname)s | %(name)s | %(message)s"))
LOGGER.addHandler(HANDLER)

def lambda_handler(event, context):

    event_body = json.loads(event["body"])
    print(f"pinpoint_message() event: {event}")
    address = event_body["address"]
    message_subject = event_body["message-subject"]
    message_body_html = event_body["message-body-html"]
    message_body_text = event_body["message-body-text"]

    try:
        factory = MessageConfigFactoryCreator.create_factory("CUSTOM")
        message_request = factory.create_message_request(address, message_subject, message_body_html, message_body_text)
    except ValueError as e:
        return {"statusCode": 400, "body": str(e), "headers": {"Content-Type": "application/json"}}

    return {"statusCode": 200, "body": json.dumps(message_request), "headers": {"Content-Type": "application/json"}}