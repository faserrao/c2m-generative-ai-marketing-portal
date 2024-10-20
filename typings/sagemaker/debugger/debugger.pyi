"""
This type stub file was generated by pyright.
"""

import attr
from abc import ABC
from typing import Dict, List, Optional, Union
from sagemaker.workflow.entities import PipelineVariable

"""
This type stub file was generated by pyright.
"""
framework_name = ...
detailed_framework_name = ...
DEBUGGER_FLAG = ...
class DetailedProfilerProcessingJobConfig:
    """ProfilerRule like class.

    Serves as a vehicle to pass info through to the processing instance.

    """
    def __init__(self) -> None:
        ...
    


def get_rule_container_image_uri(name, region):
    """Return the Debugger rule image URI for the given AWS Region.

    For a full list of rule image URIs,
    see `Use Debugger Docker Images for Built-in or Custom Rules
    <https://docs.aws.amazon.com/sagemaker/latest/dg/debugger-docker-images-rules.html>`_.

    Args:
        region (str): A string of AWS Region. For example, ``'us-east-1'``.

    Returns:
        str: Formatted image URI for the given AWS Region and the rule container type.

    """
    ...

def get_default_profiler_processing_job(instance_type=..., volume_size_in_gb=...):
    """Return the default profiler processing job (a rule) with a unique name.

    Returns:
        sagemaker.debugger.ProfilerRule: The instance of the built-in ProfilerRule.

    """
    ...

@attr.s
class RuleBase(ABC):
    """The SageMaker Debugger rule base class that cannot be instantiated directly.

    .. tip::

        Debugger rule classes inheriting this RuleBase class are
        :class:`~sagemaker.debugger.Rule` and :class:`~sagemaker.debugger.ProfilerRule`.
        Do not directly use the rule base class to instantiate a SageMaker Debugger rule.
        Use the :class:`~sagemaker.debugger.Rule` classmethods for debugging
        and the :class:`~sagemaker.debugger.ProfilerRule` classmethods for profiling.

    Attributes:
        name (str): The name of the rule.
        image_uri (str): The image URI to use the rule.
        instance_type (str): Type of EC2 instance to use. For example, 'ml.c4.xlarge'.
        container_local_output_path (str): The local path to store the Rule output.
        s3_output_path (str): The location in S3 to store the output.
        volume_size_in_gb (int): Size in GB of the EBS volume to use for storing data.
        rule_parameters (dict): A dictionary of parameters for the rule.

    """
    name = ...
    image_uri = ...
    instance_type = ...
    container_local_output_path = ...
    s3_output_path = ...
    volume_size_in_gb = ...
    rule_parameters = ...


