"""
Lambda that prompts Pinpoint to send a message based on channel
"""

#########################
#   LIBRARIES & LOGGER
#########################

import logging
import sys

import requests
import xml.etree.ElementTree as ET

create_job_url          = "https://stage-rest.click2mail.com/molpro/jobs"

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


def c2m_create_job(document_class:    str = 'Letter 8.5 x 11',
                   layout:            str = 'Address on Separate Page',
                   production_time:   str = 'Next Day',
                   envelope:          str = '#10 Double Window',
                   color:             str = 'Black and White',
                   paper_type:        str = 'White 24#',
                   print_option:      str = 'Printing One side',
                   document_id:       str = None,
                   address_list_id:   str = None):

  url = create_job_url
  headers = {'user-agent': 'my-app/0.0.1'}
  values = {'documentClass' : document_class,
            'layout'        : layout,
            'productionTime': production_time,
            'envelope'      : envelope,
            'color'         : color,
            'paperType'     : paper_type,
            'printOption'   : print_option,
            'documentId'    : document_id,
            'addressId'     : address_list_id}

  try:
    r = requests.post(url, data=values, headers=headers, auth=(myusername, mypassword))
    r.raise_for_status()  # Raise an exception for HTTP errors
    xml_data = r.text
    root = ET.fromstring(xml_data)
    job_id = root.find('id').text
    return {
      "statusCode": r.status_code,
      "body": job_id,
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