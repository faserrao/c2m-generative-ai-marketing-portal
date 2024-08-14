"""
Lambda that prompts Pinpoint to send a message based on channel
"""

#########################
#   LIBRARIES & LOGGER
#########################

import json
#import logging
import os
import sys
from datetime import datetime, timezone

import boto3
from botocore.exceptions import ClientError

import requests

check_job_status_url    = "https://stage-rest.click2mail.com/molpro/jobs/"

"""
LOGGER = logging.Logger("Content-generation", level=logging.DEBUG)
HANDLER = logging.StreamHandler(sys.stdout)
HANDLER.setFormatter(logging.Formatter("%(levelname)s | %(name)s | %(message)s"))
LOGGER.addHandler(HANDLER)
"""

# Define credentials
myusername = 'stellario'
mypassword = 'Babushka1!'

#########################
#        HANDLER
#########################

def c2m_check_job_status(job_id: str = None):

  print('Entering c2m_check_job_status()')

  # Define the endpoint to use, including the jobId
  url = check_job_status_url + job_id 

  headers = {'user-agent': 'my-app/0.0.1'}

  # Make the GET call
  r = requests.get(url, headers=headers, auth=(myusername, mypassword))

  # Display the result - a success should return an HTTP status_code 201
  print('r.status_code = ')
  print(r.status_code)

  # Display the full XML returned.
  print('r.text = ' + r.text)

  print('Exiting c2m_check_job_status()')

  return r.text