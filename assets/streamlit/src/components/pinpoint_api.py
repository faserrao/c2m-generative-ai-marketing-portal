"""Helper classes for Amazon Pinpoint."""

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


# ********* Pinpoint API *********
def invoke_pinpoint_segment(
    access_token: str,
) -> list:
    """Get Segments From Pinpoint Project."""
    response = requests.get(
        url=API_URI + "/pinpoint/segment",
        stream=False,
        headers={"Authorization": access_token},
    )
    return response.content


def invoke_pinpoint_create_export_job(access_token: str, segment_id: str) -> list:
    """Create Export Job For A Pinpoint Segment."""
    params = {"segment-id": segment_id}
    response = requests.post(
        url=API_URI + "/pinpoint/job",
        json=params,
        stream=False,
        headers={"Authorization": access_token},
    )
    return response.content


def invoke_pinpoint_export_job_status(access_token: str, job_id: str) -> list:
    """Get Export Job Status From Pinpoint."""
    params = {"job-id": job_id}
    response = requests.get(
        url=API_URI + "/pinpoint/job",
        json=params,
        stream=False,
        headers={"Authorization": access_token},
    )
    return response.content


def invoke_pinpoint_send_message(
    access_token: str,
    address: str,
    channel: str,
    message_body_text: str,
    message_subject: str = None,
    message_body_html: str = None,
) -> list:
    """Send a message using Amazon Pinpoint.

    Args:
        access_token (str): Authentication token.
        address (str): Recipient address.
        channel (str): Message channel (EMAIL, SMS, or CUSTOM).
        message_body_text (str): Plain text message body.
        message_subject (str, optional): Message subject for email.
        message_body_html (str, optional): HTML message body for email.

    Returns:
        list: Response content from the Pinpoint API.
    """
    params = {
        "address": address,
        "channel": channel,
        "message-subject": message_subject,
        "message-body-html": message_body_html,
        "message-body-text": message_body_text,
    }

    api_endpoints = {"EMAIL": "/pinpoint/email", "SMS": "/pinpoint/sms", "CUSTOM": "/pinpoint/custom"}

    # Select the appropriate API endpoint based on the channel
    url = API_URI + api_endpoints.get(channel)
    if not url:
        raise ValueError(f"Unsupported channel: {channel}")

    # TODO: Use APU_URI
    response = requests.post(
        #        url=API_URI + "/pinpoint/message",
        url=url,
        json=params,
        stream=False,
        headers={"Authorization": access_token},
    )
    return response.content


def invoke_s3_fetch_files(
    access_token: str,
    s3_url_prefix: str,
    total_pieces: int,
) -> list:
    """Get Files URI from S3 which were exported by Pinpoint."""
    params = {
        "s3-url-prefix": s3_url_prefix,
        "total-pieces": total_pieces,
    }
    response = requests.get(
        url=API_URI + "/s3",
        json=params,
        stream=False,
        headers={"Authorization": access_token},
    )
    return response.content
