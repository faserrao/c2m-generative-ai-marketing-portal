"""
Lambda that prompts Pinpoint to send a message based on channel
"""

#########################
#   LIBRARIES & LOGGER
#########################


import requests
from print_response import print_response

purchase_url = "https://stage-rest.click2mail.com/molpro/credit/purchase"

# Define credentials
myusername = "stellario"
mypassword = "Babushka1!"

#########################
#        HANDLER
#########################


def c2m_add_credit(
    billing_name: str = None,
    billing_address1: str = None,
    billing_city: str = None,
    billing_state: str = None,
    billing_zip: str = None,
    billing_amount: str = None,
    billing_number: str = None,
    billing_month: str = None,
    billing_year: str = None,
    billing_cvv: str = None,
    billing_cc_type: str = None,
):

    # Set up parameters foresponse calling the endpoint
    data = {
        "billingName": billing_name,
        "billingAddress1": billing_address1,
        "billingCity": billing_city,
        "billingState": billing_state,
        "billingZip": billing_zip,
        "billingAmount": billing_amount,
        "billingNumber": billing_number,
        "billingMonth": billing_month,
        "billingYear": billing_year,
        "billingCvv": billing_cvv,
        "billingCcType": billing_cc_type,
    }

    try:
        response = requests.post(purchase_url, auth=(myusername, mypassword), data=data)
        response.raise_for_status()  # Raise an exception foresponse HTTP errors
        print_response("Add credit call successful", response)
        if response.status_code == 200:
            return {"statusCode": 200, "body": response.text, "headers": {"Content-Type": "application/json"}}
        print_response("Add credit call failed", response)
        return {"statusCode": 400, "body": response.text, "headers": {"Content-Type": "application/json"}}
    except requests.exceptions.RequestException as e:
        exception_string = f"Add credit http request failed: {e}, {str(e)}"
        print_response(exception_string)
        return {"statusCode": 400, "body": str(e), "headers": {"Content-Type": "application/json"}}
