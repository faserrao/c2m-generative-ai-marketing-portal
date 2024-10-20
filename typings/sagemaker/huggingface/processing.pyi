"""
This type stub file was generated by pyright.
"""

from typing import Dict, List, Optional, Union
from sagemaker.session import Session
from sagemaker.network import NetworkConfig
from sagemaker.processing import FrameworkProcessor
from sagemaker.huggingface.estimator import HuggingFace
from sagemaker.workflow.entities import PipelineVariable

"""This module contains code related to HuggingFace Processors which are used for Processing jobs.

These jobs let customers perform data pre-processing, post-processing, feature engineering,
data validation, and model evaluation and interpretation on SageMaker.
"""
class HuggingFaceProcessor(FrameworkProcessor):
    """Handles Amazon SageMaker processing tasks for jobs using HuggingFace containers."""
    estimator_cls = HuggingFace
    def __init__(self, role: Optional[Union[str, PipelineVariable]] = ..., instance_count: Union[int, PipelineVariable] = ..., instance_type: Union[str, PipelineVariable] = ..., transformers_version: Optional[str] = ..., tensorflow_version: Optional[str] = ..., pytorch_version: Optional[str] = ..., py_version: str = ..., image_uri: Optional[Union[str, PipelineVariable]] = ..., command: Optional[List[str]] = ..., volume_size_in_gb: Union[int, PipelineVariable] = ..., volume_kms_key: Optional[Union[str, PipelineVariable]] = ..., output_kms_key: Optional[Union[str, PipelineVariable]] = ..., code_location: Optional[str] = ..., max_runtime_in_seconds: Optional[Union[int, PipelineVariable]] = ..., base_job_name: Optional[str] = ..., sagemaker_session: Optional[Session] = ..., env: Optional[Dict[str, Union[str, PipelineVariable]]] = ..., tags: Optional[List[Dict[str, Union[str, PipelineVariable]]]] = ..., network_config: Optional[NetworkConfig] = ...) -> None:
        """This processor executes a Python script in a HuggingFace execution environment.

        Unless ``image_uri`` is specified, the environment is an Amazon-built Docker container
        that executes functions defined in the supplied ``code`` Python script.

        The arguments have the same meaning as in ``FrameworkProcessor``, with the following
        exceptions.

        Args:
            transformers_version (str): Transformers version you want to use for
                executing your model training code. Defaults to ``None``. Required unless
                ``image_uri`` is provided. The current supported version is ``4.4.2``.
            tensorflow_version (str): TensorFlow version you want to use for
                executing your model training code. Defaults to ``None``. Required unless
                ``pytorch_version`` is provided. The current supported version is ``2.4.1``.
            pytorch_version (str): PyTorch version you want to use for
                executing your model training code. Defaults to ``None``. Required unless
                ``tensorflow_version`` is provided. The current supported version is ``1.6.0``.
            py_version (str): Python version you want to use for executing your model training
                code. Defaults to ``None``. Required unless ``image_uri`` is provided.  If
                using PyTorch, the current supported version is ``py36``. If using TensorFlow,
                the current supported version is ``py37``.

        .. tip::

            You can find additional parameters for initializing this class at
            :class:`~sagemaker.processing.FrameworkProcessor`.
        """
        ...
    