class Rule(RuleBase):
    """The SageMaker Debugger Rule class configures *debugging* rules to debug your training job.

    The debugging rules analyze tensor outputs from your training job
    and monitor conditions that are critical for the success of the training
    job.

    SageMaker Debugger comes pre-packaged with built-in *debugging* rules.
    For example, the debugging rules can detect whether gradients are getting too large or
    too small, or if a model is overfitting.
    For a full list of built-in rules for debugging, see
    `List of Debugger Built-in Rules
    <https://docs.aws.amazon.com/sagemaker/latest/dg/debugger-built-in-rules.html>`_.
    You can also write your own rules using the custom rule classmethod.

    """
    def __init__(self, name, image_uri, instance_type, container_local_output_path, s3_output_path, volume_size_in_gb, rule_parameters, collections_to_save, actions=...) -> None:
        """Configure the debugging rules using the following classmethods.

        .. tip::
            Use the following ``Rule.sagemaker`` class method for built-in debugging rules
            or the ``Rule.custom`` class method for custom debugging rules.
            Do not directly use the :class:`~sagemaker.debugger.Rule`
            initialization method.

        """
        ...
    
    @classmethod
    def sagemaker(cls, base_config, name=..., container_local_output_path=..., s3_output_path=..., other_trials_s3_input_paths=..., rule_parameters=..., collections_to_save=..., actions=...):
        """Initialize a ``Rule`` object for a *built-in* debugging rule.

        Args:
            base_config (dict): Required. This is the base rule config dictionary returned from the
                :class:`~sagemaker.debugger.rule_configs` method.
                For example, ``rule_configs.dead_relu()``.
                For a full list of built-in rules for debugging, see
                `List of Debugger Built-in Rules
                <https://docs.aws.amazon.com/sagemaker/latest/dg/debugger-built-in-rules.html>`_.
            name (str): Optional. The name of the debugger rule. If one is not provided,
                the name of the base_config will be used.
            container_local_output_path (str): Optional. The local path in the rule processing
                container.
            s3_output_path (str): Optional. The location in Amazon S3 to store the output tensors.
                The default Debugger output path for debugging data is created under the
                default output path of the :class:`~sagemaker.estimator.Estimator` class.
                For example,
                s3://sagemaker-<region>-<12digit_account_id>/<training-job-name>/debug-output/.
            other_trials_s3_input_paths ([str]): Optional. The Amazon S3 input paths
                of other trials to use the SimilarAcrossRuns rule.
            rule_parameters (dict): Optional. A dictionary of parameters for the rule.
            collections_to_save (:class:`~sagemaker.debugger.CollectionConfig`):
                Optional. A list
                of :class:`~sagemaker.debugger.CollectionConfig` objects to be saved.

        Returns:
            :class:`~sagemaker.debugger.Rule`: An instance of the built-in rule.

        **Example of how to create a built-in rule instance:**

        .. code-block:: python

            from sagemaker.debugger import Rule, rule_configs

            built_in_rules = [
                Rule.sagemaker(rule_configs.built_in_rule_name_in_pysdk_format_1()),
                Rule.sagemaker(rule_configs.built_in_rule_name_in_pysdk_format_2()),
                ...
                Rule.sagemaker(rule_configs.built_in_rule_name_in_pysdk_format_n())
            ]

        You need to replace the ``built_in_rule_name_in_pysdk_format_*`` with the
        names of built-in rules. You can find the rule names at `List of Debugger Built-in
        Rules <https://docs.aws.amazon.com/sagemaker/latest/dg/debugger-built-in-rules.html>`_.

        **Example of creating a built-in rule instance with adjusting parameter values:**

        .. code-block:: python

            from sagemaker.debugger import Rule, rule_configs

            built_in_rules = [
                Rule.sagemaker(
                    base_config=rule_configs.built_in_rule_name_in_pysdk_format(),
                    rule_parameters={
                            "key": "value"
                    }
                    collections_to_save=[
                        CollectionConfig(
                            name="tensor_collection_name",
                            parameters={
                                "key": "value"
                            }
                        )
                    ]
                )
            ]

        For more information about setting up the ``rule_parameters`` parameter,
        see `List of Debugger Built-in
        Rules <https://docs.aws.amazon.com/sagemaker/latest/dg/debugger-built-in-rules.html>`_.

        For more information about setting up the ``collections_to_save`` parameter,
        see the :class:`~sagemaker.debugger.CollectionConfig` class.

        """
        ...
    
    @classmethod
    def custom(cls, name: str, image_uri: Union[str, PipelineVariable], instance_type: Union[str, PipelineVariable], volume_size_in_gb: Union[int, PipelineVariable], source: Optional[str] = ..., rule_to_invoke: Optional[Union[str, PipelineVariable]] = ..., container_local_output_path: Optional[Union[str, PipelineVariable]] = ..., s3_output_path: Optional[Union[str, PipelineVariable]] = ..., other_trials_s3_input_paths: Optional[List[Union[str, PipelineVariable]]] = ..., rule_parameters: Optional[Dict[str, Union[str, PipelineVariable]]] = ..., collections_to_save: Optional[List[CollectionConfig]] = ..., actions=...):
        """Initialize a ``Rule`` object for a *custom* debugging rule.

        You can create a custom rule that analyzes tensors emitted
        during the training of a model
        and monitors conditions that are critical for the success of a training
        job. For more information, see `Create Debugger Custom Rules for Training Job
        Analysis
        <https://docs.aws.amazon.com/sagemaker/latest/dg/debugger-custom-rules.html>`_.

        Args:
            name (str): Required. The name of the debugger rule.
            image_uri (str or PipelineVariable): Required. The URI of the image to
                be used by the debugger rule.
            instance_type (str or PipelineVariable): Required. Type of EC2 instance to use,
                for example, 'ml.c4.xlarge'.
            volume_size_in_gb (int or PipelineVariable): Required. Size in GB of the
                EBS volume to use for storing data.
            source (str): Optional. A source file containing a rule to invoke. If provided,
                you must also provide rule_to_invoke. This can either be an S3 uri or
                a local path.
            rule_to_invoke (str or PipelineVariable): Optional. The name of the rule to
                invoke within the source. If provided, you must also provide source.
            container_local_output_path (str or PipelineVariable): Optional. The local path
                in the container.
            s3_output_path (str or PipelineVariable): Optional. The location in Amazon S3
                to store the output tensors.
                The default Debugger output path for debugging data is created under the
                default output path of the :class:`~sagemaker.estimator.Estimator` class.
                For example,
                s3://sagemaker-<region>-<12digit_account_id>/<training-job-name>/debug-output/.
            other_trials_s3_input_paths (list[str] or list[PipelineVariable]: Optional.
                The Amazon S3 input paths of other trials to use the SimilarAcrossRuns rule.
            rule_parameters (dict[str, str] or dict[str, PipelineVariable]): Optional.
                A dictionary of parameters for the rule.
            collections_to_save ([sagemaker.debugger.CollectionConfig]): Optional. A list
                of :class:`~sagemaker.debugger.CollectionConfig` objects to be saved.

        Returns:
            :class:`~sagemaker.debugger.Rule`: The instance of the custom rule.

        """
        ...
    
    def prepare_actions(self, training_job_name):
        """Prepare actions for Debugger Rule.

        Args:
            training_job_name (str): The training job name. To be set as the default training job
                prefix for the StopTraining action if it is specified.
        """
        ...
    
    def to_debugger_rule_config_dict(self):
        """Generates a request dictionary using the parameters provided when initializing object.

        Returns:
            dict: An portion of an API request as a dictionary.

        """
        ...
    


