"""
This type stub file was generated by pyright.
"""

import attr
from typing import Any, Dict, List, Optional, Sequence, Set, Union
from sagemaker.session import Session
from sagemaker.workflow.entities import Entity, RequestType
from sagemaker.workflow.parameters import Parameter
from sagemaker.workflow.pipeline_definition_config import PipelineDefinitionConfig
from sagemaker.workflow.pipeline_experiment_config import PipelineExperimentConfig
from sagemaker.workflow.parallelism_config import ParallelismConfiguration
from sagemaker.workflow.selective_execution_config import SelectiveExecutionConfig
from sagemaker.workflow.steps import Step
from sagemaker.workflow.step_collections import StepCollection

"""The Pipeline entity for workflow."""
logger = ...
_DEFAULT_EXPERIMENT_CFG = ...
_DEFAULT_DEFINITION_CFG = ...
class Pipeline(Entity):
    """Pipeline for workflow."""
    def __init__(self, name: str = ..., parameters: Optional[Sequence[Parameter]] = ..., pipeline_experiment_config: Optional[PipelineExperimentConfig] = ..., steps: Optional[Sequence[Union[Step, StepCollection]]] = ..., sagemaker_session: Optional[Session] = ..., pipeline_definition_config: Optional[PipelineDefinitionConfig] = ...) -> None:
        """Initialize a Pipeline

        Args:
            name (str): The name of the pipeline.
            parameters (Sequence[Parameter]): The list of the parameters.
            pipeline_experiment_config (Optional[PipelineExperimentConfig]): If set,
                the workflow will attempt to create an experiment and trial before
                executing the steps. Creation will be skipped if an experiment or a trial with
                the same name already exists. By default, pipeline name is used as
                experiment name and execution id is used as the trial name.
                If set to None, no experiment or trial will be created automatically.
            steps (Sequence[Union[Step, StepCollection]]): The list of the non-conditional steps
                associated with the pipeline. Any steps that are within the
                `if_steps` or `else_steps` of a `ConditionStep` cannot be listed in the steps of a
                pipeline. Of particular note, the workflow service rejects any pipeline definitions
                that specify a step in the list of steps of a pipeline and that step in the
                `if_steps` or `else_steps` of any `ConditionStep`.
            sagemaker_session (sagemaker.session.Session): Session object that manages interactions
                with Amazon SageMaker APIs and any other AWS services needed. If not specified, the
                pipeline creates one using the default AWS configuration chain.
            pipeline_definition_config (Optional[PipelineDefinitionConfig]): If set,
                the workflow customizes the pipeline definition using the configurations
                specified. By default, custom job-prefixing is turned off.
        """
        ...
    
    def to_request(self) -> RequestType:
        """Gets the request structure for workflow service calls."""
        ...
    
    def create(self, role_arn: str = ..., description: str = ..., tags: List[Dict[str, str]] = ..., parallelism_config: ParallelismConfiguration = ...) -> Dict[str, Any]:
        """Creates a Pipeline in the Pipelines service.

        Args:
            role_arn (str): The role arn that is assumed by the pipeline to create step artifacts.
            description (str): A description of the pipeline.
            tags (List[Dict[str, str]]): A list of {"Key": "string", "Value": "string"} dicts as
                tags.
            parallelism_config (Optional[ParallelismConfiguration]): Parallelism configuration
                that is applied to each of the executions of the pipeline. It takes precedence
                over the parallelism configuration of the parent pipeline.

        Returns:
            A response dict from the service.
        """
        ...
    
    def describe(self) -> Dict[str, Any]:
        """Describes a Pipeline in the Workflow service.

        Returns:
            Response dict from the service. See `boto3 client documentation
            <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/\
sagemaker.html#SageMaker.Client.describe_pipeline>`_
        """
        ...
    
    def update(self, role_arn: str = ..., description: str = ..., parallelism_config: ParallelismConfiguration = ...) -> Dict[str, Any]:
        """Updates a Pipeline in the Workflow service.

        Args:
            role_arn (str): The role arn that is assumed by pipelines to create step artifacts.
            description (str): A description of the pipeline.
            parallelism_config (Optional[ParallelismConfiguration]): Parallelism configuration
                that is applied to each of the executions of the pipeline. It takes precedence
                over the parallelism configuration of the parent pipeline.

        Returns:
            A response dict from the service.
        """
        ...
    
    def upsert(self, role_arn: str = ..., description: str = ..., tags: List[Dict[str, str]] = ..., parallelism_config: ParallelismConfiguration = ...) -> Dict[str, Any]:
        """Creates a pipeline or updates it, if it already exists.

        Args:
            role_arn (str): The role arn that is assumed by workflow to create step artifacts.
            description (str): A description of the pipeline.
            tags (List[Dict[str, str]]): A list of {"Key": "string", "Value": "string"} dicts as
                tags.
            parallelism_config (Optional[Config for parallel steps, Parallelism configuration that
                is applied to each of. the executions

        Returns:
            response dict from service
        """
        ...
    
    def delete(self) -> Dict[str, Any]:
        """Deletes a Pipeline in the Workflow service.

        Returns:
            A response dict from the service.
        """
        ...
    
    def start(self, parameters: Dict[str, Union[str, bool, int, float]] = ..., execution_display_name: str = ..., execution_description: str = ..., parallelism_config: ParallelismConfiguration = ..., selective_execution_config: SelectiveExecutionConfig = ...): # -> _PipelineExecution:
        """Starts a Pipeline execution in the Workflow service.

        Args:
            parameters (Dict[str, Union[str, bool, int, float]]): values to override
                pipeline parameters.
            execution_display_name (str): The display name of the pipeline execution.
            execution_description (str): A description of the execution.
            parallelism_config (Optional[ParallelismConfiguration]): Parallelism configuration
                that is applied to each of the executions of the pipeline. It takes precedence
                over the parallelism configuration of the parent pipeline.
            selective_execution_config (Optional[SelectiveExecutionConfig]): The configuration for
                selective step execution.

        Returns:
            A `_PipelineExecution` instance, if successful.
        """
        ...
    
    def definition(self) -> str:
        """Converts a request structure to string representation for workflow service calls."""
        ...
    
    def list_executions(self, sort_by: str = ..., sort_order: str = ..., max_results: int = ..., next_token: str = ...) -> Dict[str, Any]:
        """Lists a pipeline's executions.

        Args:
            sort_by (str): The field by which to sort results(CreationTime/PipelineExecutionArn).
            sort_order (str): The sort order for results (Ascending/Descending).
            max_results (int): The maximum number of pipeline executions to return in the response.
            next_token (str):  If the result of the previous `ListPipelineExecutions` request was
                truncated, the response includes a `NextToken`. To retrieve the next set of pipeline
                executions, use the token in the next request.

        Returns:
            List of Pipeline Execution Summaries. See
            boto3 client list_pipeline_executions
            https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Client.list_pipeline_executions
        """
        ...
    
    def build_parameters_from_execution(self, pipeline_execution_arn: str, parameter_value_overrides: Dict[str, Union[str, bool, int, float]] = ...) -> Dict[str, Union[str, bool, int, float]]:
        """Gets the parameters from an execution, update with optional parameter value overrides.

        Args:
            pipeline_execution_arn (str): The arn of the reference pipeline execution.
            parameter_value_overrides (Dict[str, Union[str, bool, int, float]]): Parameter dict
                to be updated with the parameters from the referenced execution.

        Returns:
            A parameter dict built from an execution and provided parameter value overrides.
        """
        ...
    


