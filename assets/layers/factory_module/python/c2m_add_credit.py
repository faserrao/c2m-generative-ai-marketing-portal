"""Lambda that prompts Pinpoint to send a message based on channel."""

#########################
#   LIBRARIES & LOGGER
#########################


import requests
from print_response import print_response

CONTENT_TYPE_JSON = "application/json"

PURCHASE_URL = "https://stage-rest.click2mail.com/molpro/credit/purchase"

# Define credentials
MY_USERNAME = "stellario"
MY_PASSWORD = "Babushka1!"

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
    """
    Add credit to Click2Mail account using provided billing information.
    Args:
        :param billing_name: Name on the billing account
        :param billing_address1: Billing address line 1
        :param billing_city: Billing city
        :param billing_state: Billing state
        :param billing_zip: Billing ZIP code
        :param billing_amount: Amount to add to the account
        :param billing_number: Credit card number
        :param billing_month: Credit card expiration month
        :param billing_year: Credit card expiration year
        :param billing_cvv: Credit card CVV
        :param billing_cc_type: Credit card type
    Returns:
        Dict with status code, response body, and headers
    """
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
        response = requests.post(PURCHASE_URL, auth=(MY_USERNAME, MY_PASSWORD), data=data)
        response.raise_for_status()  # Raise an exception for HTTP errors
        print_response("Add credit call successful", response)
        if response.status_code == 200:
            return {"statusCode": 200, "body": response.text, "headers": {"Content-Type": CONTENT_TYPE_JSON}}
        print_response("Add credit call failed", response)
        return {"statusCode": 400, "body": response.text, "headers": {"Content-Type": CONTENT_TYPE_JSON}}
    except requests.exceptions.RequestException as e:
        exception_string = f"Add credit http request failed: {e}, {str(e)}"
        print_response(exception_string)
        return {"statusCode": 400, "body": str(e), "headers": {"Content-Type": CONTENT_TYPE_JSON}}
