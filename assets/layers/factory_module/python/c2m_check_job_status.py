"""
Lambda that prompts Pinpoint to send a message based on channel
"""

#########################
#   LIBRARIES & LOGGER
#########################

import logging
import sys

import requests

from print_response import print_response

check_job_status_url    = "https://stage-rest.click2mail.com/molpro/jobs/"

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

def c2m_check_job_status(job_id: str = None):

  url = check_job_status_url + job_id 
  headers = {'user-agent': 'my-app/0.0.1'}

  try:
    r = requests.get(url, headers=headers, auth=(myusername, mypassword))
    r.raise_for_status()  # Raise an exception for HTTP errors
    if (r.status_code == 201):
      return {
        "statusCode": 200,
        "body": r.text,
        "headers": {"Content-Type": "application/json"}
      }
    else:
      print(f"c2m_check_job_status():Check job status call failed: {r.status_code}, {r.text}")
      logging.error(f"c2m_check_job_status():Check job status call failed: {r.status_code}, {r.text}")
      return {
        "statusCode": 400,
        "body": r.text,
        "headers": {"Content-Type": "application/json"
      }
    }
  except requests.exceptions.RequestException as e:
    # Log the error for debugging
    print(f"c2m_check_job_status():Check job status http request failed: {e}")
    logging.error(f"c2m_check_job_status():Check job status http request failed: {e}")
    return {
      "statusCode": 400,
      "body": str(e),
      "headers": {
      "Content-Type": "application/json"
      }
    }