"""Lambda that performs summarization with Bedrock."""

#########################
#   LIBRARIES & LOGGER
#########################

import json
import logging
import os
import sys
from datetime import datetime, timezone

import boto3
from botocore.config import Config

LOGGER = logging.Logger("Content-generation", level=logging.DEBUG)
HANDLER = logging.StreamHandler(sys.stdout)
HANDLER.setFormatter(logging.Formatter("%(levelname)s | %(name)s | %(message)s"))
LOGGER.addHandler(HANDLER)


#########################
#        HELPER
#########################
BEDROCK_ROLE_ARN = os.environ["BEDROCK_ROLE_ARN"]
BEDROCK_CONFIG = Config(connect_timeout=60, read_timeout=60, retries={"max_attempts": 10})

MODELS_MAPPING = {
    "Bedrock: Amazon Titan": "amazon.titan-tg1-large",
    "Bedrock: Claude": "anthropic.claude-v1",
    "Bedrock: Claude V2": "anthropic.claude-v2",
    "Bedrock: Claude Instant": "anthropic.claude-instant-v1",
    "Bedrock: J2 Grande Instruct": "ai21.j2-grande-instruct",
    "Bedrock: J2 Jumbo Instruct": "ai21.j2-jumbo-instruct",
    "Bedrock: Claude Haiku": "anthropic.claude-3-haiku-20240307-v1:0",
}


def create_bedrock_client():
    """Create and return a Bedrock client. If the BEDROCK_ROLE_ARN environment
    variable is set, use cross-account access. Otherwise, use the same AWS
    account.

    Returns:
        tuple: A tuple where the first element is the Bedrock client and the
        second element is the expiration datetime of the assumed role
        credentials (if cross-account access is used).
    """
    if BEDROCK_ROLE_ARN != "None":
        LOGGER.info("Using cross-account bedrock client.")
        role_arn = None

        # Check if the BEDROCK_ROLE_ARN environment variable is a non-empty
        # string and not "None".
        if isinstance(role_arn, str) and role_arn != "None":
            role_arn = os.environ["BEDROCK_ROLE_ARN"]
        else:
            raise ValueError(
                "Cross-account arn is not empty but not a string! Please check "
                "the BEDROCK_ROLE_ARN environment variable."
            )

        LOGGER.info("Using ARN: %s", role_arn)

        # Assume the role using the STS client.
        sts_connection = boto3.client("sts")
        acct_bedrock = sts_connection.assume_role(RoleArn=role_arn, RoleSessionName="cross_account_bedrock")

        # Extract the temporary access key ID, secret key, and session token
        # from the assumed role.
        access_key = acct_bedrock["Credentials"]["AccessKeyId"]
        secret_key = acct_bedrock["Credentials"]["SecretAccessKey"]
        session_token = acct_bedrock["Credentials"]["SessionToken"]

        # Extract the expiration datetime of the assumed role credentials.
        expiration = acct_bedrock["Credentials"]["Expiration"]

        # Get the region from the environment variable.
        region = os.environ["BEDROCK_REGION"]

        # Create the Bedrock client using the assumed role credentials.
        bedrock_client = boto3.client(
            service_name="bedrock-runtime",
            region_name=region,
            endpoint_url=f"https://bedrock.{region}.amazonaws.com",
            config=BEDROCK_CONFIG,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            aws_session_token=session_token,
        )

    else:
        LOGGER.info("Using bedrock client from same account.")
        bedrock_client = boto3.client(
            service_name="bedrock-runtime",
            region_name=os.environ["BEDROCK_REGION"],
            config=BEDROCK_CONFIG,
        )
        expiration = None
    LOGGER.info("Successfully set bedrock client")

    return bedrock_client, expiration


BEDROCK_CLIENT, EXPIRATION = create_bedrock_client()


def verify_bedrock_client():
    """Check if the Bedrock client token is still valid. This function should
    be called before every invocation of the Bedrock client to ensure that the
    token is not expired.

    Returns:
        bool: True if the token is not expired, False otherwise.
    """
    # Check if the expiration time is set and the token is not expired.
    if EXPIRATION is not None:
        now = datetime.now(timezone.utc)
        LOGGER.info("Bedrock token expires in %s seconds", (EXPIRATION - now).total_seconds())
        # If the token is about to expire (less than 1 minute), return False.
        if (EXPIRATION - now).total_seconds() < 60:
            return False
    # If the token is not expired, return True.
    return True


