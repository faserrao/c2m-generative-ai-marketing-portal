"""Lambda that prompts Pinpoint to send a message based on channel."""

#########################
#   LIBRARIES & LOGGER
#########################

import xml.etree.ElementTree as ET

import requests
from print_response import print_response

CREATE_JOB_URL = "https://stage-rest.click2mail.com/molpro/jobs"

# Define constants
CONTENT_TYPE_JSON = "application/json"

# Define credentials
MY_USERNAME = "stellario"
MY_PASSWORD = "Babushka1!"

#########################
#        HANDLER
#########################


def c2m_create_job(
    document_class: str = "Letter 8.5 x 11",
    layout: str = "Address on Separate Page",
    production_time: str = "Next Day",
    envelope: str = "#10 Double Window",
    color: str = "Black and White",
    paper_type: str = "White 24#",
    print_option: str = "Printing One side",
    document_id: str = None,
    address_list_id: str = None,
):
    """Create a job for Click2Mail service."""
    headers = {"user-agent": "my-app/0.0.1"}
    values = {
        "documentClass": document_class,
        "layout": layout,
        "productionTime": production_time,
        "envelope": envelope,
        "color": color,
        "paperType": paper_type,
        "printOption": print_option,
        "documentId": document_id,
        "addressId": address_list_id,
    }

    try:
        response = requests.post(CREATE_JOB_URL, data=values, headers=headers, auth=(MY_USERNAME, MY_PASSWORD))
        response.raise_for_status()
        if response.status_code == 201:
            print_response("Add create job successful", response)

            xml_data = response.text
            root = ET.fromstring(xml_data)
            id_element = root.find("id")

            if id_element is not None:
                job_id = id_element.text
                return {"statusCode": 200, "body": job_id, "headers": {"Content-Type": CONTENT_TYPE_JSON}}
            print_response("Add create job failed", response)
            return {"statusCode": 400, "body": response.text, "headers": {"Content-Type": CONTENT_TYPE_JSON}}
    except requests.exceptions.RequestException as e:
        exception_string = f"Create jobhttp request failed: {e}, {str(e)}"
        print_response(exception_string)
        return {"statusCode": 400, "body": str(e), "headers": {"Content-Type": CONTENT_TYPE_JSON}}
