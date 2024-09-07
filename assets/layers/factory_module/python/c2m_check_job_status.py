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
    response = requests.get(url, headers=headers, auth=(myusername, mypassword))
    response.raise_for_status()  # Raise an exception for HTTP errors
    if (response.status_code == 201):
      print_response("Check job status call successful", response)
      return {
        "statusCode": 200,
        "body": response.text,
        "headers": {"Content-Type": "application/json"}
      }
    else:
      print_response("Add credit call failed", response)
      return {
        "statusCode": 400,
        "body": response.text,
        "headers": {"Content-Type": "application/json"
      }
    }
  except requests.exceptions.RequestException as e:
    exception_string = f"Add credit http request failed: {e}, {str(e)}"
    print_response(exception_string)
    return {
      "statusCode": 400,
      "body": str(e),
      "headers": {
      "Content-Type": "application/json"
      }
    }