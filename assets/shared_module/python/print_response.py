import json

def print_response(function_name, text_to_print, response):

  """
  # Check if the response contains JSON data
  try:
      # Extract JSON content
      json_response = response.json()
  except ValueError:
      print("Response is not in JSON format.")


  # Serialize and print JSON data
  serialized_json_response = json.dumps(json_response, indent=4)  
  print(f"{function_name}(): {text_to_print} response: {serialized_json_response}")
  """

  print(f"{function_name}(): {text_to_print} response: {response.text}")