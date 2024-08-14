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
from io import BytesIO
import xml.etree.ElementTree as ET

import boto3
from botocore.exceptions import ClientError

from requests_toolbelt.multipart.encoder import MultipartEncoder
import requests

purchase_url            = "https://stage-rest.click2mail.com/molpro/credit/purchase"

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


def c2m_add_credit(billing_name: str = None,
                   billing_address1: str = None, 
 				  			   billing_city: str = None, 
							  	 billing_state: str = None,
							  	 billing_zip: str = None,
				  				 billing_amount: str = None, 
							  	 billing_number: str = None, 
							  	 billing_month: str = None, 
							  	 billing_year: str = None, 
							  	 billing_cvv: str = None, 
							  	 billing_cc_type: str = None):

  print('Entering c2m_add_credit')

  # Set up parameters for calling the endpoint
  data = {'billingName' : billing_name,
          'billingAddress1' :billing_address1,
          'billingCity' : billing_city,
          'billingState' : billing_state,
          'billingZip' : billing_zip,
          'billingAmount' : billing_amount,
          'billingNumber' : billing_number,
          'billingMonth' : billing_month,
          'billingYear' : billing_year,
          'billingCvv' : billing_cvv,
          'billingCcType' : billing_cc_type 
        }

  # Make the POST call
  r = requests.post(purchase_url, auth=(myusername, mypassword), data=data)
  print('After post in add credit')

  # Display the result - a success should return status_code 200
  print('r.status_code = ')
  print(r.status_code)

  # Display the full XML returned.
  print('r.text = ' + r.text)

  print('Exiting c2m_add_credit')

  return r.text