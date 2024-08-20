"""
Lambda that prompts Pinpoint to send a message based on channel
"""

#########################
#   LIBRARIES & LOGGER
#########################

import logging
from io import BytesIO
import xml.etree.ElementTree as ET
import sys

from requests_toolbelt.multipart.encoder import MultipartEncoder
import requests
from odf.opendocument import OpenDocumentText
from odf.text import P

upload_address_list_url = "https://stage-rest.click2mail.com/molpro/addressLists"

LOGGER = logging.Logger("Content-generation", level=logging.DEBUG)
HANDLER = logging.StreamHandler(sys.stdout)
HANDLER.setFormatter(logging.Formatter("%(levelname)s | %(name)s | %(message)s"))
LOGGER.addHandler(HANDLER)

# Define credentials
myusername = 'stellario'
mypassword = 'Babushka1!'

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


def c2m_upload_address_list(address_list_name :       str = '',
                            address_list_mapping_id:  str = '',
                            first_name:               str = 'first_name',
                            last_name:                str = 'last_name',
                            organization:             str = '',
                            address_1:                str = '',
                            address_2:                str = '',
                            address_3:                str = '',
                            city:                     str = '',
                            state:                    str = '',
                            postal_code:              str = '',
                            country:                  str = ''):

  body = (
  '<addressList>'
    '<addressListName>' + address_list_name + '</addressListName>'
    '<addressMappingId>' + address_list_mapping_id + '</addressMappingId>'
    '<addresses>'
      '<address>'
          '<Firstname>' + first_name + '</Firstname>'
          '<Lastname>' + last_name + '</Lastname>'
          '<Organization>' + organization + '</Organization>'
          '<Address1>' + address_1 + '</Address1>'
          '<Address2>' + address_2 + '</Address2>'
          '<Address3>' + address_3 + '</Address3>'
          '<City>' + city + '</City>'
          '<State>' + state + '</State>'
          '<Postalcode>' + postal_code + '</Postalcode>'
          '<Country>' + country + '</Country>'
      '</address>'
    '</addresses>'
  '</addressList>'
  )

  url = upload_address_list_url
  headers = { "Accept": "application/xml", "Content-Type": "application/xml" }

  try:
    r = requests.post(url, data=body, headers=headers, auth=(myusername, mypassword))
    r.raise_for_status()  # Raise an exception for HTTP errors
    xml_data = r.text
    root = ET.fromstring(xml_data)
    address_list_id = root.find('id').text
    return {
      "statusCode": r.status_code,
      "body": address_list_id,
      "headers": {"Content-Type": "application/json"}
    }
  except requests.exceptions.RequestException as e:
    # Log the error for debugging
    logging.error(f"Request failed: {e}")
    return {
      "statusCode": 400,
      "body": str(e),
      "headers": {
      "Content-Type": "application/json"
      }
    }
