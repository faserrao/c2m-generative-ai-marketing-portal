"""This module contains utility functions for SageMaker Endpoints."""
from sagemaker.utils import sagemaker_timestamp

from infra.constructs.llm_endpoints.constants import NAME_SEPARATOR

MAX_RESOURCE_NAME_LENGTH = 63


def create_resource_name(base_name: str) -> str:
    """Creates a SageMaker resource name by prepending a base name with a
    timestamp.

    The base name is truncated to ensure the total length of the resource name does
    not exceed MAX_RESOURCE_NAME_LENGTH. The timestamp is appended to the base
    name with a hyphen separator.

    Parameters
    ----------
    base_name : str
        The base name to prepend the timestamp to.

    Returns
    -------
    str
        The resource name.
    """
    ts = sagemaker_timestamp()
    max_base_length = MAX_RESOURCE_NAME_LENGTH - len(ts) - 1
    return NAME_SEPARATOR.join([base_name[:max_base_length], ts])
