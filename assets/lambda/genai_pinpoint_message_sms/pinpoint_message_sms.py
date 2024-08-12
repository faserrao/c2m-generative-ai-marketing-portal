import boto3
import os
import json
from factory_module import MessageConfigFactoryCreator  # Import your factory module

def lambda_handler(event, context):
    try:
        event_body = json.loads(event["body"])
        address = event_body["address"]
        message_body_text = event_body["message-body-text"]

        # Preface the SMS address with +1 for Pinpoint
        address = '+1' + address

        try:
            factory = MessageConfigFactoryCreator.create_factory("SMS")
            message_request = factory.create_message_request(address, None, None, message_body_text)
        except ValueError as e:
            return {"statusCode": 400, "body": str(e), "headers": {"Content-Type": "application/json"}}

        client = boto3.client("pinpoint")
        response = client.send_messages(
            ApplicationId=os.environ["PINPOINT_PROJECT_ID"],
            MessageRequest=message_request
        )

        return {"statusCode": 200, "body": json.dumps(response), "headers": {"Content-Type": "application/json"}}
    except Exception as e:
        return {"statusCode": 500, "body": str(e), "headers": {"Content-Type": "application/json"}}