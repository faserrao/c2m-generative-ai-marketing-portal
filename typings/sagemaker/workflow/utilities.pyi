"""
This type stub file was generated by pyright.
"""

from typing import List, Sequence, Set, TYPE_CHECKING, Union
from sagemaker.workflow.pipeline_context import _PipelineConfig, _StepArguments
from sagemaker.workflow.entities import Entity, RequestType
from sagemaker.workflow.pipeline_definition_config import PipelineDefinitionConfig
from sagemaker.workflow.step_collections import StepCollection

"""
This type stub file was generated by pyright.
"""
logger = ...
DEF_CONFIG_WARN_MSG_TEMPLATE = ...
if TYPE_CHECKING:
    ...
BUF_SIZE = ...
_pipeline_config: _PipelineConfig = ...
def list_to_request(entities: Sequence[Union[Entity, StepCollection]]) -> List[RequestType]:
    """Get the request structure for list of entities.

    Args:
        entities (Sequence[Entity]): A list of entities.
    Returns:
        list: A request structure for a workflow service call.
    """
    ...

def build_steps(steps: Sequence[Entity], pipeline_name: str, pipeline_definition_config: PipelineDefinitionConfig):
    """Get the request structure for list of steps, with _pipeline_config_manager

    Args:
        steps (Sequence[Entity]): A list of steps, (Entity type because Step causes circular import)
        pipeline_name (str): The name of the pipeline, passed down from pipeline.to_request()
        pipeline_definition_config (PipelineDefinitionConfig): A pipeline definition configuration
            for a pipeline containing feature flag toggles
    Returns:
        list: A request structure object for a service call for the list of pipeline steps
    """
    ...

def get_code_hash(step: Entity) -> str:
    """Get the hash of the code artifact(s) for the given step

    Args:
        step (Entity): A pipeline step object (Entity type because Step causes circular import)
    Returns:
        str: A hash string representing the unique code artifact(s) for the step
    """
    ...

def get_processing_dependencies(dependency_args: List[List[str]]) -> List[str]:
    """Get the Processing job dependencies from the processor run kwargs

    Args:
        dependency_args: A list of dependency args from processor.run()
    Returns:
        List[str]: A list of code dependencies for the job
    """
    ...

def get_processing_code_hash(code: str, source_dir: str, dependencies: List[str]) -> str:
    """Get the hash of a processing step's code artifact(s).

    Args:
        code (str): Path to a file with the processing script to run
        source_dir (str): Path to a directory with any other processing
                source code dependencies aside from the entry point file
        dependencies (str): A list of paths to directories (absolute
                or relative) with any additional libraries that will be exported
                to the container
    Returns:
        str: A hash string representing the unique code artifact(s) for the step
    """
    ...

def get_training_code_hash(entry_point: str, source_dir: str, dependencies: List[str]) -> str:
    """Get the hash of a training step's code artifact(s).

    Args:
        entry_point (str): The absolute or relative path to the local Python
                source file that should be executed as the entry point to
                training
        source_dir (str): Path to a directory with any other training source
                code dependencies aside from the entry point file
        dependencies (str): A list of paths to directories (absolute
                or relative) with any additional libraries that will be exported
                to the container
    Returns:
        str: A hash string representing the unique code artifact(s) for the step
    """
    ...

def get_config_hash(step: Entity):
    """Get the hash of the config artifact(s) for the given step

    Args:
        step (Entity): A pipeline step object (Entity type because Step causes circular import)
    Returns:
        str: A hash string representing the unique config artifact(s) for the step
    """
    ...

def hash_object(obj) -> str:
    """Get the MD5 hash of an object.

    Args:
        obj (dict): The object
    Returns:
        str: The MD5 hash of the object
    """
    ...

def hash_file(path: str) -> str:
    """Get the MD5 hash of a file.

    Args:
        path (str): The local path for the file.
    Returns:
        str: The MD5 hash of the file.
    """
    ...

def hash_files_or_dirs(paths: List[str]) -> str:
    """Get the MD5 hash of the contents of a list of files or directories.

    Hash is changed if:
       * input list is changed
       * new nested directories/files are added to any directory in the input list
       * nested directory/file names are changed for any of the inputted directories
       * content of files is edited

    Args:
        paths: List of file or directory paths
    Returns:
        str: The MD5 hash of the list of files or directories.
    """
    ...

def validate_step_args_input(step_args: _StepArguments, expected_caller: Set[str], error_message: str):
    """Validate the `_StepArguments` object which is passed into a pipeline step

    Args:
        step_args (_StepArguments): A `_StepArguments` object to be used for composing
            a pipeline step.
        expected_caller (Set[str]): The expected name of the caller function which is
            intercepted by the PipelineSession to get the step arguments.
        error_message (str): The error message to be thrown if the validation fails.
    """
    ...

def override_pipeline_parameter_var(func):
    """A decorator to override pipeline Parameters passed into a function

    This is a temporary decorator to override pipeline Parameter objects with their default value
    and display warning information to instruct users to update their code.

    This decorator can help to give a grace period for users to update their code when
    we make changes to explicitly prevent passing any pipeline variables to a function.

    We should remove this decorator after the grace period.
    """
    ...

def execute_job_functions(step_args: _StepArguments):
    """Execute the job class functions during pipeline definition construction

    Executes the job functions such as run(), fit(), or transform() that have been
    delayed until the pipeline gets built, for steps built with a PipelineSession.

    Handles multiple functions in instances where job functions are chained
    together from the inheritance of different job classes (e.g. PySparkProcessor,
    ScriptProcessor, and Processor).

    Args:
        step_args (_StepArguments): A `_StepArguments` object to be used for composing
            a pipeline step, contains the necessary function information
    """
    ...

def trim_request_dict(request_dict, job_key, config):
    """Trim request_dict for unwanted fields to not persist them in step arguments

    Trim the job_name field off request_dict in cases where we do not want to include it
    in the pipeline definition.

    Args:
        request_dict (dict): A dictionary used to build the arguments for a pipeline step,
            containing fields that will be passed to job client during orchestration.
        job_key (str): The key in a step's arguments to look up the base_job_name if it
            exists
        config (_pipeline_config) The config intercepted and set for a pipeline via the
            context manager
    """
    ...

