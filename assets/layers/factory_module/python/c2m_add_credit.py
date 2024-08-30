"""
Lambda that prompts Pinpoint to send a message based on channel
"""

#########################
#   LIBRARIES & LOGGER
#########################

import json
import logging
import sys
import xml.etree.ElementTree as ET
from botocore.exceptions import ClientError
from requests_toolbelt.multipart.encoder import MultipartEncoder
import requests

purchase_url            = "https://stage-rest.click2mail.com/molpro/credit/purchase"

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

  try:
      r = requests.post(purchase_url, auth=(myusername, mypassword), data=data)
      r.raise_for_status()  # Raise an exception for HTTP errors
      if (r.status_code == 200):
        return {
          "statusCode": 200,
          "body": r.text,
          "headers": {"Content-Type": "application/json"}
        }
      else:
        print(f"c2m_add_credit():Add credit call failed: {r.status_code}, {r.text}")
        logging.error(f"c2m_add_credit():Add credit call failed: {r.status_code}, {r.text}")
        return {
          "statusCode": 400,
          "body": r.text,
          "headers": {"Content-Type": "application/json"
        }
      }
  except requests.exceptions.RequestException as e:
      # Log the error for debugging
      print(f"c2m_add_credit():Add credit http request failed: {e}, {str(e)}")
      logging.error(f"c2m_add_credit():Add credit http request failed: {e}, {str(e)}")
      return {
          "statusCode": 400,
          "body": str(e),
          "headers": {"Content-Type": "application/json"}
      }