"""
This type stub file was generated by pyright.
"""

import attr
from abc import ABC
from typing import List, Optional, Union
from sagemaker.clarify import BiasConfig, DataConfig, ModelConfig, ModelPredictedLabelConfig, SHAPConfig
from sagemaker.workflow.entities import PipelineVariable, RequestType
from sagemaker.workflow.step_collections import StepCollection
from sagemaker.workflow.steps import CacheConfig, Step
from sagemaker.workflow.check_job_config import CheckJobConfig

"""The step definitions for workflow."""
_DATA_BIAS_TYPE = ...
_MODEL_BIAS_TYPE = ...
_MODEL_EXPLAINABILITY_TYPE = ...
_BIAS_MONITORING_CFG_BASE_NAME = ...
_EXPLAINABILITY_MONITORING_CFG_BASE_NAME = ...
@attr.s
class ClarifyCheckConfig(ABC):
    """Clarify Check Config

    Attributes:
        data_config (DataConfig): Config of the input/output data.
        kms_key (str): The ARN of the KMS key that is used to encrypt the
            user code file (default: None).
            This field CANNOT be any type of the `PipelineVariable`.
        monitoring_analysis_config_uri: (str): The uri of monitoring analysis config.
            This field does not take input.
            It will be generated once uploading the created analysis config file.
    """
    data_config: DataConfig = ...
    kms_key: str = ...
    monitoring_analysis_config_uri: str = ...


@attr.s
class DataBiasCheckConfig(ClarifyCheckConfig):
    """Data Bias Check Config

    Attributes:
        data_bias_config (BiasConfig): Config of sensitive groups.
        methods (str or list[str]): Selector of a subset of potential metrics:
            ["`CI <https://docs.aws.amazon.com/sagemaker/latest/dg/clarify-bias-metric-class-imbalance.html>`_",
            "`DPL <https://docs.aws.amazon.com/sagemaker/latest/dg/clarify-data-bias-metric-true-label-imbalance.html>`_",
            "`KL <https://docs.aws.amazon.com/sagemaker/latest/dg/clarify-data-bias-metric-kl-divergence.html>`_",
            "`JS <https://docs.aws.amazon.com/sagemaker/latest/dg/clarify-data-bias-metric-jensen-shannon-divergence.html>`_",
            "`LP <https://docs.aws.amazon.com/sagemaker/latest/dg/clarify-data-bias-metric-lp-norm.html>`_",
            "`TVD <https://docs.aws.amazon.com/sagemaker/latest/dg/clarify-data-bias-metric-total-variation-distance.html>`_",
            "`KS <https://docs.aws.amazon.com/sagemaker/latest/dg/clarify-data-bias-metric-kolmogorov-smirnov.html>`_",
            "`CDDL <https://docs.aws.amazon.com/sagemaker/latest/dg/clarify-data-bias-metric-cddl.html>`_"].
            Defaults to computing all.
            This field CANNOT be any type of the `PipelineVariable`.
    """
    data_bias_config: BiasConfig = ...
    methods: Union[str, List[str]] = ...


@attr.s
class ModelBiasCheckConfig(ClarifyCheckConfig):
    """Model Bias Check Config

    Attributes:
        data_bias_config (BiasConfig): Config of sensitive groups.
        model_config (ModelConfig): Config of the model and its endpoint to be created.
        model_predicted_label_config (ModelPredictedLabelConfig): Config of how to
            extract the predicted label from the model output.
        methods (str or list[str]): Selector of a subset of potential metrics:
            ["`DPPL <https://docs.aws.amazon.com/sagemaker/latest/dg/clarify-post-training-bias-metric-dppl.html>`_"
            , "`DI <https://docs.aws.amazon.com/sagemaker/latest/dg/clarify-post-training-bias-metric-di.html>`_",
            "`DCA <https://docs.aws.amazon.com/sagemaker/latest/dg/clarify-post-training-bias-metric-dca.html>`_",
            "`DCR <https://docs.aws.amazon.com/sagemaker/latest/dg/clarify-post-training-bias-metric-dcr.html>`_",
            "`RD <https://docs.aws.amazon.com/sagemaker/latest/dg/clarify-post-training-bias-metric-rd.html>`_",
            "`DAR <https://docs.aws.amazon.com/sagemaker/latest/dg/clarify-post-training-bias-metric-dar.html>`_",
            "`DRR <https://docs.aws.amazon.com/sagemaker/latest/dg/clarify-post-training-bias-metric-drr.html>`_",
            "`AD <https://docs.aws.amazon.com/sagemaker/latest/dg/clarify-post-training-bias-metric-ad.html>`_",
            "`CDDPL <https://docs.aws.amazon.com/sagemaker/latest/dg/clarify-post-training-bias-metric-cddpl.html>`_
            ", "`TE <https://docs.aws.amazon.com/sagemaker/latest/dg/clarify-post-training-bias-metric-te.html>`_",
            "`FT <https://docs.aws.amazon.com/sagemaker/latest/dg/clarify-post-training-bias-metric-ft.html>`_"].
            Defaults to computing all.
            This field CANNOT be any type of the `PipelineVariable`.
    """
    data_bias_config: BiasConfig = ...
    model_config: ModelConfig = ...
    model_predicted_label_config: ModelPredictedLabelConfig = ...
    methods: Union[str, List[str]] = ...


