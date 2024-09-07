import sys
import inspect
import logging

LOGGER = logging.Logger("Content-generation", level=logging.INFO)
HANDLER = logging.StreamHandler(sys.stdout)
HANDLER.setFormatter(logging.Formatter("%(levelname)s | %(name)s | %(message)s"))
LOGGER.addHandler(HANDLER)

def print_response(text_to_print: str, response = None):

    # Get the current frame and the caller's frame
    stack = inspect.stack()

    # The caller's frame is at index 1 in the stack
    caller_frame = stack[1]

    # Get the function name from the caller's frame
    caller_function_name = caller_frame.function

    print(f"called_function was called by: {caller_function_name}")

    if (response is not None):
        print(f"{caller_function_name}(): {text_to_print} response: {response.text}")
        logging.info(f"{caller_function_name}(): {text_to_print} response: {response.text}")
        # logging.error(f"c2m_add_credit():Add credit call failed: {response.status_code}, {r.text}")
    else:
        print(f"{caller_function_name}(): {text_to_print}") 
        logging.error(f"{caller_function_name}(): {text_to_print}")
        # logging.error(f"c2m_add_credit():Add credit call failed: {response.status_code}, {r.text}")
        

    """
    # Serialize and print JSON data
    serialized_json_response = json.dumps(json_response, indent=4)  
    print(f"{function_name}(): {text_to_print} response: {serialized_json_response}")
    # Check if the response contains JSON data
    try:
        # Extract JSON content
        json_response = response.json()
    except ValueError:
        print("Response is not in JSON format.")
    """