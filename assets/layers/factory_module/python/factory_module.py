import logging
from abc import ABC, abstractmethod
import os
import sys
import random
import string
import c2m_add_credit
import c2m_check_job_status
import c2m_create_job
import c2m_submit_job
import c2m_upload_address_list
import c2m_upload_document
from channel_states import get_channel_states

LOGGER = logging.Logger("Content-generation", level=logging.INFO)
HANDLER = logging.StreamHandler(sys.stdout)
HANDLER.setFormatter(logging.Formatter("%(levelname)s | %(name)s | %(message)s"))
LOGGER.addHandler(HANDLER)

# Define credentials
myusername = 'stellario'
mypassword = 'Babushka1!'

def parse_custom_address(address: str):
    address_1, city, state, postal_code = address.split('%')
    address_object = {"address_1": address_1,
                      "city": city,
                      "state": state,
                      "postal_code": postal_code}
    print(address_object)
    return address_object


def generate_unique_name(length=8):

    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(length))


class MessageConfigFactory(ABC):
    @abstractmethod
    def create_message_request(self, address, message_subject, message_body_html, message_body_text):
        pass


class EmailMessageConfig(MessageConfigFactory):
    def create_message_request(self, address, message_subject, message_body_html, message_body_text):
        return {
            "Addresses": {address: {"ChannelType": "EMAIL"}},
            "MessageConfiguration": {
                "EmailMessage": {
                    "FromAddress": os.environ["EMAIL_IDENTITY"],
                    "SimpleEmail": {
                        "Subject": {"Charset": "UTF-8", "Data": message_subject},
                        "HtmlPart": {"Charset": "UTF-8", "Data": message_body_html},
                        "TextPart": {"Charset": "UTF-8", "Data": message_body_text},
                    },
                }
            }
        }


class SMSMessageConfig(MessageConfigFactory):
    def create_message_request(self, address, message_subject, message_body_html, message_body_text):
        sms_config = {
            "Body": message_body_text,
            "MessageType": "PROMOTIONAL"
        }
        if os.environ["SMS_IDENTITY"]:
            sms_config["OriginationNumber"] = os.environ["SMS_IDENTITY"]

        return {
            "Addresses": {address: {"ChannelType": "SMS"}},
            "MessageConfiguration": {"SMSMessage": sms_config}
        }

# TODO: Check that all status codes being checked are correct
class CustomMessageConfig(MessageConfigFactory):

    def create_message_request(self, address, message_subject, message_body_html, message_body_text):

        print('CustomMessageConfig.create_message_request():message_body_text = ', message_body_text)

        response = c2m_add_credit.c2m_add_credit(billing_name = 'Awesome User',
                                            billing_address1 = '221B Baker St',
                                            billing_city = 'Springfield',
                                            billing_state = 'MO',
                                            billing_zip = '34567',
                                            billing_amount = '10',
                                            billing_number = '4111111111111111',
                                            billing_month = '12',
                                            billing_year = '2030',
                                            billing_cvv = '123',
                                            billing_cc_type = 'VI')
        if response["statusCode"] == 200:
            print(f"CustomMessageConfig.create_message_request():Credit applied successfully")
        else:
            print(f"CustomMessageConfig.create_message_request():Failed to apply credit. Error: {response['body']}")

        address_object = parse_custom_address(address)
        address_list_name = generate_unique_name()
        print("create_message_request():address_list_name = {address_list_name}")

        response = c2m_upload_address_list.c2m_upload_address_list(address_list_name = address_list_name,
                                                    address_list_mapping_id = '1',
                                                    organization = 'Justice League',
                                                    address_1 = address_object['address_1'],
                                                    city = address_object['city'],
                                                    state = address_object['state'],
                                                    postal_code = address_object['postal_code'],
                                                    country = 'USA')
        c2m_upload_address_list_status_code = response["statusCode"]
        print(f"CustomMessageConfig.create_message_request():c2m_upload_address_list_status_code = {c2m_upload_address_list_status_code }")
        if c2m_upload_address_list_status_code  == 200:
            address_list_id = response["body"]
            print(f"CustomMessageConfig.create_message_request():Address list uploaded successfully: address_list_id = {address_list_id}")
        else:
            print(f"CustomMessageConfig.create_message_request():Failed upload address list. Error: {response['body']}")

        document_name = generate_unique_name()
        print("create_message_request():document_name = {document_name}")

        response = c2m_upload_document.c2m_upload_document(
                                            document_name = document_name,
                                            document_content = message_body_text,
                                            document_class = 'Letter 8.5 x 11',
                                            document_type = 'application/odt',
                                            document_format = 'ODT')

        print('response["CustomMessageConfig.create_message_request():statusCode"] = ', response["statusCode"])
        if response["statusCode"] == 200:
            document_id = response["body"]
            print(f"CustomMessageConfig.create_message_request():Document uploaded successfully. Document ID: {document_id}")
        else:
            print(f"CustomMessageConfig.create_message_request():Failed to upload document. Error: {response['body']}")


        response = c2m_create_job.c2m_create_job(document_id = document_id, address_list_id = address_list_id)
        if response["statusCode"] == 200:
            job_id = response["body"]
            print(f"CustomMessageConfig.create_message_request():Job created successfully. Job ID: {job_id}")
        else:
            print(f"CustomMessageConfig.create_message_request():Failed to create job. Error: {response['body']}")


        response = c2m_submit_job.c2m_submit_job(billing_type = 'User Credit', job_id = job_id)
        if response["statusCode"] == 200:
            print(f"CustomMessageConfig.create_message_request():Job submitted successfully.")
        else:
            print(f"CustomMessageConfig.create_message_request():Failed to submit job. Error: {response['body']}")


        response = c2m_check_job_status.c2m_check_job_status(job_id = job_id)
        if response["statusCode"] == 200:
            print(f"CustomMessageConfig.create_message_request():Job status: {response['body']}")
        else:
            print(f"CustomMessageConfig.create_message_request():Failed to retrieve job status. Error: {response['body']}")

class MessageConfigFactoryCreator:
    @staticmethod
    def create_factory(channel):

        channel_states = get_channel_states()
        if channel_states.get(channel):
            if channel == "EMAIL":
                return EmailMessageConfig()
            elif channel == "SMS":
                return SMSMessageConfig()
            elif channel == "CUSTOM":
                return CustomMessageConfig()
        else:
            raise ValueError(f"Unsupported channel: {channel}")