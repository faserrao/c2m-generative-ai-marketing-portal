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
from print_response import print_response

upload_address_list_url = "https://stage-rest.click2mail.com/molpro/addressLists"

LOGGER = logging.Logger("Content-generation", level=logging.INFO)
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

  print(f"c2m_upload_address_list():address_list_name = {address_list_name}")
  logging.info(f"c2m_upload_address_list():address_list_name = {address_list_name}")

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

  print(f"c2m_upload_address_list():body = {body}")
  logging.info(f"c2m_upload_address_list():body = {body}")

  headers = { "Accept": "application/xml", "Content-Type": "application/xml" }

  try:
    r = requests.post(upload_address_list_url, data=body, headers=headers, auth=(myusername, mypassword))
    print_response('c2m_upload_address_list', 'The response is', r)

    r.raise_for_status()  # Raise an exception for HTTP errors

    print(f"c2m_upload_address_list():Upload Address List r: {r}")
    logging.info(f"c2m_upload_address_list():Upload Address List status_code: {r.status_code}")
    print(f"c2m_upload_address_list():Upload Address List status_code: {r.status_code}")

    if (r.status_code == 200):
      xml_data = r.text
      print(f"c2m_upload_address_list():xml_data = {xml_data}")
      logging.info(f"c2m_upload_address_list():Upload Address List xml_data: {xml_data}")

      root = ET.fromstring(xml_data)

      # Find the specific list element by name
      # Dont need the .// anymore - Use the old code
      # list_element = root.find(f".//list[name='{address_list_name}']")

      list_element = root.find('id')

      # Ensure the list element was found before trying to access its id
      if list_element is not None:
        address_list_id = list_element.text
        print(f"c2m_upload_address_list():Address List ID: {address_list_id}")
        logging.info(f"c2m_upload_address_list():Address List ID: {address_list_id}")
        return {
          "statusCode": 200,
          "body": address_list_id,
          "headers": {"Content-Type": "application/json"}
        }
      else:
        print(f"c2m_upload_address_list():Upload address list call failed: {r.status_code}, {r.text}")
        logging.error(f"c2m_upload_address_list():Upload address list call failed: {r.status_code}, {r.text}")
        return {
          "statusCode": 400,
          "body": r.text,
          "headers": {"Content-Type": "application/json"}
        }
    else:
      print(f"c2m_upload_address_list():Upload address list call failed: {r.status_code}, {r.text}")
      logging.error(f"c2m_upload_address_list():Upload address list call failed: {r.status_code}, {r.text}")
      return {
        "statusCode": 400,
        "body": r.text,
        "headers": {"Content-Type": "application/json"}
      }

  except requests.exceptions.RequestException as e:
    print(f"c2m_upload_address_list():Upload address list http request failed: {e}")
    logging.error(f"c2m_upload_address_list():Upload address list http request failed: {e}")
    return {
      "statusCode": 400,
      "body": str(e),
      "headers": {
      "Content-Type": "application/json"
      }
    }