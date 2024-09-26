import logging
import sys

import requests

# Define constants
DELETE_ADDRESS_LIST_URL = "https://stage-rest.click2mail.com/molpro/addressLists"
JSON_CONTENT_TYPE = "application/json"

# Setup logging
LOGGER = logging.getLogger("Content-generation")
LOGGER.setLevel(logging.INFO)
HANDLER = logging.StreamHandler(sys.stdout)
HANDLER.setFormatter(logging.Formatter("%(levelname)s | %(name)s | %(message)s"))
LOGGER.addHandler(HANDLER)

# Define credentials
MY_USERNAME = "stellario"
MY_PASSWORD = "Babushka1!"


def c2m_delete_address_lists(address_list_ids: list):
    """Delete address lists from Click2Mail using provided IDs."""
    headers = {"accept": JSON_CONTENT_TYPE}

    for address_list_id in address_list_ids:
        url = f"{DELETE_ADDRESS_LIST_URL}/{address_list_id}"
        LOGGER.info("Attempting to delete address list with ID: %s", address_list_id)
        print(f"Attempting to delete address list with ID: {address_list_id}")

        try:
            response = requests.delete(url, headers=headers, auth=(MY_USERNAME, MY_PASSWORD))

            if response.status_code == 400:
                error_message = f"Base address list with id {address_list_id} does not belong to this user."
                print(error_message)
                LOGGER.error(error_message)
                return {"statusCode": 400, "body": response.text, "headers": {"Content-Type": JSON_CONTENT_TYPE}}
            if response.status_code == 200:
                info_message = (
                    f"Successfully deleted address list {address_list_id} with status code: {response.status_code}"
                )
                LOGGER.info(info_message)
                print(info_message)
                continue
            warning_message = f"Unexpected status code {response.status_code} for address list {address_list_id}"
            LOGGER.warning(warning_message)
            print(warning_message)
            return {"statusCode": 400, "body": response.text, "headers": {"Content-Type": JSON_CONTENT_TYPE}}

        except requests.exceptions.RequestException as e:
            error_message = f"Failed to delete address list {address_list_id}: {e}"
            LOGGER.error(error_message)
            print(error_message)
            return {"statusCode": 400, "body": response.text, "headers": {"Content-Type": JSON_CONTENT_TYPE}}

    info_message = "Successfully deleted all address lists"
    LOGGER.info(info_message)
    print(info_message)
    return {"statusCode": 200, "body": response.text, "headers": {"Content-Type": JSON_CONTENT_TYPE}}
