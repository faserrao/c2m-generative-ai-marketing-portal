"""
Lambda that prompts Pinpoint to send a message based on channel
"""

#########################
#   LIBRARIES & LOGGER
#########################

import xml.etree.ElementTree as ET
from io import BytesIO

import requests
from odf.opendocument import OpenDocumentText
from odf.text import P
from print_response import print_response
from requests_toolbelt.multipart.encoder import MultipartEncoder

upload_doc_url = "https://stage-rest.click2mail.com/molpro/documents"

# Define credentials
myusername = "stellario"
mypassword = "Babushka1!"

#########################
#        HANDLER
#########################


def string_to_odt_in_memory(content: str):

    doc = OpenDocumentText()
    paragraph = P(text=content)
    doc.text.addElement(paragraph)
    odt_stream = BytesIO()
    doc.save(odt_stream)
    odt_stream.seek(0)  # Reset stream position to the beginning

    return odt_stream


def c2m_upload_document(
    document_format: str = "ODT",
    document_name: str = "Test Letter ODT",
    document_class: str = "Letter 8.5 x 11",
    document_content: str = None,
    document_type: str = "application/odt",
):

    odt_stream = string_to_odt_in_memory(document_content)
    mp_encoder = MultipartEncoder(
        fields={
            "documentFormat": document_format,
            "documentName": document_name,
            "documentClass": document_class,
            "file": ("file.odt", odt_stream, document_type),
        }
    )

    headers = {"user-agent": "my-app/0.0.1", "Content-Type": mp_encoder.content_type}

    try:
        response = requests.post(upload_doc_url, headers=headers, auth=(myusername, mypassword), data=mp_encoder)
        response.raise_for_status()  # Raise an exception for HTTP errors

        if response.status_code == 201:
            print_response("Upload document call successful", response)

            xml_data = response.text
            root = ET.fromstring(xml_data)
            id_element = root.find("id")

            if id_element is not None:
                document_id = id_element.text
                return {"statusCode": 200, "body": document_id, "headers": {"Content-Type": "application/json"}}
            print_response("Upload document call failed", response)
            return {
                "statusCode": 400,
                "body": "No <id> element found in the XML.",
                "headers": {"Content-Type": "application/json"},
            }
        print_response("Upload document call failed", response)
        return {"statusCode": 400, "body": response.text, "headers": {"Content-Type": "application/json"}}
    except requests.exceptions.RequestException as e:
        exception_string = f"Add credit http request failed: {e}, {str(e)}"
        print_response(exception_string)
        return {"statusCode": 400, "body": str(e), "headers": {"Content-Type": "application/json"}}