def format_start_parameters(parameters: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Formats start parameter overrides as a list of dicts.

    This list of dicts adheres to the request schema of:

        `{"Name": "MyParameterName", "Value": "MyValue"}`

    Args:
        parameters (Dict[str, Any]): A dict of named values where the keys are
            the names of the parameters to pass values into.
    """
    ...

def interpolate(request_obj: RequestType, callback_output_to_step_map: Dict[str, str], lambda_output_to_step_map: Dict[str, str]) -> RequestType:
    """Replaces Parameter values in a list of nested Dict[str, Any] with their workflow expression.

    Args:
        request_obj (RequestType): The request dict.
        callback_output_to_step_map (Dict[str, str]): A dict of output name -> step name.
        lambda_output_to_step_map (Dict[str, str]): A dict of output name -> step name.

    Returns:
        RequestType: The request dict with Parameter values replaced by their expression.
    """
    ...

def update_args(args: Dict[str, Any], **kwargs): # -> None:
    """Updates the request arguments dict with a value, if populated.

    This handles the case when the service API doesn't like NoneTypes for argument values.

    Args:
        request_args (Dict[str, Any]): The request arguments dict.
        kwargs: key, value pairs to update the args dict with.
    """
    ...

@attr.s
class _PipelineExecution:
    """Internal class for encapsulating pipeline execution instances.

    Attributes:
        arn (str): The arn of the pipeline execution.
        sagemaker_session (sagemaker.session.Session): Session object which manages interactions
            with Amazon SageMaker APIs and any other AWS services needed. If not specified, the
            pipeline creates one using the default AWS configuration chain.
    """
    arn: str = ...
    sagemaker_session: Session = ...
    def stop(self):
        """Stops a pipeline execution."""
        ...
    
    def describe(self):
        """Describes a pipeline execution.

        Returns:
             Information about the pipeline execution. See
             `boto3 client describe_pipeline_execution
             <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/\
sagemaker.html#SageMaker.Client.describe_pipeline_execution>`_.
        """
        ...
    
    def list_steps(self):
        """Describes a pipeline execution's steps.

        Returns:
             Information about the steps of the pipeline execution. See
             `boto3 client list_pipeline_execution_steps
             <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/\
sagemaker.html#SageMaker.Client.list_pipeline_execution_steps>`_.
        """
        ...
    
    def list_parameters(self, max_results: int = ..., next_token: str = ...):
        """Gets a list of parameters for a pipeline execution.

        Args:
            max_results (int): The maximum number of parameters to return in the response.
            next_token (str):  If the result of the previous `ListPipelineParametersForExecution`
                request was truncated, the response includes a `NextToken`. To retrieve the next
                set of parameters, use the token in the next request.

        Returns:
            Information about the parameters of the pipeline execution. This function is also
            a wrapper for `list_pipeline_parameters_for_execution
            <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Client.list_pipeline_parameters_for_execution>`_.
        """
        ...
    
    def wait(self, delay=..., max_attempts=...):
        """Waits for a pipeline execution.

        Args:
            delay (int): The polling interval. (Defaults to 30 seconds)
            max_attempts (int): The maximum number of polling attempts.
                (Defaults to 60 polling attempts)
        """
        ...
    


class PipelineGraph:
    """Helper class representing the Pipeline Directed Acyclic Graph (DAG)

    Attributes:
        steps (Sequence[Union[Step, StepCollection]]): Sequence of `Step`s and/or `StepCollection`s
            that represent each node in the pipeline DAG
    """
    def __init__(self, steps: Sequence[Union[Step, StepCollection]]) -> None:
        ...
    
    @classmethod
    def from_pipeline(cls, pipeline: Pipeline): # -> Self:
        """Create a PipelineGraph object from the Pipeline object."""
        ...
    
    def is_cyclic(self) -> bool:
        """Check if this pipeline graph is cyclic.

        Returns true if it is cyclic, false otherwise.
        """
        ...
    
    def get_steps_in_sub_dag(self, current_step: Union[Step, StepCollection], sub_dag_steps: Set[str] = ...) -> Set[str]:
        """Get names of all steps (including current step) in the sub dag of current step.

        Returns a set of step names in the sub dag.
        """
        ...
    
    def __iter__(self):
        """Perform topological sort traversal of the Pipeline Graph."""
        ...
    
    def __next__(self) -> Step:
        """Return the next Step node from the Topological sort order."""
        ...
    


