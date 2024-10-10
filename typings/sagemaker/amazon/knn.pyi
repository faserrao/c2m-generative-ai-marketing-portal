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
class KNN(AmazonAlgorithmEstimatorBase):
    """An index-based algorithm. It uses a non-parametric method for classification or regression.

    For classification problems, the algorithm queries the k points that are closest to the sample
    point and returns the most frequently used label of their class as the predicted label. For
    regression problems, the algorithm queries the k closest points to the sample point and returns
    the average of their feature values as the predicted value.
    """
    repo_name: str = ...
    repo_version: str = ...
    k: hp = ...
    sample_size: hp = ...
    predictor_type: hp = ...
    dimension_reduction_target: hp = ...
    dimension_reduction_type: hp = ...
    index_metric: hp = ...
    index_type: hp = ...
    faiss_index_ivf_nlists: hp = ...
    faiss_index_pq_m: hp = ...
    def __init__(self, role: Optional[Union[str, PipelineVariable]] = ..., instance_count: Optional[Union[int, PipelineVariable]] = ..., instance_type: Optional[Union[str, PipelineVariable]] = ..., k: Optional[int] = ..., sample_size: Optional[int] = ..., predictor_type: Optional[str] = ..., dimension_reduction_type: Optional[str] = ..., dimension_reduction_target: Optional[int] = ..., index_type: Optional[str] = ..., index_metric: Optional[str] = ..., faiss_index_ivf_nlists: Optional[str] = ..., faiss_index_pq_m: Optional[int] = ..., **kwargs) -> None:
        """k-nearest neighbors (KNN) is :class:`Estimator` used for classification and regression.

        This Estimator may be fit via calls to
        :meth:`~sagemaker.amazon.amazon_estimator.AmazonAlgorithmEstimatorBase.fit`.
        It requires Amazon :class:`~sagemaker.amazon.record_pb2.Record` protobuf
        serialized data to be stored in S3. There is an utility
        :meth:`~sagemaker.amazon.amazon_estimator.AmazonAlgorithmEstimatorBase.record_set`
        that can be used to upload data to S3 and creates
        :class:`~sagemaker.amazon.amazon_estimator.RecordSet` to be passed to
        the `fit` call. To learn more about the Amazon protobuf Record class and
        how to prepare bulk data in this format, please consult AWS technical
        documentation:
        https://docs.aws.amazon.com/sagemaker/latest/dg/cdf-training.html After
        this Estimator is fit, model data is stored in S3. The model may be
        deployed to an Amazon SageMaker Endpoint by invoking
        :meth:`~sagemaker.amazon.estimator.EstimatorBase.deploy`. As well as
        deploying an Endpoint, deploy returns a
        :class:`~sagemaker.amazon.knn.KNNPredictor` object that can be used for
        inference calls using the trained model hosted in the SageMaker
        Endpoint. KNN Estimators can be configured by setting hyperparameters.
        The available hyperparameters for KNN are documented below. For further
        information on the AWS KNN algorithm, please consult AWS technical
        documentation: https://docs.aws.amazon.com/sagemaker/latest/dg/knn.html

        Args:
            role (str): An AWS IAM role (either name or full ARN). The Amazon
                SageMaker training jobs and APIs that create Amazon SageMaker
                endpoints use this role to access training data and model
                artifacts. After the endpoint is created, the inference code
                might use the IAM role, if accessing AWS resource.
            instance_count: (int or PipelineVariable): Number of Amazon EC2 instances to use
                for training.
            instance_type (str or PipelineVariable): Type of EC2 instance to use for training,
                for example, 'ml.c4.xlarge'.
            k (int): Required. Number of nearest neighbors.
            sample_size (int): Required. Number of data points to be sampled
                from the training data set.
            predictor_type (str): Required. Type of inference to use on the
                data's labels, allowed values are 'classifier' and 'regressor'.
            dimension_reduction_type (str): Optional. Type of dimension
                reduction technique to use. Valid values: "sign", "fjlt"
            dimension_reduction_target (int): Optional. Target dimension to
                reduce to. Required when dimension_reduction_type is specified.
            index_type (str): Optional. Type of index to use. Valid values are
                "faiss.Flat", "faiss.IVFFlat", "faiss.IVFPQ".
            index_metric (str): Optional. Distance metric to measure between
                points when finding nearest neighbors. Valid values are
                "COSINE", "INNER_PRODUCT", "L2"
            faiss_index_ivf_nlists (str): Optional. Number of centroids to
                construct in the index if index_type is "faiss.IVFFlat" or
                "faiss.IVFPQ".
            faiss_index_pq_m (int): Optional. Number of vector sub-components to
                construct in the index, if index_type is "faiss.IVFPQ".
            **kwargs: base class keyword argument values.

        .. tip::

            You can find additional parameters for initializing this class at
            :class:`~sagemaker.estimator.amazon_estimator.AmazonAlgorithmEstimatorBase` and
            :class:`~sagemaker.estimator.EstimatorBase`.
        """
        ...
    
    def create_model(self, vpc_config_override=..., **kwargs):
        """Return a :class:`~sagemaker.amazon.KNNModel`.

        It references the latest s3 model data produced by this Estimator.

        Args:
            vpc_config_override (dict[str, list[str]]): Optional override for VpcConfig set on
                the model. Default: use subnets and security groups from this Estimator.
                * 'Subnets' (list[str]): List of subnet ids.
                * 'SecurityGroupIds' (list[str]): List of security group ids.
            **kwargs: Additional kwargs passed to the KNNModel constructor.
        """
        ...
    


class KNNPredictor(Predictor):
    """Performs classification or regression prediction from input vectors.

    The implementation of
    :meth:`~sagemaker.predictor.Predictor.predict` in this
    `Predictor` requires a numpy ``ndarray`` as input. The array should
    contain the same number of columns as the feature-dimension of the data used
    to fit the model this Predictor performs inference on.

    :func:`predict` returns a list of
    :class:`~sagemaker.amazon.record_pb2.Record` objects (assuming the default
    recordio-protobuf ``deserializer`` is used), one for each row in
    the input ``ndarray``. The prediction is stored in the ``"predicted_label"``
    key of the ``Record.label`` field.
    """
    def __init__(self, endpoint_name, sagemaker_session=..., serializer=..., deserializer=...) -> None:
        """Function to initialize KNNPredictor.

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
    


class KNNModel(Model):
    """Reference S3 model data created by KNN estimator.

    Calling :meth:`~sagemaker.model.Model.deploy` creates an Endpoint
    and returns :class:`KNNPredictor`.
    """
    def __init__(self, model_data: Union[str, PipelineVariable], role: Optional[str] = ..., sagemaker_session: Optional[Session] = ..., **kwargs) -> None:
        """Function to initialize KNNModel.

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
    


