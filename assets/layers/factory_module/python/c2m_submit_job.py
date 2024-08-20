"""
Lambda that prompts Pinpoint to send a message based on channel
"""

#########################
#   LIBRARIES & LOGGER
#########################

import logging
from datetime import datetime, timezone
import sys
import requests

submit_job_url          = "https://stage-rest.click2mail.com/molpro/jobs/"

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

def c2m_submit_job(billing_type: str = 'User Credit', job_id: str = ''):

  url = submit_job_url + job_id + "/submit"
  headers = {'user-agent': 'my-app/0.0.1'}
  values = {'billingType': billing_type}

  try:
    r = requests.post(url, data=values, headers=headers, auth=(myusername, mypassword))
    r.raise_for_status()  # Raise an exception for HTTP errors
    return {
      "statusCode": r.status_code,
      "body": r.text,
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