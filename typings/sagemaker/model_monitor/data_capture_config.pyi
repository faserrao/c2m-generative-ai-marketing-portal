"""
This type stub file was generated by pyright.
"""

"""
This type stub file was generated by pyright.
"""
_MODEL_MONITOR_S3_PATH = ...
_DATA_CAPTURE_S3_PATH = ...
class DataCaptureConfig:
    """Configuration object passed in when deploying models to Amazon SageMaker Endpoints.

    This object specifies configuration related to endpoint data capture for use with
    Amazon SageMaker Model Monitoring.
    """
    API_MAPPING = ...
    def __init__(self, enable_capture, sampling_percentage=..., destination_s3_uri=..., kms_key_id=..., capture_options=..., csv_content_types=..., json_content_types=..., sagemaker_session=...) -> None:
        """Initialize a DataCaptureConfig object for capturing data from Amazon SageMaker Endpoints.

        Args:
            enable_capture (bool): Required. Whether data capture should be enabled or not.
            sampling_percentage (int): Optional. Default=20. The percentage of data to sample.
                Must be between 0 and 100.
            destination_s3_uri (str): Optional. Defaults to "s3://<default-session-bucket>/
                model-monitor/data-capture".
            kms_key_id (str): Optional. Default=None. The kms key to use when writing to S3.
            capture_options ([str]): Optional. Must be a list containing any combination of the
                following values: "REQUEST", "RESPONSE". Default=["REQUEST", "RESPONSE"]. Denotes
                which data to capture between request and response.
            csv_content_types ([str]): Optional. Default=["text/csv"].
            json_content_types([str]): Optional. Default=["application/json"].
            sagemaker_session (sagemaker.session.Session): A SageMaker Session
                object, used for SageMaker interactions (default: None). If not
                specified, one is created using the default AWS configuration
                chain.
        """
        ...
    


