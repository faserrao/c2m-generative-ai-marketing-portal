"""
This type stub file was generated by pyright.
"""

from sagemaker.workflow.entities import PipelineVariable, RequestType

"""Pipeline parameters and conditions for workflow."""
class ExecutionVariable(PipelineVariable):
    """Pipeline execution variables for workflow."""
    def __init__(self, name: str) -> None:
        """Create a pipeline execution variable.

        Args:
            name (str): The name of the execution variable.
        """
        ...
    
    def __eq__(self, other) -> bool:
        """Override default equals method"""
        ...
    
    def to_string(self) -> PipelineVariable:
        """Prompt the pipeline to convert the pipeline variable to String in runtime

        As ExecutionVariable is treated as String in runtime, no extra actions are needed.
        """
        ...
    
    @property
    def expr(self) -> RequestType:
        """The 'Get' expression dict for an `ExecutionVariable`."""
        ...
    


class ExecutionVariables:
    """Provide access to all available execution variables:

    - ExecutionVariables.START_DATETIME
    - ExecutionVariables.CURRENT_DATETIME
    - ExecutionVariables.PIPELINE_NAME
    - ExecutionVariables.PIPELINE_ARN
    - ExecutionVariables.PIPELINE_EXECUTION_ID
    - ExecutionVariables.PIPELINE_EXECUTION_ARN
    - ExecutionVariables.TRAINING_JOB_NAME
    - ExecutionVariables.PROCESSING_JOB_NAME
    """
    START_DATETIME = ...
    CURRENT_DATETIME = ...
    PIPELINE_NAME = ...
    PIPELINE_ARN = ...
    PIPELINE_EXECUTION_ID = ...
    PIPELINE_EXECUTION_ARN = ...
    TRAINING_JOB_NAME = ...
    PROCESSING_JOB_NAME = ...


