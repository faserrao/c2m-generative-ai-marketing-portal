"""
Lambda that prompts Pinpoint to send a message based on channel
"""

#########################
#   LIBRARIES & LOGGER
#########################

import json
# import logging
import os
import sys
from datetime import datetime, timezone

import boto3
from botocore.exceptions import ClientError

import requests

submit_job_url          = "https://stage-rest.click2mail.com/molpro/jobs/"

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

def c2m_submit_job(billing_type: str = 'User Credit', job_id: str = ''):

  print('Entering c2m_submit_job()')
    
  # Define the endpoint to use, including the jobId

  url = submit_job_url + job_id + "/submit"

  headers = {'user-agent': 'my-app/0.0.1'}

  # Set the source of payment for the job
  values = {'billingType': billing_type}

  # Make the POST call
  r = requests.post(url, data=values, headers=headers, auth=(myusername, mypassword))

  # Display the result - a success should return status_code 201
  print('r.status_code = ')
  print(r.status_code)

  # Display the full XML returned.
  print('r.text = ' + r.text)

  print('Exiting c2m_submit_job()')

  return(r.text)