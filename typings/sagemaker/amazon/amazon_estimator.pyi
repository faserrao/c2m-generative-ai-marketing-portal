"""
This type stub file was generated by pyright.
"""

from typing import Dict, Optional, Union
from sagemaker.amazon.hyperparameter import Hyperparameter as hp
from sagemaker.estimator import EstimatorBase
from sagemaker.workflow.entities import PipelineVariable
from sagemaker.workflow.pipeline_context import runnable_by_pipeline

"""
This type stub file was generated by pyright.
"""
logger = ...
class AmazonAlgorithmEstimatorBase(EstimatorBase):
    """Base class for Amazon first-party Estimator implementations.

    This class isn't intended to be instantiated directly.
    """
    feature_dim: hp = ...
    mini_batch_size: hp = ...
    repo_name: Optional[str] = ...
    repo_version: Optional[str] = ...
    DEFAULT_MINI_BATCH_SIZE: Optional[int] = ...
    def __init__(self, role: Optional[Union[str, PipelineVariable]] = ..., instance_count: Optional[Union[int, PipelineVariable]] = ..., instance_type: Optional[Union[str, PipelineVariable]] = ..., data_location: Optional[str] = ..., enable_network_isolation: Union[bool, PipelineVariable] = ..., **kwargs) -> None:
        """Initialize an AmazonAlgorithmEstimatorBase.

        Args:
            role (str): An AWS IAM role (either name or full ARN). The Amazon
                SageMaker training jobs and APIs that create Amazon SageMaker
                endpoints use this role to access training data and model
                artifacts. After the endpoint is created, the inference code
                might use the IAM role, if it needs to access an AWS resource.
            instance_count (int or PipelineVariable): Number of Amazon EC2 instances to use
                for training. Required.
            instance_type (str or PipelineVariable): Type of EC2 instance to use for training,
                for example, 'ml.c4.xlarge'. Required.
            data_location (str or None): The s3 prefix to upload RecordSet
                objects to, expressed as an S3 url. For example
                "s3://example-bucket/some-key-prefix/". Objects will be saved in
                a unique sub-directory of the specified location. If None, a
                default data location will be used.
            enable_network_isolation (bool or PipelineVariable): Specifies whether container will
                run in network isolation mode. Network isolation mode restricts
                the container access to outside networks (such as the internet).
                Also known as internet-free mode (default: ``False``).
            **kwargs: Additional parameters passed to
                :class:`~sagemaker.estimator.EstimatorBase`.

        .. tip::

            You can find additional parameters for initializing this class at
            :class:`~sagemaker.estimator.EstimatorBase`.
        """
        ...
    
    def training_image_uri(self):
        """Placeholder docstring"""
        ...
    
    def hyperparameters(self):
        """Placeholder docstring"""
        ...
    
    @property
    def data_location(self):
        """Placeholder docstring"""
        ...
    
    @data_location.setter
    def data_location(self, data_location: str):
        """Placeholder docstring"""
        ...
    
    def prepare_workflow_for_training(self, records=..., mini_batch_size=..., job_name=...):
        """Calls _prepare_for_training. Used when setting up a workflow.

        Args:
            records (:class:`~RecordSet`): The records to train this ``Estimator`` on.
            mini_batch_size (int or None): The size of each mini-batch to use when
                training. If ``None``, a default value will be used.
            job_name (str): Name of the training job to be created. If not
                specified, one is generated, using the base name given to the
                constructor if applicable.
        """
        ...
    
    @runnable_by_pipeline
    def fit(self, records: RecordSet, mini_batch_size: Optional[int] = ..., wait: bool = ..., logs: bool = ..., job_name: Optional[str] = ..., experiment_config: Optional[Dict[str, str]] = ...):
        """Fit this Estimator on serialized Record objects, stored in S3.

        ``records`` should be an instance of :class:`~RecordSet`. This
        defines a collection of S3 data files to train this ``Estimator`` on.

        Training data is expected to be encoded as dense or sparse vectors in
        the "values" feature on each Record. If the data is labeled, the label
        is expected to be encoded as a list of scalas in the "values" feature of
        the Record label.

        More information on the Amazon Record format is available at:
        https://docs.aws.amazon.com/sagemaker/latest/dg/cdf-training.html

        See :meth:`~AmazonAlgorithmEstimatorBase.record_set` to construct a
        ``RecordSet`` object from :class:`~numpy.ndarray` arrays.

        Args:
            records (:class:`~RecordSet`): The records to train this ``Estimator`` on
            mini_batch_size (int or None): The size of each mini-batch to use
                when training. If ``None``, a default value will be used.
            wait (bool): Whether the call should wait until the job completes
                (default: True).
            logs (bool): Whether to show the logs produced by the job. Only
                meaningful when wait is True (default: True).
            job_name (str): Training job name. If not specified, the estimator
                generates a default job name, based on the training image name
                and current timestamp.
            experiment_config (dict[str, str]): Experiment management configuration.
                Optionally, the dict can contain four keys:
                'ExperimentName', 'TrialName', 'TrialComponentDisplayName' and 'RunName'.
                The behavior of setting these keys is as follows:
                * If `ExperimentName` is supplied but `TrialName` is not a Trial will be
                automatically created and the job's Trial Component associated with the Trial.
                * If `TrialName` is supplied and the Trial already exists the job's Trial Component
                will be associated with the Trial.
                * If both `ExperimentName` and `TrialName` are not supplied the trial component
                will be unassociated.
                * `TrialComponentDisplayName` is used for display in Studio.
        """
        ...
    
    def record_set(self, train, labels=..., channel=..., encrypt=...):
        """Build a :class:`~RecordSet` from a numpy :class:`~ndarray` matrix and label vector.

        For the 2D ``ndarray`` ``train``, each row is converted to a
        :class:`~Record` object. The vector is stored in the "values" entry of
        the ``features`` property of each Record. If ``labels`` is not None,
        each corresponding label is assigned to the "values" entry of the
        ``labels`` property of each Record.

        The collection of ``Record`` objects are protobuf serialized and
        uploaded to new S3 locations. A manifest file is generated containing
        the list of objects created and also stored in S3.

        The number of S3 objects created is controlled by the
        ``instance_count`` property on this Estimator. One S3 object is
        created per training instance.

        Args:
            train (numpy.ndarray): A 2D numpy array of training data.
            labels (numpy.ndarray): A 1D numpy array of labels. Its length must
                be equal to the number of rows in ``train``.
            channel (str): The SageMaker TrainingJob channel this RecordSet
                should be assigned to.
            encrypt (bool): Specifies whether the objects uploaded to S3 are
                encrypted on the server side using AES-256 (default: ``False``).

        Returns:
            RecordSet: A RecordSet referencing the encoded, uploading training
            and label data.
        """
        ...
    


