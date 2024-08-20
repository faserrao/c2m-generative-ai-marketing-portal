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

upload_doc_url          = "https://stage-rest.click2mail.com/molpro/documents"

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
    r = requests.post(upload_doc_url, auth=(myusername, mypassword), headers=headers, data=mp_encoder)
    r.raise_for_status()  # Raise an exception for HTTP errors
    xml_data = r.text
    root = ET.fromstring(xml_data)
    document_id = root.find('id').text
    return {
      "statusCode": r.status_code,
      "body": document_id,
      "headers": {
        "Content-Type": "application/json"
      }
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