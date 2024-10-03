import re
import os


def camel_to_snake(name):
    """Convert camelCase or PascalCase to snake_case."""
    s1 = re.sub("([a-z])([A-Z])", r"\1_\2", name)
    return s1.lower()


def process_file(file_path):
    """Read the file, replace camelCase/PascalCase variables with snake_case,
    and save to a new file suffixed with '_sn'."""
    with open(file_path, "r") as file:
        content = file.read()

    # Find all words that could be variable names (assuming they start with a letter)
    variables = re.findall(r"\b[a-zA-Z][a-zA-Z0-9]*\b", content)

    for var in variables:
        snake_case_var = camel_to_snake(var)
        if snake_case_var != var:  # Only replace if the name was camel or Pascal case
            content = content.replace(var, snake_case_var)

    # Generate the new file name by appending '_sn' before the file extension
    base, ext = os.path.splitext(file_path)
    new_file_path = f"{base}_sn{ext}"

    # Write the modified content to the new file
    with open(new_file_path, "w") as new_file:
        new_file.write(content)

    print(f"Processed file: {new_file_path}")


# Example usage
process_file(
    "/Users/frankserrao/MyStuff/TestAndPlay/Click2Mail/c2m-generative-ai-marketing-portal/assets/layers/utilities/python/aws_helper.py"
)
