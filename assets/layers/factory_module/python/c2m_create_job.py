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

from print_response import print_response

create_job_url          = "https://stage-rest.click2mail.com/molpro/jobs"

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


def c2m_create_job(document_class:    str = 'Letter 8.5 x 11',
                   layout:            str = 'Address on Separate Page',
                   production_time:   str = 'Next Day',
                   envelope:          str = '#10 Double Window',
                   color:             str = 'Black and White',
                   paper_type:        str = 'White 24#',
                   print_option:      str = 'Printing One side',
                   document_id:       str = None,
                   address_list_id:   str = None):

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
    r = requests.post(create_job_url, data=values, headers=headers, auth=(myusername, mypassword))
    r.raise_for_status()
    print_response('c2m_create_job', 'The response is:', r)
    print(f"c2m_create_job(): status_code = {r.status_code}")
    if (r.status_code == 201):
      xml_data = r.text
      logging.info(f"xml_data = {xml_data}")
      print(f"xml_data = {xml_data}")

      root = ET.fromstring(xml_data)

      # Directly find the <id> element within the xml
      id_element = root.find('id')

      if id_element is not None:
        job_id = id_element.text
        print(f"c2m_upload_document():document_id = {job_id}")
        logging.info(f"c2m_upload_document():document_id = {job_id}")
        return {
          "statusCode": 200,
          "body": job_id,
          "headers": {"Content-Type": "application/json"}
        }
      else:
        print(f"c2m_create_job():Create job call failed: {r.status_code}, {r.text}")
        logging.error(f"c2m_create_job():Create job call failed: {r.status_code}, {r.text}")
        return {
          "statusCode": 400,
          "body": r.text,
          "headers": {"Content-Type": "application/json"}
        }
  except requests.exceptions.RequestException as e:
    # Log the error for debugging
    print(f"c2m_create_job():Create job http request failed: {e}")
    logging.error(f"c2m_create_job():Create job http request failed: {e}")
    return {
      "statusCode": 400,
      "body": str(e),
      "headers": {
      "Content-Type": "application/json"
      }
    }