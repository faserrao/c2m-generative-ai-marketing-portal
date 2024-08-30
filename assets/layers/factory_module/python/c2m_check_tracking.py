"""
Lambda that prompts Pinpoint to send a message based on channel
"""

#########################
#   LIBRARIES & LOGGER
#########################

import logging
import sys

from botocore.exceptions import ClientError

import requests

check_tracking_url      = "https://stage-rest.click2mail.com/molpro/jobs/"

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

def c2m_check_tracking(tracking_type: str = 'IMB', job_id: str = ''):

  headers = {'user-agent': 'my-app/0.0.1'}
  tracking_type = tracking_type
  url = check_tracking_url + job_id + "/tracking?tracking_type=" + tracking_type

  try:
    r = requests.get(url, headers=headers, auth=(myusername, mypassword))
    r.raise_for_status()  # Raise an exception for HTTP errors
    if (r.status_code == 200):
      return {
        "statusCode": 200,
        "body": r.text,
        "headers": {"Content-Type": "application/json"}
      }
    else:
      print(f"Check tracking call failed: {r.status_code}, {r.text}")
      logging.error(f"Check tracking call failed: {r.status_code}, {r.text}")
      return {
        "statusCode": 400,
        "body": r.text,
        "headers": {"Content-Type": "application/json"
      }
    }
  except requests.exceptions.RequestException as e:
    # Log the error for debugging
    print(f"Check tracking http request failed: {e}")
    logging.error(f"Check tracking http request failed: {e}")
    return {
      "statusCode": 400,
      "body": str(e),
      "headers": {
      "Content-Type": "application/json"
      }
    }