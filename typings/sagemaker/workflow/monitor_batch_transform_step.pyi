"""
This type stub file was generated by pyright.
"""

from typing import Optional, Union
from sagemaker.workflow.pipeline_context import _JobStepArguments
from sagemaker.workflow.entities import PipelineVariable
from sagemaker.workflow.step_collections import StepCollection
from sagemaker.workflow.quality_check_step import QualityCheckConfig
from sagemaker.workflow.clarify_check_step import ClarifyCheckConfig
from sagemaker.workflow.check_job_config import CheckJobConfig

"""The `MonitorBatchTransform` definition for SageMaker Pipelines Workflows"""
class MonitorBatchTransformStep(StepCollection):
    """Creates a Transformer step with Quality or Clarify check step

    Used to monitor the inputs and outputs of the batch transform job.
    """
    def __init__(self, name: str, transform_step_args: _JobStepArguments, monitor_configuration: Union[QualityCheckConfig, ClarifyCheckConfig], check_job_configuration: CheckJobConfig, monitor_before_transform: bool = ..., fail_on_violation: Union[bool, PipelineVariable] = ..., supplied_baseline_statistics: Union[str, PipelineVariable] = ..., supplied_baseline_constraints: Union[str, PipelineVariable] = ..., display_name: Optional[str] = ..., description: Optional[str] = ...) -> None:
        """Construct a step collection of `TransformStep`, `QualityCheckStep` or `ClarifyCheckStep`

        Args:
            name (str): The name of the `MonitorBatchTransformStep`.
                The corresponding transform step will be named `{name}-transform`;
                and the corresponding check step will be named `{name}-monitoring`
            transform_step_args (_JobStepArguments): the transform step transform arguments.
            monitor_configuration (Union[
                `sagemaker.workflow.quality_check_step.QualityCheckConfig`,
                `sagemaker.workflow.quality_check_step.ClarifyCheckConfig`
            ]): the monitoring configuration used for run model monitoring.
            check_job_configuration (`sagemaker.workflow.check_job_config.CheckJobConfig`):
                the check job (processing job) cluster resource configuration.
            monitor_before_transform (bool): If to run data quality or model explainability
                monitoring type, a true value of this flag indicates
                running the check step before the transform job.
            fail_on_violation (Union[bool, PipelineVariable]): A opt-out flag to not to fail the
                check step when a violation is detected.
            supplied_baseline_statistics (Union[str, PipelineVariable]): The S3 path
                to the supplied statistics object representing the statistics JSON file
                which will be used for drift to check (default: None).
            supplied_baseline_constraints (Union[str, PipelineVariable]): The S3 path
                to the supplied constraints object representing the constraints JSON file
                which will be used for drift to check (default: None).
            display_name (str): The display name of the `MonitorBatchTransformStep`.
                The display name provides better UI readability.
                The corresponding transform step will be
                named `{display_name}-transform`;  and the corresponding check step
                will be named `{display_name}-monitoring` (default: None).
            description (str): The description of the `MonitorBatchTransformStep` (default: None).
        """
        ...
    


