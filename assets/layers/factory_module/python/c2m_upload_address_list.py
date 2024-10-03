"""Lambda that prompts Pinpoint to send a message based on channel."""

#########################
#   LIBRARIES & LOGGER
#########################

import xml.etree.ElementTree as ET
from io import BytesIO

import requests
from odf.opendocument import OpenDocumentText
from odf.text import P
from print_response import print_response

UPLOAD_ADDRESS_LIST_URL = "https://stage-rest.click2mail.com/molpro/addressLists"

# Define credentials
USERNAME = "stellario"
PASSWORD = "Babushka1!"

# Add this constant at the top of the file, with other constants
JSON_CONTENT_TYPE = "application/json"

#########################
#        HANDLER
#########################


def string_to_odt_in_memory(content: str) -> BytesIO:
    """Convert a string to an in-memory ODT document.

    Args:
        content (str): The string to convert to an ODT document.

    Returns:
        BytesIO: An in-memory ODT document.
    """

    # Create an OpenDocumentText object
    doc = OpenDocumentText()

    # Add the content to the document as a paragraph
    paragraph = P(text=content)
    doc.text.addElement(paragraph)

    # Save the document to an in-memory stream
    odt_stream = BytesIO()
    doc.save(odt_stream)

    # Reset the stream position to the beginning
    odt_stream.seek(0)

    return odt_stream


def c2m_upload_address_list(
    address_list_name: str = "",
    address_list_mapping_id: str = "",
    first_name: str = "first_name",
    last_name: str = "last_name",
    organization: str = "",
    address_1: str = "",
    address_2: str = "",
    address_3: str = "",
    city: str = "",
    state: str = "",
    postal_code: str = "",
    country: str = "",
) -> dict:
    """Upload an address list to Click2Mail.

    The address list is formatted as an XML document that is sent in the body
    of a POST request to the Click2Mail API.

    Args:
        address_list_name (str): Name of the address list.
        address_list_mapping_id (str): Mapping ID for the address list.
        first_name (str): First name of the recipient.
        last_name (str): Last name of the recipient.
        organization (str): Organization name of the recipient.
        address_1 (str): Address line 1 of the recipient.
        address_2 (str): Address line 2 of the recipient.
        address_3 (str): Address line 3 of the recipient.
        city (str): City of the recipient.
        state (str): State of the recipient.
        postal_code (str): Postal code of the recipient.
        country (str): Country of the recipient.

    Returns:
        dict: Response containing status code, body, and headers.
    """
    # Construct the XML document
    body = (
        "<addressList>"
        "<addressListName>" + address_list_name + "</addressListName>"
        "<addressMappingId>" + address_list_mapping_id + "</addressMappingId>"
        "<addresses>"
        "<address>"
        "<Firstname>" + first_name + "</Firstname>"
        "<Lastname>" + last_name + "</Lastname>"
        "<Organization>" + organization + "</Organization>"
        "<Address1>" + address_1 + "</Address1>"
        "<Address2>" + address_2 + "</Address2>"
        "<Address3>" + address_3 + "</Address3>"
        "<City>" + city + "</City>"
        "<State>" + state + "</State>"
        "<Postalcode>" + postal_code + "</Postalcode>"
        "<Country>" + country + "</Country>"
        "</address>"
        "</addresses>"
        "</addressList>"
    )

    # Set the headers for the POST request
    headers = {"Accept": "application/xml", "Content-Type": "application/xml"}

    try:
        # Make the POST request
        response = requests.post(UPLOAD_ADDRESS_LIST_URL, data=body, headers=headers, auth=(USERNAME, PASSWORD))
        response.raise_for_status()  # Raise an exception for HTTP errors

        if response.status_code == 200:
            print_response("Upload address list call successful", response)

            # Parse the response XML to extract the address list ID
            xml_data = response.text
            root = ET.fromstring(xml_data)
            list_element = root.find("id")

            # Ensure the list element was found before trying to access its id
            if list_element is not None:
                address_list_id = list_element.text
                return {"statusCode": 200, "body": address_list_id, "headers": {"Content-Type": JSON_CONTENT_TYPE}}
            print_response("Upload address list call failed", response)
            return {"statusCode": 400, "body": response.text, "headers": {"Content-Type": JSON_CONTENT_TYPE}}
        print_response("Upload address list call failed", response)
        return {"statusCode": 400, "body": response.text, "headers": {"Content-Type": JSON_CONTENT_TYPE}}

    except requests.exceptions.RequestException as e:
        exception_string = f"Upload address list http request failed: {e}, {str(e)}"
        print_response(exception_string)
        return {"statusCode": 400, "body": str(e), "headers": {"Content-Type": JSON_CONTENT_TYPE}}
