"""
This type stub file was generated by pyright.
"""

"""Provides utilities for converting between python style and boto style."""
def to_camel_case(snake_case):
    """Convert a snake case string to camel case.

    Args:
        snake_case (str): String to convert to camel case.

    Returns:
        str: String converted to camel case.
    """
    ...

def to_snake_case(name):
    """Convert a camel case string to snake case.

    Args:
        name (str): String to convert to snake case.

    Returns:
        str: String converted to snake case.
    """
    ...

def from_boto(boto_dict, boto_name_to_member_name, member_name_to_type):
    """Convert an UpperCamelCase boto response to a snake case representation.

    Args:
        boto_dict (dict[str, ?]): A boto response dictionary.
        boto_name_to_member_name (dict[str, str]):  A map from boto name to snake_case name.
            If a given boto name is not in the map then a default mapping is applied.
        member_name_to_type (dict[str, (_base_types.ApiObject, boolean)]): A map from snake case
            name to a type description tuple. The first element of the tuple, a subclass of
            ApiObject, is the type of the mapped object. The second element indicates whether the
            mapped element is a collection or singleton.

    Returns:
        dict: Boto response in snake case.
    """
    ...

def to_boto(member_vars, member_name_to_boto_name, member_name_to_type):
    """Convert a dict of of snake case names to values into a boto UpperCamelCase representation.

    Args:
        member_vars dict[str, ?]: A map from snake case name to value.
        member_name_to_boto_name dict[str, ?]: A map from snake_case name to boto name.

     Returns:
         dict: boto dict converted to snake case

    """
    ...

