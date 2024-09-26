import inspect
import logging
import sys

LOGGER = logging.Logger("Content-generation", level=logging.INFO)
HANDLER = logging.StreamHandler(sys.stdout)
HANDLER.setFormatter(logging.Formatter("%(levelname)s | %(name)s | %(message)s"))
LOGGER.addHandler(HANDLER)


def print_response(text_to_print: str, response=None):
    """Print and log the response with caller information.

    Args:
        text_to_print (str): The text to be printed.
        response (Optional): The response object to be logged.
    """
    # Get the current frame and the caller's frame
    stack = inspect.stack()

    # The caller's frame is at index 1 in the stack
    caller_frame = stack[1]

    # Get the function name from the caller's frame
    caller_function_name = caller_frame.function

    print(f"called_function was called by: {caller_function_name}")

    if response is not None:
        print(f"{caller_function_name}(): {text_to_print} response: {response.text}")
        LOGGER.info("%s(): %s response: %s", caller_function_name, text_to_print, response.text)
    else:
        print(f"{caller_function_name}(): {text_to_print}")
        LOGGER.error("%s(): %s", caller_function_name, text_to_print)