class RecordSet:
    """Placeholder docstring"""
    def __init__(self, s3_data: Union[str, PipelineVariable], num_records: int, feature_dim: int, s3_data_type: Union[str, PipelineVariable] = ..., channel: Union[str, PipelineVariable] = ...) -> None:
        """A collection of Amazon :class:~`Record` objects serialized and stored in S3.

        Args:
            s3_data (str or PipelineVariable): The S3 location of the training data
            num_records (int): The number of records in the set.
            feature_dim (int): The dimensionality of "values" arrays in the
                Record features, and label (if each Record is labeled).
            s3_data_type (str or PipelineVariable): Valid values: 'S3Prefix', 'ManifestFile'.
                If 'S3Prefix', ``s3_data`` defines a prefix of s3 objects to train
                on. All objects with s3 keys beginning with ``s3_data`` will be
                used to train. If 'ManifestFile', then ``s3_data`` defines a
                single s3 manifest file, listing each s3 object to train on.
            channel (str or PipelineVariable): The SageMaker Training Job channel this RecordSet
                should be bound to
        """
        ...
    
    def __repr__(self):
        """Return an unambiguous representation of this RecordSet"""
        ...
    
    def data_channel(self):
        """Returns dictionary to represent the training data in a channel to use with ``fit()``."""
        ...
    
    def records_s3_input(self):
        """Return a TrainingInput to represent the training data"""
        ...
    


class FileSystemRecordSet:
    """Amazon SageMaker channel configuration for file system data source for Amazon algorithms."""
    def __init__(self, file_system_id, file_system_type, directory_path, num_records, feature_dim, file_system_access_mode=..., channel=...) -> None:
        """Initialize a ``FileSystemRecordSet`` object.

        Args:
            file_system_id (str): An Amazon file system ID starting with 'fs-'.
            file_system_type (str): The type of file system used for the input.
                Valid values: 'EFS', 'FSxLustre'.
            directory_path (str): Absolute or normalized path to the root directory (mount point) in
                the file system. Reference:
                https://docs.aws.amazon.com/efs/latest/ug/mounting-fs.html and
                https://docs.aws.amazon.com/efs/latest/ug/wt1-test.html
            num_records (int): The number of records in the set.
            feature_dim (int): The dimensionality of "values" arrays in the Record features,
                and label (if each Record is labeled).
            file_system_access_mode (str): Permissions for read and write.
                Valid values: 'ro' or 'rw'. Defaults to 'ro'.
            channel (str): The SageMaker Training Job channel this RecordSet should be bound to
        """
        ...
    
    def __repr__(self):
        """Return an unambiguous representation of this RecordSet"""
        ...
    
    def data_channel(self):
        """Return a dictionary to represent the training data in a channel for use with ``fit()``"""
        ...
    


def upload_numpy_to_s3_shards(num_shards, s3, bucket, key_prefix, array, labels=..., encrypt=...):
    """Upload the training ``array`` and ``labels`` arrays to ``num_shards``.

    S3 objects, stored in "s3:// ``bucket`` / ``key_prefix`` /". Optionally
    ``encrypt`` the S3 objects using AES-256.

    Args:
        num_shards:
        s3:
        bucket:
        key_prefix:
        array:
        labels:
        encrypt:
    """
    ...

def get_image_uri(region_name, repo_name, repo_version=...):
    """Deprecated method. Please use sagemaker.image_uris.retrieve().

    Args:
        region_name: name of the region
        repo_name: name of the repo (e.g. xgboost)
        repo_version: version of the repo

    Returns:
        the image uri
    """
    ...

