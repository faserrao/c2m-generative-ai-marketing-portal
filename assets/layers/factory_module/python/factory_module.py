from abc import ABC, abstractmethod
import os

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


class CustomMessageConfig(MessageConfigFactory):
    def create_message_request(self, address, message_subject, message_body_html, message_body_text):
        # Custom logic for handling the CUSTOM channel, potentially using Click2Mail API
        address_object = parse_custom_address(address)
        # Further processing and return the appropriate request or output
        # This section would include all the calls to the Click2Mail API as before
        pass


class MessageConfigFactoryCreator:
    @staticmethod
    def create_factory(channel):
        # Fetch channel states from environment variables
        channel_states = {
            "EMAIL": os.environ.get("EMAIL_CHANNEL_ENABLED", "true").lower() == "true",
            "SMS": os.environ.get("SMS_CHANNEL_ENABLED", "true").lower() == "true",
            "CUSTOM": os.environ.get("CUSTOM_CHANNEL_ENABLED", "true").lower() == "true"
        }

        if channel_states.get(channel):
            if channel == "EMAIL":
                return EmailMessageConfig()
            elif channel == "SMS":
                return SMSMessageConfig()
            elif channel == "CUSTOM":
                return CustomMessageConfig()
        else:
            #raise ValueError(f"Unsupported channel: {channel}")
            raise ValueError(f"{channel} channel is turned off")
