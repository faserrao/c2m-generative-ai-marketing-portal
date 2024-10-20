"""
This type stub file was generated by pyright.
"""

from typing import Optional
from sagemaker.session import Session

"""Functions for generating ECR image URIs for pre-built SageMaker Docker images."""
def get_huggingface_llm_image_uri(backend: str, session: Optional[Session] = ..., region: Optional[str] = ..., version: Optional[str] = ...) -> str:
    """Retrieves the image URI for inference.

    Args:
        backend (str): The backend to use. Valid values include "huggingface" and "lmi".
        session (Session): The SageMaker Session to use. (Default: None).
        region (str): The AWS region to use for image URI. (default: None).
        version (str): The framework version for which to retrieve an
            image URI. If no version is set, defaults to latest version. (default: None).

    Returns:
        str: The image URI string.
    """
    ...

