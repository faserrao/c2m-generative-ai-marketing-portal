#########################
#   LIBRARIES & LOGGER
#########################

import json
# import logging
import os
import sys
from datetime import datetime, timezone

from requests_toolbelt.multipart.encoder import MultipartEncoder
import requests
from factory_module import MessageConfigFactoryCreator  # Import your factory module

"""
LOGGER = logging.Logger("Content-generation", level=logging.DEBUG)
HANDLER = logging.StreamHandler(sys.stdout)
HANDLER.setFormatter(logging.Formatter("%(levelname)s | %(name)s | %(message)s"))
LOGGER.addHandler(HANDLER)
"""

def lambda_handler(event, context):

    print("Channel is CUSTOM")
    print("In the pinpoint_message() Lambda")

    event_body = json.loads(event["body"])
    print(f"pinpoint_message() event: {event}")
    address = event_body["address"]
    message_subject = event_body["message-subject"]
    message_body_html = event_body["message-body-html"]
    message_body_text = event_body["message-body-text"]

    print('address = ', address)
    print('message_subject = ', message_subject)
    print('message_body_html = ', message_body_html)
    print('message_body_text = ', message_body_text)

    try:
        factory = MessageConfigFactoryCreator.create_factory("CUSTOM")
        print('Before calling factory.create_message_request()')
        message_request = factory.create_message_request(address, message_subject, message_body_html, message_body_text)
        print('Adfter calling factory.create_message_request()')
    except ValueError as e:
        print('lambda_handler Value error')
        return {"statusCode": 400, "body": str(e), "headers": {"Content-Type": "application/json"}}

    print('Before return from lambda hander')
    return {"statusCode": 200, "body": json.dumps(message_request), "headers": {"Content-Type": "application/json"}}