"""
Lambda that prompts Pinpoint to send a message based on channel
"""

#########################
#   LIBRARIES & LOGGER
#########################

import inspect
import logging
from io import BytesIO
import xml.etree.ElementTree as ET
import sys
from requests_toolbelt.multipart.encoder import MultipartEncoder
import requests
from odf.opendocument import OpenDocumentText
from odf.text import P
from print_response import print_response

upload_doc_url          = "https://stage-rest.click2mail.com/molpro/documents"

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

def c2m_upload_document(document_format:  str = 'ODT',
                        document_name:    str = 'Test Letter ODT',
                        document_class:   str = 'Letter 8.5 x 11',
                        document_content: str = None,
                        document_type:    str = 'application/odt'):

  odt_stream = string_to_odt_in_memory(document_content)
  mp_encoder = MultipartEncoder(
    fields={
      'documentFormat': document_format,
      'documentName': document_name,
      'documentClass': document_class,
      'file': ('file.odt', odt_stream, document_type)
    }
  )

  headers = {'user-agent': 'my-app/0.0.1','Content-Type': mp_encoder.content_type}

  try:
    r = requests.post(upload_doc_url, headers=headers, auth=(myusername, mypassword), data=mp_encoder)

    r.raise_for_status()  # Raise an exception for HTTP errors

    current_function_name = inspect.currentframe().f_code.co_name

    print_response(current_function_name, "response = ", r)
    print(f"c2m_upload_document():Upload Document call status_code: {r.status_code}")
    logging.info(f"c2m_upload_document():Upload Document call status_code: {r.status_code}")

    if (r.status_code == 201):
      xml_data = r.text
      logging.info(f"xml_data = {xml_data}")
      print(f"xml_data = {xml_data}")

      root = ET.fromstring(xml_data)

      # Directly find the <id> element within the <document>
      id_element = root.find('id')

      # Ensure the id element was found before trying to access its text
      if id_element is not None:
        document_id = id_element.text
        print(f"c2m_upload_document():document_id = {document_id}")
        logging.info(f"c2m_upload_document():document_id = {document_id}")
        return {
          "statusCode": 200,
          "body": document_id,
          "headers": {"Content-Type": "application/json"}
        }
      else:
        print(f"c2m_upload_document():No <id> element found in the XML.")
        logging.error(f"c2m_upload_document():No <id> element found in the XML.")
        return {
          "statusCode": 400,
          "body": "No <id> element found in the XML.",
          "headers": {"Content-Type": "application/json"}
        }
    else:
      print(f"fc2m_upload_document():Upload Document call failed: {r.status_code}, {r.text}")
      logging.error(f"c2m_upload_document():Upload Document call failed: {r.status_code}, {r.text}")
      return {
        "statusCode": 400,
        "body": r.text,
        "headers": {"Content-Type": "application/json"}
      }
  except requests.exceptions.RequestException as e:
    # Log the error for debugging
    print(f"c2m_upload_document():Upload Document http request failed: {e}")
    logging.error(f"c2m_upload_document():Upload Document http request failed: {e}")
    return {
      "statusCode": 400,
      "body": str(e),
      "headers": {
      "Content-Type": "application/json"
      }
    }