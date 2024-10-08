"""
This type stub file was generated by pyright.
"""

from typing import Optional, Union
from sagemaker.amazon.amazon_estimator import AmazonAlgorithmEstimatorBase
from sagemaker.amazon.hyperparameter import Hyperparameter as hp
from sagemaker.predictor import Predictor
from sagemaker.model import Model
from sagemaker.session import Session
from sagemaker.workflow.entities import PipelineVariable

"""
This type stub file was generated by pyright.
"""
class PCA(AmazonAlgorithmEstimatorBase):
    """An unsupervised machine learning algorithm to reduce feature dimensionality.

    As a result, number of features within a dataset is reduced but the dataset still
    retain as much information as possible.
    """
    repo_name: str = ...
    repo_version: str = ...
    DEFAULT_MINI_BATCH_SIZE: int = ...
    num_components: hp = ...
    algorithm_mode: hp = ...
    subtract_mean: hp = ...
    extra_components: hp = ...
    def __init__(self, role: Optional[Union[str, PipelineVariable]] = ..., instance_count: Optional[Union[int, PipelineVariable]] = ..., instance_type: Optional[Union[str, PipelineVariable]] = ..., num_components: Optional[int] = ..., algorithm_mode: Optional[str] = ..., subtract_mean: Optional[bool] = ..., extra_components: Optional[int] = ..., **kwargs) -> None:
        """A Principal Components Analysis (PCA)

        :class:`~sagemaker.amazon.amazon_estimator.AmazonAlgorithmEstimatorBase`.

        This Estimator may be fit via calls to
        :meth:`~sagemaker.amazon.amazon_estimator.AmazonAlgorithmEstimatorBase.fit_ndarray`
        or
        :meth:`~sagemaker.amazon.amazon_estimator.AmazonAlgorithmEstimatorBase.fit`.
        The former allows a PCA model to be fit on a 2-dimensional numpy array.
        The latter requires Amazon :class:`~sagemaker.amazon.record_pb2.Record`
        protobuf serialized data to be stored in S3.

        To learn more about the Amazon protobuf Record class and how to
        prepare bulk data in this format, please consult AWS technical
        documentation:
        https://docs.aws.amazon.com/sagemaker/latest/dg/cdf-training.html

        After this Estimator is fit, model data is stored in S3. The model
        may be deployed to an Amazon SageMaker Endpoint by invoking
        :meth:`~sagemaker.amazon.estimator.EstimatorBase.deploy`. As well as
        deploying an Endpoint, deploy returns a
        :class:`~sagemaker.amazon.pca.PCAPredictor` object that can be used to
        project input vectors to the learned lower-dimensional representation,
        using the trained PCA model hosted in the SageMaker Endpoint.

        PCA Estimators can be configured by setting hyperparameters. The
        available hyperparameters for PCA are documented below. For further
        information on the AWS PCA algorithm, please consult AWS technical
        documentation: https://docs.aws.amazon.com/sagemaker/latest/dg/pca.html

        This Estimator uses Amazon SageMaker PCA to perform training and host
        deployed models. To learn more about Amazon SageMaker PCA, please read:
        https://docs.aws.amazon.com/sagemaker/latest/dg/how-pca-works.html

        Args:
            role (str): An AWS IAM role (either name or full ARN). The Amazon
                SageMaker training jobs and APIs that create Amazon SageMaker
                endpoints use this role to access training data and model
                artifacts. After the endpoint is created, the inference code
                might use the IAM role, if accessing AWS resource.
            instance_count (int or PipelineVariable): Number of Amazon EC2 instances to use
                for training.
            instance_type (str or PipelineVariable): Type of EC2 instance to use for training,
                for example, 'ml.c4.xlarge'.
            num_components (int): The number of principal components. Must be
                greater than zero.
            algorithm_mode (str): Mode for computing the principal components.
                One of 'regular' or 'randomized'.
            subtract_mean (bool): Whether the data should be unbiased both
                during train and at inference.
            extra_components (int): As the value grows larger, the solution
                becomes more accurate but the runtime and memory consumption
                increase linearly. If this value is unset or set to -1, then a
                default value equal to the maximum of 10 and num_components will
                be used. Valid for randomized mode only.
            **kwargs: base class keyword argument values.

        .. tip::

            You can find additional parameters for initializing this class at
            :class:`~sagemaker.estimator.amazon_estimator.AmazonAlgorithmEstimatorBase` and
            :class:`~sagemaker.estimator.EstimatorBase`.
        """
        ...
    
    def create_model(self, vpc_config_override=..., **kwargs):
        """Return a :class:`~sagemaker.amazon.pca.PCAModel`.

        It references the latest s3 model data produced by this Estimator.

        Args:
            vpc_config_override (dict[str, list[str]]): Optional override for VpcConfig set on
                the model. Default: use subnets and security groups from this Estimator.
                * 'Subnets' (list[str]): List of subnet ids.
                * 'SecurityGroupIds' (list[str]): List of security group ids.
            **kwargs: Additional kwargs passed to the PCAModel constructor.
        """
        ...
    


class PCAPredictor(Predictor):
    """Transforms input vectors to lower-dimesional representations.

    The implementation of
    :meth:`~sagemaker.predictor.Predictor.predict` in this
    `Predictor` requires a numpy ``ndarray`` as input. The array should
    contain the same number of columns as the feature-dimension of the data used
    to fit the model this Predictor performs inference on.

    :meth:`predict()` returns a list of
    :class:`~sagemaker.amazon.record_pb2.Record` objects (assuming the default
    recordio-protobuf ``deserializer`` is used), one for each row in
    the input ``ndarray``. The lower dimension vector result is stored in the
    ``projection`` key of the ``Record.label`` field.
    """
    def __init__(self, endpoint_name, sagemaker_session=..., serializer=..., deserializer=...) -> None:
        """Initialization for PCAPredictor.

        Args:
            endpoint_name (str): Name of the Amazon SageMaker endpoint to which
                requests are sent.
            sagemaker_session (sagemaker.session.Session): A SageMaker Session
                object, used for SageMaker interactions (default: None). If not
                specified, one is created using the default AWS configuration
                chain.
            serializer (sagemaker.serializers.BaseSerializer): Optional. Default
                serializes input data to x-recordio-protobuf format.
            deserializer (sagemaker.deserializers.BaseDeserializer): Optional.
                Default parses responses from x-recordio-protobuf format.
        """
        ...
    


class PCAModel(Model):
    """Reference PCA s3 model data.

    Calling :meth:`~sagemaker.model.Model.deploy` creates an Endpoint and return a
    Predictor that transforms vectors to a lower-dimensional representation.
    """
    def __init__(self, model_data: Union[str, PipelineVariable], role: Optional[str] = ..., sagemaker_session: Optional[Session] = ..., **kwargs) -> None:
        """Initialization for PCAModel.

        Args:
            model_data (str or PipelineVariable): The S3 location of a SageMaker model data
                ``.tar.gz`` file.
            role (str): An AWS IAM role (either name or full ARN). The Amazon
                SageMaker training jobs and APIs that create Amazon SageMaker
                endpoints use this role to access training data and model
                artifacts. After the endpoint is created, the inference code
                might use the IAM role, if it needs to access an AWS resource.
            sagemaker_session (sagemaker.session.Session): Session object which
                manages interactions with Amazon SageMaker APIs and any other
                AWS services needed. If not specified, the estimator creates one
                using the default AWS configuration chain.
            **kwargs: Keyword arguments passed to the ``FrameworkModel``
                initializer.
        """
        ...
    


