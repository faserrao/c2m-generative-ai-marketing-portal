import os


def get_channel_states():
    """Return a dictionary of channel states based on environment variables."""
    return {
        "EMAIL": os.environ.get("EMAIL_ENABLED", "true").lower(),
        "SMS": os.environ.get("SMS_ENABLED", "true").lower(),
        "CUSTOM": os.environ.get("CUSTOM_ENABLED", "true").lower(),
    }
