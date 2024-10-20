"""
This type stub file was generated by pyright.
"""

from typing import List

"""
This type stub file was generated by pyright.
"""
logger = ...
_APP_NAME = ...
_CONFIG_FILE_NAME = ...
_DEFAULT_ADMIN_CONFIG_FILE_PATH = ...
_DEFAULT_USER_CONFIG_FILE_PATH = ...
_DEFAULT_LOCAL_MODE_CONFIG_FILE_PATH = ...
ENV_VARIABLE_ADMIN_CONFIG_OVERRIDE = ...
ENV_VARIABLE_USER_CONFIG_OVERRIDE = ...
S3_PREFIX = ...
def load_sagemaker_config(additional_config_paths: List[str] = ..., s3_resource=...) -> dict:
    """Loads config files and merges them.

    By default, this method first searches for config files in the default locations
    defined by the SDK.

    Users can override the default admin and user config file paths using the
    ``SAGEMAKER_ADMIN_CONFIG_OVERRIDE`` and ``SAGEMAKER_USER_CONFIG_OVERRIDE`` environment
    variables, respectively.

    Additional config file paths can also be provided as a parameter.

    This method then:
        * Loads each config file, whether it is Amazon S3 or the local file system.
        * Validates the schema of the config files.
        * Merges the files in the same order.

    This method throws exceptions in the following cases:
        * ``jsonschema.exceptions.ValidationError``: Schema validation fails for one or more
          config files.
        * ``RuntimeError``: The method is unable to retrieve the list of all S3 files with the
          same prefix or is unable to retrieve the file.
        * ``ValueError``: There are no S3 files with the prefix when an S3 URI is provided.
        * ``ValueError``: There is no config.yaml file in the S3 bucket when an S3 URI is
          provided.
        * ``ValueError``: A file doesn't exist in a path that was specified by the user as
          part of an environment variable or additional configuration file path. This doesn't
          include the default config file locations.

    Args:
        additional_config_paths: List of config file paths.
            These paths can be one of the following. In the case of a directory, this method
            searches for a ``config.yaml`` file in that directory. This method does not perform a
            recursive search of folders in that directory.

                * Local file path
                * Local directory path
                * S3 URI of the config file
                * S3 URI of the directory containing the config file

            Note: S3 URI follows the format ``s3://<bucket>/<Key prefix>``
        s3_resource (boto3.resource("s3")): The Boto3 S3 resource. This is used to fetch
            config files from S3. If it is not provided but config files are present in S3,
            this method creates a default S3 resource. See `Boto3 Session documentation
            <https://boto3.amazonaws.com/v1/documentation/api\
            /latest/reference/core/session.html#boto3.session.Session.resource>`__.
            This argument is not needed if the config files are present in the local file system.
    """
    ...

def validate_sagemaker_config(sagemaker_config: dict = ...):
    """Validates whether a given dictionary adheres to the schema.

    The schema is defined at
    ``sagemaker.config.config_schema.SAGEMAKER_PYTHON_SDK_CONFIG_SCHEMA``.

    Args:
        sagemaker_config: A dictionary containing default values for the
                SageMaker Python SDK. (default: None).
    """
    ...

def load_local_mode_config() -> dict | None:
    """Loads the local mode config file."""
    ...

