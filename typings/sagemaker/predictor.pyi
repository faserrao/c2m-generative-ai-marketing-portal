"""
This type stub file was generated by pyright.
"""

from typing import Optional
from sagemaker.session import Session
from sagemaker.base_predictor import Predictor

"""
This type stub file was generated by pyright.
"""
def retrieve_default(endpoint_name: str, sagemaker_session: Session = ..., region: Optional[str] = ..., model_id: Optional[str] = ..., model_version: Optional[str] = ..., tolerate_vulnerable_model: bool = ..., tolerate_deprecated_model: bool = ...) -> Predictor:
    """Retrieves the default predictor for the model matching the given arguments.

    Args:
        endpoint_name (str): Endpoint name for which to create a predictor.
        sagemaker_session (Session): The SageMaker Session to attach to the Predictor.
            (Default: sagemaker.jumpstart.constants.DEFAULT_JUMPSTART_SAGEMAKER_SESSION).
        region (str): The AWS Region for which to retrieve the default predictor.
            (Default: None).
        model_id (str): The model ID of the model for which to
            retrieve the default predictor. (Default: None).
        model_version (str): The version of the model for which to retrieve the
            default predictor. (Default: None).
        tolerate_vulnerable_model (bool): True if vulnerable versions of model
            specifications should be tolerated (exception not raised). If False, raises an
            exception if the script used by this version of the model has dependencies with known
            security vulnerabilities. (Default: False).
        tolerate_deprecated_model (bool): True if deprecated models should be tolerated
            (exception not raised). False if these models should raise an exception.
            (Default: False).
    Returns:
        Predictor: The default predictor to use for the model.

    Raises:
        ValueError: If the combination of arguments specified is not supported.
    """
    ...

