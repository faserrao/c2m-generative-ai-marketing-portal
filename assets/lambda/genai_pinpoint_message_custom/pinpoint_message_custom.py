import json
import logging
import sys
import pkgutil
import subprocess


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

    # Check if the Python packages required for Pinpoint messaging are installed
    installed_modules = [mod.name for mod in pkgutil.iter_modules()]
    print(f"installed_modules() event: {installed_modules}")

    # Print the current version of the packages
    result = subprocess.run(["pip", "freeze"], stdout=subprocess.PIPE)
    result.stdout.decode("utf-8")

    # Parse the event object
    event_body = json.loads(event["body"])
    print(f"pinpoint_message() event: {event}")
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
