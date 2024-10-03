"""Helper classes for Amazon Personalize."""

#########################
#    IMPORTS & LOGGER
#########################

from __future__ import annotations

import os

import requests

#########################
#      CONSTANTS
#########################

API_URI = os.environ.get("API_URI")


#########################
#    HELPER FUNCTIONS
#########################


# ********* Personalize API *********
def invoke_personalize_batch_segment(
    access_token: str,
    item_ids: str,
    num_results: int,
) -> list:
    """Start a batch segmentation job in Personalize.

    The job takes a list of item IDs and the number of results desired for each item.

    Args:
        access_token (str): The access token for the Personalize API.
        item_ids (str): The list of item IDs to be segmented.
        num_results (int): The number of results desired for each item.

    Returns:
        list: The response content from the Personalize API.
    """
    params = {
        "item-ids": item_ids,
        "num-results": num_results,
    }
    response = requests.post(
        url=API_URI + "/personalize/batch-segment-job",
        json=params,
        stream=False,
        headers={"Authorization": access_token},
    )
    return response.content


def invoke_personalize_get_jobs(
    access_token: str,
) -> list:
    """Get all batch segment jobs in personalize.

    Returns a list of all batch segment jobs in Personalize.
    """
    params = {}
    response = requests.get(
        url=API_URI + "/personalize/batch-segment-jobs",
        json=params,
        stream=False,
        headers={"Authorization": access_token},
    )
    return response.content


def invoke_personalize_describe_job(
    access_token: str,
    job_arn: str,
) -> list:
    """Describe a batch segment job in personalize.

    Args:
        access_token (str): The access token for the Personalize API.
        job_arn (str): The ARN of the batch segment job to describe.

    Returns:
        list: The response content from the Personalize API.
    """
    params = {"job-arn": job_arn}
    response = requests.get(
        url=API_URI + "/personalize/batch-segment-job",
        json=params,
        stream=False,
        headers={"Authorization": access_token},
    )
    return response.content
