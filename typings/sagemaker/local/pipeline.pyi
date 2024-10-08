"""
This type stub file was generated by pyright.
"""

from abc import ABC, abstractmethod
from typing import Dict
from sagemaker.workflow.steps import Step

"""Local Pipeline Executor"""
PRIMITIVES = ...
BINARY_CONDITION_TYPES = ...
class LocalPipelineExecutor:
    """An executor that executes SageMaker Pipelines locally."""
    def __init__(self, execution, sagemaker_session) -> None:
        """Initialize StepExecutor.

        Args:
            sagemaker_session (sagemaker.session.Session): a session to use to read configurations
                from, and use its boto client.
        """
        ...
    
    def execute(self):
        """Execute a local pipeline."""
        ...
    
    def evaluate_step_arguments(self, step):
        """Parses and evaluate step arguments."""
        ...
    
    def evaluate_pipeline_variable(self, pipeline_variable, step_name):
        """Evaluate pipeline variable runtime value."""
        ...
    


class _StepExecutor(ABC):
    """An abstract base class for step executors running steps locally"""
    def __init__(self, pipeline_executor: LocalPipelineExecutor, step: Step) -> None:
        ...
    
    @abstractmethod
    def execute(self) -> Dict:
        """Execute a pipeline step locally

        Returns:
            A dictionary as properties of the current step
        """
        ...
    


class _TrainingStepExecutor(_StepExecutor):
    """Executor class to execute TrainingStep locally"""
    def execute(self):
        ...
    


class _ProcessingStepExecutor(_StepExecutor):
    """Executor class to execute ProcessingStep locally"""
    def execute(self):
        ...
    


class _ConditionStepExecutor(_StepExecutor):
    """Executor class to execute ConditionStep locally"""
    def execute(self):
        ...
    


class _TransformStepExecutor(_StepExecutor):
    """Executor class to execute TransformStep locally"""
    def execute(self):
        ...
    


class _CreateModelStepExecutor(_StepExecutor):
    """Executor class to execute CreateModelStep locally"""
    def execute(self):
        ...
    


class _FailStepExecutor(_StepExecutor):
    """Executor class to execute FailStep locally"""
    def execute(self):
        ...
    


class _StepExecutorFactory:
    """Factory class to generate executors for given step based on their types"""
    def __init__(self, pipeline_executor: LocalPipelineExecutor) -> None:
        ...
    
    def get(self, step: Step) -> _StepExecutor:
        """Return corresponding step executor for given step"""
        ...
    


