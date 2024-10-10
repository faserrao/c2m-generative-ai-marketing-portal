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
class FactorizationMachines(AmazonAlgorithmEstimatorBase):
    """A supervised learning algorithm used in classification and regression.

    Factorization Machines combine the advantages of Support Vector Machines
    with factorization models. It is an extension of a linear model that is
    designed to capture interactions between features within high dimensional
    sparse datasets economically.
    """
    repo_name: str = ...
    repo_version: str = ...
    num_factors: hp = ...
    predictor_type: hp = ...
    epochs: hp = ...
    clip_gradient: hp = ...
    eps: hp = ...
    rescale_grad: hp = ...
    bias_lr: hp = ...
    linear_lr: hp = ...
    factors_lr: hp = ...
    bias_wd: hp = ...
    linear_wd: hp = ...
    factors_wd: hp = ...
    bias_init_method: hp = ...
    bias_init_scale: hp = ...
    bias_init_sigma: hp = ...
    bias_init_value: hp = ...
    linear_init_method: hp = ...
    linear_init_scale: hp = ...
    linear_init_sigma: hp = ...
    linear_init_value: hp = ...
    factors_init_method: hp = ...
    factors_init_scale: hp = ...
    factors_init_sigma: hp = ...
    factors_init_value: hp = ...
    def __init__(self, role: Optional[Union[str, PipelineVariable]] = ..., instance_count: Optional[Union[int, PipelineVariable]] = ..., instance_type: Optional[Union[str, PipelineVariable]] = ..., num_factors: Optional[int] = ..., predictor_type: Optional[str] = ..., epochs: Optional[int] = ..., clip_gradient: Optional[float] = ..., eps: Optional[float] = ..., rescale_grad: Optional[float] = ..., bias_lr: Optional[float] = ..., linear_lr: Optional[float] = ..., factors_lr: Optional[float] = ..., bias_wd: Optional[float] = ..., linear_wd: Optional[float] = ..., factors_wd: Optional[float] = ..., bias_init_method: Optional[str] = ..., bias_init_scale: Optional[float] = ..., bias_init_sigma: Optional[float] = ..., bias_init_value: Optional[float] = ..., linear_init_method: Optional[str] = ..., linear_init_scale: Optional[float] = ..., linear_init_sigma: Optional[float] = ..., linear_init_value: Optional[float] = ..., factors_init_method: Optional[str] = ..., factors_init_scale: Optional[float] = ..., factors_init_sigma: Optional[float] = ..., factors_init_value: Optional[float] = ..., **kwargs) -> None:
        """Factorization Machines is :class:`Estimator` for general-purpose supervised learning.

        Amazon SageMaker Factorization Machines is a general-purpose
        supervised learning algorithm that you can use for both classification
        and regression tasks. It is an extension of a linear model that is
        designed to parsimoniously capture interactions between features within
        high dimensional sparse datasets.

        This Estimator may be fit via calls to
        :meth:`~sagemaker.amazon.amazon_estimator.AmazonAlgorithmEstimatorBase.fit`.
        It requires Amazon :class:`~sagemaker.amazon.record_pb2.Record` protobuf
        serialized data to be stored in S3. There is an utility
        :meth:`~sagemaker.amazon.amazon_estimator.AmazonAlgorithmEstimatorBase.record_set`
        that can be used to upload data to S3 and creates
        :class:`~sagemaker.amazon.amazon_estimator.RecordSet` to be passed to
        the `fit` call.

        To learn more about the Amazon protobuf Record class and how to
        prepare bulk data in this format, please consult AWS technical
        documentation:
        https://docs.aws.amazon.com/sagemaker/latest/dg/cdf-training.html

        After this Estimator is fit, model data is stored in S3. The model
        may be deployed to an Amazon SageMaker Endpoint by invoking
        :meth:`~sagemaker.amazon.estimator.EstimatorBase.deploy`. As well as
        deploying an Endpoint, deploy returns a
        :class:`~sagemaker.amazon.pca.FactorizationMachinesPredictor` object
        that can be used for inference calls using the trained model hosted in
        the SageMaker Endpoint.

        FactorizationMachines Estimators can be configured by setting
        hyperparameters. The available hyperparameters for FactorizationMachines
        are documented below.

        For further information on the AWS FactorizationMachines algorithm,
        please consult AWS technical documentation:
        https://docs.aws.amazon.com/sagemaker/latest/dg/fact-machines.html

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
            num_factors (int): Dimensionality of factorization.
            predictor_type (str): Type of predictor 'binary_classifier' or
                'regressor'.
            epochs (int): Number of training epochs to run.
            clip_gradient (float): Optimizer parameter. Clip the gradient by
                projecting onto the box [-clip_gradient, +clip_gradient]
            eps (float): Optimizer parameter. Small value to avoid division by
                0.
            rescale_grad (float): Optimizer parameter. If set, multiplies the
                gradient with rescale_grad before updating. Often choose to be
                1.0/batch_size.
            bias_lr (float): Non-negative learning rate for the bias term.
            linear_lr (float): Non-negative learning rate for linear terms.
            factors_lr (float): Noon-negative learning rate for factorization
                terms.
            bias_wd (float): Non-negative weight decay for the bias term.
            linear_wd (float): Non-negative weight decay for linear terms.
            factors_wd (float): Non-negative weight decay for factorization
                terms.
            bias_init_method (str): Initialization method for the bias term:
                'normal', 'uniform' or 'constant'.
            bias_init_scale (float): Non-negative range for initialization of
                the bias term that takes effect when bias_init_method parameter
                is 'uniform'
            bias_init_sigma (float): Non-negative standard deviation for
                initialization of the bias term that takes effect when
                bias_init_method parameter is 'normal'.
            bias_init_value (float): Initial value of the bias term that takes
                effect when bias_init_method parameter is 'constant'.
            linear_init_method (str): Initialization method for linear term:
                'normal', 'uniform' or 'constant'.
            linear_init_scale (float): Non-negative range for initialization of
                linear terms that takes effect when linear_init_method parameter
                is 'uniform'.
            linear_init_sigma (float): Non-negative standard deviation for
                initialization of linear terms that takes effect when
                linear_init_method parameter is 'normal'.
            linear_init_value (float): Initial value of linear terms that takes
                effect when linear_init_method parameter is 'constant'.
            factors_init_method (str): Initialization method for
                factorization term: 'normal', 'uniform' or 'constant'.
            factors_init_scale (float): Non-negative range for initialization of
                factorization terms that takes effect when factors_init_method
                parameter is 'uniform'.
            factors_init_sigma (float): Non-negative standard deviation for
                initialization of factorization terms that takes effect when
                factors_init_method parameter is 'normal'.
            factors_init_value (float): Initial value of factorization terms
                that takes effect when factors_init_method parameter is
                'constant'.
            **kwargs: base class keyword argument values.

        .. tip::

            You can find additional parameters for initializing this class at
            :class:`~sagemaker.estimator.amazon_estimator.AmazonAlgorithmEstimatorBase` and
            :class:`~sagemaker.estimator.EstimatorBase`.
        """
        ...
    
    def create_model(self, vpc_config_override=..., **kwargs):
        """Return a :class:`~sagemaker.amazon.FactorizationMachinesModel`.

        It references the latest s3 model data produced by this Estimator.

        Args:
            vpc_config_override (dict[str, list[str]]): Optional override for VpcConfig set on
                the model. Default: use subnets and security groups from this Estimator.
                * 'Subnets' (list[str]): List of subnet ids.
                * 'SecurityGroupIds' (list[str]): List of security group ids.
            **kwargs: Additional kwargs passed to the FactorizationMachinesModel constructor.
        """
        ...
    


