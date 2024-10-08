"""
This type stub file was generated by pyright.
"""

"""S3 error codes adapted into more natural Python ones.

Adapted from: https://docs.aws.amazon.com/AmazonS3/latest/API/ErrorResponses.html
"""
ENAMETOOLONG = ...
ENOTEMPTY = ...
EMSGSIZE = ...
EREMOTEIO = ...
EREMCHG = ...
ERROR_CODE_TO_EXCEPTION = ...
def translate_boto_error(error, message=..., set_cause=..., *args, **kwargs):
    """Convert a ClientError exception into a Python one.

    Parameters
    ----------

    error : botocore.exceptions.ClientError
        The exception returned by the boto API.
    message : str
        An error message to use for the returned exception. If not given, the
        error message returned by the server is used instead.
    set_cause : bool
        Whether to set the __cause__ attribute to the previous exception if the
        exception is translated.
    *args, **kwargs :
        Additional arguments to pass to the exception constructor, after the
        error message. Useful for passing the filename arguments to ``IOError``.

    Returns
    -------

    An instantiated exception ready to be thrown. If the error code isn't
    recognized, an IOError with the original error message is returned.
    """
    ...