class ProfilerRule(RuleBase):
    """The SageMaker Debugger ProfilerRule class configures *profiling* rules.

    SageMaker Debugger profiling rules automatically analyze
    hardware system resource utilization and framework metrics of a
    training job to identify performance bottlenecks.

    SageMaker Debugger comes pre-packaged with built-in *profiling* rules.
    For example, the profiling rules can detect if GPUs are underutilized due to CPU bottlenecks or
    IO bottlenecks.
    For a full list of built-in rules for debugging, see
    `List of Debugger Built-in Rules <https://docs.aws.amazon.com/sagemaker/latest/dg/debugger-built-in-rules.html>`_.
    You can also write your own profiling rules using the Amazon SageMaker
    Debugger APIs.

    .. tip::
        Use the following ``ProfilerRule.sagemaker`` class method for built-in profiling rules
        or the ``ProfilerRule.custom`` class method for custom profiling rules.
        Do not directly use the `Rule` initialization method.

    """
    @classmethod
    def sagemaker(cls, base_config, name=..., container_local_output_path=..., s3_output_path=..., instance_type=..., volume_size_in_gb=...):
        """Initialize a ``ProfilerRule`` object for a *built-in* profiling rule.

        The rule analyzes system and framework metrics of a given
        training job to identify performance bottlenecks.

        Args:
            base_config (rule_configs.ProfilerRule): The base rule configuration object
                returned from the ``rule_configs`` method.
                For example, 'rule_configs.ProfilerReport()'.
                For a full list of built-in rules for debugging, see
                `List of Debugger Built-in Rules
                <https://docs.aws.amazon.com/sagemaker/latest/dg/debugger-built-in-rules.html>`_.

            name (str): The name of the profiler rule. If one is not provided,
                the name of the base_config will be used.
            container_local_output_path (str): The path in the container.
            s3_output_path (str): The location in Amazon S3 to store the profiling output data.
                The default Debugger output path for profiling data is created under the
                default output path of the :class:`~sagemaker.estimator.Estimator` class.
                For example,
                s3://sagemaker-<region>-<12digit_account_id>/<training-job-name>/profiler-output/.

        Returns:
            :class:`~sagemaker.debugger.ProfilerRule`:
            The instance of the built-in ProfilerRule.

        """
        ...
    
    @classmethod
    def custom(cls, name, image_uri, instance_type, volume_size_in_gb, source=..., rule_to_invoke=..., container_local_output_path=..., s3_output_path=..., rule_parameters=...):
        """Initialize a ``ProfilerRule`` object for a *custom* profiling rule.

        You can create a rule that
        analyzes system and framework metrics emitted during the training of a model and
        monitors conditions that are critical for the success of a
        training job.

        Args:
            name (str): The name of the profiler rule.
            image_uri (str): The URI of the image to be used by the proflier rule.
            instance_type (str): Type of EC2 instance to use, for example,
                'ml.c4.xlarge'.
            volume_size_in_gb (int): Size in GB of the EBS volume
                to use for storing data.
            source (str): A source file containing a rule to invoke. If provided,
                you must also provide rule_to_invoke. This can either be an S3 uri or
                a local path.
            rule_to_invoke (str): The name of the rule to invoke within the source.
                If provided, you must also provide the source.
            container_local_output_path (str): The path in the container.
            s3_output_path (str): The location in Amazon S3 to store the output.
                The default Debugger output path for profiling data is created under the
                default output path of the :class:`~sagemaker.estimator.Estimator` class.
                For example,
                s3://sagemaker-<region>-<12digit_account_id>/<training-job-name>/profiler-output/.
            rule_parameters (dict): A dictionary of parameters for the rule.

        Returns:
            :class:`~sagemaker.debugger.ProfilerRule`:
            The instance of the custom ProfilerRule.

        """
        ...
    
    def to_profiler_rule_config_dict(self):
        """Generates a request dictionary using the parameters provided when initializing object.

        Returns:
            dict: An portion of an API request as a dictionary.

        """
        ...
    


