
import logging
from abc import ABC, abstractmethod
import os
import sys
import c2m_add_credit
import c2m_check_job_status
import c2m_check_tracking
import c2m_create_job
import c2m_submit_job
import c2m_upload_address_list
import c2m_upload_document
from channel_states import get_channel_states

LOGGER = logging.Logger("Content-generation", level=logging.DEBUG)
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
        address_object = parse_custom_address(address)

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
            print(f"Credit applied successfully")
        else:
            print(f"Failed to apply credit. Error: {response['body']}")


        response = c2m_upload_document.c2m_upload_document(
                                            document_name = 'Test Document',
                                            document_content = message_body_text,
                                            document_class = 'Letter 8.5 x 11',
                                            document_type = 'application/odt',
                                            document_format = 'ODT')

        print('response["statusCode"] = ', response["statusCode"])
        if response["statusCode"] == 201:
            document_id = response["body"]
            print(f"Document uploaded successfully. Document ID: {document_id}")
        else:
            print(f"Failed to upload document. Error: {response['body']}")


        response = c2m_upload_address_list.c2m_upload_address_list(address_list_name = 'My First List',
                                                    address_list_mapping_id = '1',
                                                    organization = 'Justice League',
                                                    address_1 = address_object['address_1'],
                                                    city = address_object['city'],
                                                    state = address_object['state'],
                                                    postal_code = address_object['postal_code'],
                                                    country = 'USA')
        if response["statusCode"] == 200:
            address_list_id = response["body"]
            print(f"Address list uploaded successfully")
        else:
            print(f"Failed upload address list. Error: {response['body']}")


        response = c2m_create_job.c2m_create_job(document_id = document_id, address_list_id = address_list_id)
        if response["statusCode"] == 201:
            job_id = response["body"]
            print(f"Job created successfully. Job ID: {document_id}")
        else:
            print(f"Failed to create job. Error: {response['body']}")


        response = c2m_submit_job.c2m_submit_job(billing_type = 'User Credit', job_id = job_id)
        if response["statusCode"] == 200:
            print(f"Job submitted successfully.")
        else:
            print(f"Failed to submit job. Error: {response['body']}")


        response = c2m_check_job_status.c2m_check_job_status(job_id = job_id)
        if response["statusCode"] == 201:
            print(f"Job status: . {response['body']}")
        else:
            print(f"Failed to retrieve job status. Error: {response['body']}")


        """
        check_tracking_return = c2m_check_tracking.c2m_check_tracking(tracking_type = 'IMB', job_id = job_id)
        print(check_tracking_return)
        """

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