class FactorizationMachinesPredictor(Predictor):
    """Performs binary-classification or regression prediction from input vectors.

    The implementation of
    :meth:`~sagemaker.predictor.Predictor.predict` in this
    `Predictor` requires a numpy ``ndarray`` as input. The array should
    contain the same number of columns as the feature-dimension of the data used
    to fit the model this Predictor performs inference on.

    :meth:`predict()` returns a list of
    :class:`~sagemaker.amazon.record_pb2.Record` objects (assuming the default
    recordio-protobuf ``deserializer`` is used), one for each row in
    the input ``ndarray``. The prediction is stored in the ``"score"`` key of
    the ``Record.label`` field. Please refer to the formats details described:
    https://docs.aws.amazon.com/sagemaker/latest/dg/fm-in-formats.html
    """
    def __init__(self, endpoint_name, sagemaker_session=..., serializer=..., deserializer=...) -> None:
        """Initialization for FactorizationMachinesPredictor class.

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
    


class FactorizationMachinesModel(Model):
    """Reference S3 model data created by FactorizationMachines estimator.

    Calling :meth:`~sagemaker.model.Model.deploy` creates an Endpoint and
    returns :class:`FactorizationMachinesPredictor`.
    """
    def __init__(self, model_data: Union[str, PipelineVariable], role: Optional[str] = ..., sagemaker_session: Optional[Session] = ..., **kwargs) -> None:
        """Initialization for FactorizationMachinesModel class.

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
    