class DebuggerHookConfig:
    """Create a Debugger hook configuration object to save the tensor for debugging.

    DebuggerHookConfig provides options to customize how debugging
    information is emitted and saved. This high-level DebuggerHookConfig class
    runs based on the `smdebug.SaveConfig
    <https://github.com/awslabs/sagemaker-debugger/blob/master/docs/
    api.md#saveconfig>`_ class.

    """
    def __init__(self, s3_output_path: Optional[Union[str, PipelineVariable]] = ..., container_local_output_path: Optional[Union[str, PipelineVariable]] = ..., hook_parameters: Optional[Dict[str, Union[str, PipelineVariable]]] = ..., collection_configs: Optional[List[CollectionConfig]] = ...) -> None:
        """Initialize the DebuggerHookConfig instance.

        Args:
            s3_output_path (str or PipelineVariable): Optional. The location in Amazon S3 to
                store the output tensors. The default Debugger output path is created under the
                default output path of the :class:`~sagemaker.estimator.Estimator` class.
                For example,
                s3://sagemaker-<region>-<12digit_account_id>/<training-job-name>/debug-output/.
            container_local_output_path (str or PipelineVariable): Optional. The local path
                in the container.
            hook_parameters (dict[str, str] or dict[str, PipelineVariable]): Optional.
                A dictionary of parameters.
            collection_configs ([sagemaker.debugger.CollectionConfig]): Required. A list
                of :class:`~sagemaker.debugger.CollectionConfig` objects to be saved
                at the **s3_output_path**.

        **Example of creating a DebuggerHookConfig object:**

        .. code-block:: python

            from sagemaker.debugger import CollectionConfig, DebuggerHookConfig

            collection_configs=[
                CollectionConfig(name="tensor_collection_1")
                CollectionConfig(name="tensor_collection_2")
                ...
                CollectionConfig(name="tensor_collection_n")
            ]

            hook_config = DebuggerHookConfig(
                collection_configs=collection_configs
            )

        """
        ...
    


class TensorBoardOutputConfig:
    """Create a tensor ouput configuration object for debugging visualizations on TensorBoard."""
    def __init__(self, s3_output_path: Union[str, PipelineVariable], container_local_output_path: Optional[Union[str, PipelineVariable]] = ...) -> None:
        """Initialize the TensorBoardOutputConfig instance.

        Args:
            s3_output_path (str or PipelineVariable): Optional. The location in Amazon S3
                to store the output.
            container_local_output_path (str or PipelineVariable): Optional. The local path
                in the container.

        """
        ...
    


