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

upload_address_list_url = "https://stage-rest.click2mail.com/molpro/addressLists"

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
):

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

    headers = {"Accept": "application/xml", "Content-Type": "application/xml"}

    try:
        response = requests.post(upload_address_list_url, data=body, headers=headers, auth=(myusername, mypassword))
        response.raise_for_status()  # Raise an exception for HTTP errors

        if response.status_code == 200:
            print_response("Upload address list call successful", response)

            xml_data = response.text
            root = ET.fromstring(xml_data)
            list_element = root.find("id")

            # Ensure the list element was found before trying to access its id
            if list_element is not None:
                address_list_id = list_element.text
                return {"statusCode": 200, "body": address_list_id, "headers": {"Content-Type": "application/json"}}
            print_response("Upload address list call failed", response)
            return {"statusCode": 400, "body": response.text, "headers": {"Content-Type": "application/json"}}
        print_response("Upload address list call failed", response)
        return {"statusCode": 400, "body": response.text, "headers": {"Content-Type": "application/json"}}

    except requests.exceptions.RequestException as e:
        exception_string = f"Upload address list http request failed: {e}, {str(e)}"
        print_response(exception_string)
        return {"statusCode": 400, "body": str(e), "headers": {"Content-Type": "application/json"}}