@attr.s
class ModelExplainabilityCheckConfig(ClarifyCheckConfig):
    """Model Explainability Check Config

    Attributes:
        model_config (ModelConfig): Config of the model and its endpoint to be created.
        explainability_config (SHAPConfig): Config of the specific explainability method.
            Currently, only SHAP is supported.
        model_scores (str or int or ModelPredictedLabelConfig): Index or JMESPath expression
            to locate the predicted scores in the model output (default: None).
            This is not required if the model output is a single score. Alternatively,
            an instance of ModelPredictedLabelConfig can be provided
            but this field CANNOT be any type of the `PipelineVariable`.
    """
    model_config: ModelConfig = ...
    explainability_config: SHAPConfig = ...
    model_scores: Union[str, int, ModelPredictedLabelConfig] = ...


class ClarifyCheckStep(Step):
    """ClarifyCheckStep step for workflow."""
    def __init__(self, name: str, clarify_check_config: ClarifyCheckConfig, check_job_config: CheckJobConfig, skip_check: Union[bool, PipelineVariable] = ..., fail_on_violation: Union[bool, PipelineVariable] = ..., register_new_baseline: Union[bool, PipelineVariable] = ..., model_package_group_name: Union[str, PipelineVariable] = ..., supplied_baseline_constraints: Union[str, PipelineVariable] = ..., display_name: str = ..., description: str = ..., cache_config: CacheConfig = ..., depends_on: Optional[List[Union[str, Step, StepCollection]]] = ...) -> None:
        """Constructs a ClarifyCheckStep.

        Args:
            name (str): The name of the ClarifyCheckStep step.
            clarify_check_config (ClarifyCheckConfig): A ClarifyCheckConfig instance.
            check_job_config (CheckJobConfig): A CheckJobConfig instance.
            skip_check (bool or PipelineVariable): Whether the check
                should be skipped (default: False).
            fail_on_violation (bool or PipelineVariable): Whether to fail the step
                if violation detected (default: True).
            register_new_baseline (bool or PipelineVariable): Whether
                the new baseline should be registered (default: False).
            model_package_group_name (str or PipelineVariable): The name of a
                registered model package group, among which the baseline will be fetched
                from the latest approved model (default: None).
            supplied_baseline_constraints (str or PipelineVariable): The S3 path
                to the supplied constraints object representing the constraints JSON file
                which will be used for drift to check (default: None).
            display_name (str): The display name of the ClarifyCheckStep step (default: None).
            description (str): The description of the ClarifyCheckStep step (default: None).
            cache_config (CacheConfig):  A `sagemaker.workflow.steps.CacheConfig` instance
                (default: None).
            depends_on (List[Union[str, Step, StepCollection]]): A list of `Step`/`StepCollection`
                names or `Step` instances or `StepCollection` instances that this `ClarifyCheckStep`
                depends on (default: None).
        """
        ...
    
    @property
    def arguments(self) -> RequestType:
        """The arguments dict that is used to define the ClarifyCheck step."""
        ...
    
    @property
    def properties(self):
        """A Properties object representing the output parameters of the ClarifyCheck step."""
        ...
    
    def to_request(self) -> RequestType:
        """Updates the dictionary with cache configuration etc."""
        ...
    