class CollectionConfig:
    """Creates tensor collections for SageMaker Debugger."""
    def __init__(self, name: Union[str, PipelineVariable], parameters: Optional[Dict[str, Union[str, PipelineVariable]]] = ...) -> None:
        """Constructor for collection configuration.

        Args:
            name (str or PipelineVariable): Required. The name of the collection configuration.
            parameters (dict[str, str] or dict[str, PipelineVariable]): Optional. The parameters
                for the collection configuration.

        **Example of creating a CollectionConfig object:**

        .. code-block:: python

            from sagemaker.debugger import CollectionConfig

            collection_configs=[
                CollectionConfig(name="tensor_collection_1")
                CollectionConfig(name="tensor_collection_2")
                ...
                CollectionConfig(name="tensor_collection_n")
            ]

        For a full list of Debugger built-in collection, see
        `Debugger Built in Collections
        <https://github.com/awslabs/sagemaker-debugger/blob/master
        /docs/api.md#built-in-collections>`_.

        **Example of creating a CollectionConfig object with parameter adjustment:**

        You can use the following CollectionConfig template in two ways:
        (1) to adjust the parameters of the built-in tensor collections,
        and (2) to create custom tensor collections.

        If you put the built-in collection names to the ``name`` parameter,
        ``CollectionConfig`` takes it to match the built-in collections and adjust parameters.
        If you specify a new name to the ``name`` parameter,
        ``CollectionConfig`` creates a new tensor collection, and you must use
        ``include_regex`` parameter to specify regex of tensors you want to collect.

        .. code-block:: python

            from sagemaker.debugger import CollectionConfig

            collection_configs=[
                CollectionConfig(
                    name="tensor_collection",
                    parameters={
                        "key_1": "value_1",
                        "key_2": "value_2"
                        ...
                        "key_n": "value_n"
                    }
                )
            ]

        The following list shows the available CollectionConfig parameters.

        +--------------------------+---------------------------------------------------------+
        | Parameter Key            | Descriptions                                            |
        +==========================+=========================================================+
        |``include_regex``         |  Specify a list of regex patterns of tensors to save.   |
        |                          |                                                         |
        |                          |  Tensors whose names match these patterns will be saved.|
        +--------------------------+---------------------------------------------------------+
        |``save_histogram``        |  Set *True* if want to save histogram output data for   |
        |                          |                                                         |
        |                          |  TensorFlow visualization.                              |
        +--------------------------+---------------------------------------------------------+
        |``reductions``            |  Specify certain reduction values of tensors.           |
        |                          |                                                         |
        |                          |  This helps reduce the amount of data saved and         |
        |                          |                                                         |
        |                          |  increase training speed.                               |
        |                          |                                                         |
        |                          |  Available values are ``min``, ``max``, ``median``,     |
        |                          |                                                         |
        |                          |  ``mean``, ``std``, ``variance``, ``sum``, and ``prod``.|
        +--------------------------+---------------------------------------------------------+
        |``save_interval``         |  Specify how often to save tensors in steps.            |
        |                          |                                                         |
        |``train.save_interval``   |  You can also specify the save intervals                |
        |                          |                                                         |
        |``eval.save_interval``    |  in TRAIN, EVAL, PREDICT, and GLOBAL modes.             |
        |                          |                                                         |
        |``predict.save_interval`` |  The default value is 500 steps.                        |
        |                          |                                                         |
        |``global.save_interval``  |                                                         |
        +--------------------------+---------------------------------------------------------+
        |``save_steps``            |  Specify the exact step numbers to save tensors.        |
        |                          |                                                         |
        |``train.save_steps``      |  You can also specify the save steps                    |
        |                          |                                                         |
        |``eval.save_steps``       |  in TRAIN, EVAL, PREDICT, and GLOBAL modes.             |
        |                          |                                                         |
        |``predict.save_steps``    |                                                         |
        |                          |                                                         |
        |``global.save_steps``     |                                                         |
        +--------------------------+---------------------------------------------------------+
        |``start_step``            |  Specify the exact start step to save tensors.          |
        |                          |                                                         |
        |``train.start_step``      |  You can also specify the start steps                   |
        |                          |                                                         |
        |``eval.start_step``       |  in TRAIN, EVAL, PREDICT, and GLOBAL modes.             |
        |                          |                                                         |
        |``predict.start_step``    |                                                         |
        |                          |                                                         |
        |``global.start_step``     |                                                         |
        +--------------------------+---------------------------------------------------------+
        |``end_step``              |  Specify the exact end step to save tensors.            |
        |                          |                                                         |
        |``train.end_step``        |  You can also specify the end steps                     |
        |                          |                                                         |
        |``eval.end_step``         |  in TRAIN, EVAL, PREDICT, and GLOBAL modes.             |
        |                          |                                                         |
        |``predict.end_step``      |                                                         |
        |                          |                                                         |
        |``global.end_step``       |                                                         |
        +--------------------------+---------------------------------------------------------+

        For example, the following code shows how to control the save_interval parameters
        of the built-in ``losses`` tensor collection. With the following collection configuration,
        Debugger collects loss values every 100 steps from training loops and every 10 steps
        from evaluation loops.

        .. code-block:: python

            collection_configs=[
                CollectionConfig(
                    name="losses",
                    parameters={
                        "train.save_interval": "100",
                        "eval.save_interval": "10"
                    }
                )
            ]

        """
        ...
    
    def __eq__(self, other) -> bool:
        """Equal method override.

        Args:
            other: Object to test equality against.

        """
        ...
    
    def __ne__(self, other) -> bool:
        """Not-equal method override.

        Args:
            other: Object to test equality against.

        """
        ...
    
    def __hash__(self) -> int:
        """Hash method override."""
        ...
    


