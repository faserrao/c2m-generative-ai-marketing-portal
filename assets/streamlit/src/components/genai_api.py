"""Helper classes for LLM inference."""

#########################
#    IMPORTS & LOGGER
#########################

from __future__ import annotations

import json
import os

import requests

#########################
#      CONSTANTS
#########################

API_URI = os.environ.get("API_URI")


#########################
#    HELPER FUNCTIONS
#########################


def invoke_content_creation(
    prompt: str,
    model_id: int,
    access_token: str,
    answer_length: int = 4096,
    temperature: float = 0.0,
) -> str:
    """Run LLM to generate content via API.

    This function sends a POST request to the LLM API with the given prompt,
    model ID, and other parameters. The API response is then parsed as JSON
    and returned as a string.

    Args:
        prompt (str): The input prompt for the LLM.
        model_id (int): The ID of the LLM model to use.
        access_token (str): The access token for the API.
        answer_length (int, optional): The length of the generated output.
            Defaults to 4096.
        temperature (float, optional): The temperature value for the LLM.
            Defaults to 0.0.

    Returns:
        str: The generated content as a string.
    """
    params = {
        # The input prompt for the LLM
        "query": prompt,
        # The type of request (content generation)
        "type": "content_generation",
        # Parameters for the LLM model
        "model_params": {
            # The ID of the LLM model to use
            "model_id": model_id,
            # The length of the generated output
            "answer_length": answer_length,
            # The temperature value for the LLM
            "temperature": temperature,
        },
    }
    # Send the POST request to the LLM API
    response = requests.post(
        url=API_URI + "/content/bedrock",
        json=params,
        stream=False,
        headers={"Authorization": access_token},
    )
    # Parse the response as JSON and return it as a string
    return json.loads(response.text)