def generate_message(bedrock_runtime, model_id, system_prompt, messages, max_tokens):
    """Generate a message using the Bedrock runtime.

    Args:
        bedrock_runtime (Bedrock): The Bedrock runtime client.
        model_id (str): The ID of the model to use.
        system_prompt (str): The system prompt to pass to the model.
        messages (list[dict]): The chat history to pass to the model.
        max_tokens (int): The maximum number of tokens to generate.

    Returns:
        dict: The response from the Bedrock runtime.
    """
    body = json.dumps(
        {
            # Use the latest version of the Bedrock API.
            "anthropic_version": "bedrock-2023-05-31",
            # Set the maximum number of tokens to generate.
            "max_tokens": max_tokens,
            # Pass the system prompt to the model.
            "system": system_prompt,
            # Pass the chat history to the model.
            "messages": messages,
        }
    )

    # Invoke the model using the Bedrock runtime.
    return bedrock_runtime.invoke_model(body=body, modelId=model_id)


#########################
#        HANDLER
#########################


def lambda_handler(event, context):
    """Lambda handler that takes the event and context and uses the Bedrock
    runtime to generate text based on the given query and model parameters.

    Args:
        event (dict): The event object containing the query and model parameters.
        context (object): The context object.

    Returns:
        str: The generated text.
    """
    LOGGER.info("Starting execution of lambda_handler()")

    # PREPARATIONS
    # Convert the 'body' string to a dictionary
    body_data = json.loads(event["body"])

    # Extract the 'query' value
    query_value = body_data["query"]

    # Extract the 'model_params' value
    model_params_value = body_data["model_params"]

    # get fixed model params
    model_id = MODELS_MAPPING[model_params_value["model_id"]]
    LOGGER.info("model_id: %s", model_id)

    with open(f"model_configs/{model_id}.json", encoding="utf-8") as file:
        fixed_params = json.load(file)

    # load variable model params
    amazon_flag = False
    claude3_flag = False
    model_params = {}
    if model_id.startswith("amazon"):
        model_params = {
            "maxTokenCount": model_params_value["answer_length"],
            "stopSequences": fixed_params["STOP_WORDS"],
            "temperature": model_params_value["temperature"],
            "topP": fixed_params["TOP_P"],
        }
        amazon_flag = True
    elif model_id.startswith("anthropic.claude-3"):
        model_params = {
            "max_tokens_to_sample": model_params_value["answer_length"],
            "temperature": model_params_value["temperature"],
            "top_p": fixed_params["TOP_P"],
            "stop_sequences": fixed_params["STOP_WORDS"],
        }
        claude3_flag = True
    elif model_id.startswith("anthropic"):
        model_params = {
            "max_tokens_to_sample": model_params_value["answer_length"],
            "temperature": model_params_value["temperature"],
            "top_p": fixed_params["TOP_P"],
            "stop_sequences": fixed_params["STOP_WORDS"],
        }
        query_value = f"\n\nHuman:{query_value}\n\nAssistant:"
    elif model_id.startswith("ai21"):
        model_params = {
            "maxTokens": model_params_value["answer_length"],
            "stopSequences": fixed_params["STOP_WORDS"],
            "temperature": model_params_value["temperature"],
            "topP": fixed_params["TOP_P"],
        }
    LOGGER.info("MODEL_PARAMS: %s", model_params)

    # Check if the Bedrock client token is expired and refresh if necessary
    if not verify_bedrock_client():
        LOGGER.info("Bedrock client expired, will refresh token.")
        global BEDROCK_CLIENT, EXPIRATION
        BEDROCK_CLIENT, EXPIRATION = create_bedrock_client()

    accept = "application/json"
    content_type = "application/json"

    # Based on the model_id, construct the input and invoke the model
    if amazon_flag:
        input_data = json.dumps(
            {
                "inputText": query_value,
                "textGenerationConfig": model_params,
            }
        )
        response = BEDROCK_CLIENT.invoke_model(
            body=input_data, modelId=model_id, accept=accept, contentType=content_type
        )
    elif claude3_flag:
        system_prompt = "Please respond directly to user request. Do not add any extra comments"
        # Prompt with user turn only.
        user_message = {"role": "user", "content": query_value}
        messages = [user_message]
        max_tokens = 4096
        response = generate_message(BEDROCK_CLIENT, model_id, system_prompt, messages, max_tokens)

    else:
        body = json.dumps({"prompt": query_value, **model_params})
        response = BEDROCK_CLIENT.invoke_model(body=body, modelId=model_id, accept=accept, contentType=content_type)

    response_body = json.loads(response.get("body").read())

    if "amazon" in model_id:
        response = response_body.get("results")[0].get("outputText")
    elif "claude-3" in model_id:
        response = response_body["content"][0]["text"]
    elif "anthropic" in model_id:
        response = response_body.get("completion")
    elif "ai21" in model_id:
        response = response_body.get("completions")[0].get("data").get("text")

    return json.dumps(response)
