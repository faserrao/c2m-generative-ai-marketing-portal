"""
This type stub file was generated by pyright.
"""

import attr
from enum import Enum
from typing import Dict, List, Type
from sagemaker.workflow.entities import DefaultEnumMeta, Entity, PipelineVariable, PrimitiveType, RequestType

"""
This type stub file was generated by pyright.
"""
class ParameterTypeEnum(Enum, metaclass=DefaultEnumMeta):
    """Parameter type enum."""
    STRING = ...
    INTEGER = ...
    BOOLEAN = ...
    FLOAT = ...
    @property
    def python_type(self) -> Type:
        """Provide the Python type of the enum value."""
        ...
    


@attr.s
class Parameter(PipelineVariable, Entity):
    """Pipeline parameter for workflow.

    Attributes:
        name (str): The name of the parameter.
        parameter_type (ParameterTypeEnum): The type of the parameter.
        default_value (PrimitiveType): The default value of the parameter.
    """
    name: str = ...
    parameter_type: ParameterTypeEnum = ...
    default_value: PrimitiveType = ...
    def to_request(self) -> RequestType:
        """Get the request structure for workflow service calls."""
        ...
    
    @property
    def expr(self) -> Dict[str, str]:
        """The 'Get' expression dict for a `Parameter`."""
        ...
    


ParameterBoolean = ...
class ParameterString(Parameter):
    """String parameter for pipelines."""
    def __init__(self, name: str, default_value: str = ..., enum_values: List[str] = ...) -> None:
        """Create a pipeline string parameter.

        Args:
            name (str): The name of the parameter.
            default_value (str): The default value of the parameter.
                The default value could be overridden at start of an execution.
                If not set or it is set to None, a value must be provided
                at the start of the execution.
            enum_values (List[str]): Enum values for this parameter.
        """
        ...
    
    def __hash__(self) -> int:
        """Hash function for parameter types"""
        ...
    
    def to_string(self) -> PipelineVariable:
        """Prompt the pipeline to convert the pipeline variable to String in runtime

        As ParameterString is treated as String in runtime, no extra actions are needed.
        """
        ...
    
    def to_request(self) -> RequestType:
        """Get the request structure for workflow service calls."""
        ...
    


class ParameterInteger(Parameter):
    """Integer parameter for pipelines."""
    def __init__(self, name: str, default_value: int = ...) -> None:
        """Create a pipeline integer parameter.

        Args:
            name (str): The name of the parameter.
            default_value (int): The default value of the parameter.
                The default value could be overridden at start of an execution.
                If not set or it is set to None, a value must be provided
                at the start of the execution.
        """
        ...
    


class ParameterFloat(Parameter):
    """Float parameter for pipelines."""
    def __init__(self, name: str, default_value: float = ...) -> None:
        """Create a pipeline float parameter.

        Args:
            name (str): The name of the parameter.
            default_value (float): The default value of the parameter.
                The default value could be overridden at start of an execution.
                If not set or it is set to None, a value must be provided
                at the start of the execution.
        """
        ...
    


