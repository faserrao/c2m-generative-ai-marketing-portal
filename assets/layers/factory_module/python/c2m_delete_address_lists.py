import logging
import sys
import requests

from print_response import print_response

# Define the base URL for deletion
base_url = "https://stage-rest.click2mail.com/molpro/addressLists"

# Setup logging
LOGGER = logging.getLogger("Content-generation")
LOGGER.setLevel(logging.INFO)
HANDLER = logging.StreamHandler(sys.stdout)
HANDLER.setFormatter(logging.Formatter("%(levelname)s | %(name)s | %(message)s"))
LOGGER.addHandler(HANDLER)

# Define credentials
myusername = 'stellario'
mypassword = 'Babushka1!'

def c2m_delete_address_lists(address_list_ids: list):
    headers = {"accept": "application/json"}

    for address_list_id in address_list_ids:
        url = f"{base_url}/{address_list_id}"
        LOGGER.info(f"Attempting to delete address list with ID: {address_list_id}")
        print(f"Attempting to delete address list with ID: {address_list_id}")

        try:
            response = requests.delete(url, headers=headers, auth=(myusername, mypassword))

            if response.status_code == 400:
                error_message = f"Base address list with id {address_list_id} does not belong to this user."
                print(error_message)
                LOGGER.error(error_message)
                return {
                "statusCode": 400,
                "body": response.text,
                "headers": {"Content-Type": "application/json"}
                }
            elif response.status_code == 200:
                info_message = f"Successfully deleted address list {address_list_id} with status code: {response.status_code}"
                LOGGER.info(info_message)
                print(info_message)
                continue
            else:
                warning_message = f"Unexpected status code {response.status_code} for address list {address_list_id}"
                LOGGER.warning(warning_message)
                print(warning_message)
                return {
                "statusCode": 400,
                "body": response.text,
                "headers": {"Content-Type": "application/json"}
                }

        except requests.exceptions.RequestException as e:
            error_message = f"Failed to delete address list {address_list_id}: {e}"
            LOGGER.error(error_message)
            print(error_message)
            return {
            "statusCode": 400,
            "body": response.text,
            "headers": {"Content-Type": "application/json"}
            }

    info_message = f"Successfully deleted all address lists"
    LOGGER.info(info_message)
    print(info_message)
    return {
    "statusCode": 200,
    "body": response.text,
    "headers": {"Content-Type": "application/json"}
    }