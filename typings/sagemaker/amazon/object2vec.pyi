"""
This type stub file was generated by pyright.
"""

from typing import Optional, Union
from sagemaker.amazon.amazon_estimator import AmazonAlgorithmEstimatorBase
from sagemaker.amazon.hyperparameter import Hyperparameter as hp
from sagemaker.model import Model
from sagemaker.session import Session
from sagemaker.workflow.entities import PipelineVariable

"""
This type stub file was generated by pyright.
"""
class Object2Vec(AmazonAlgorithmEstimatorBase):
    """A general-purpose neural embedding algorithm that is highly customizable.

    It can learn low-dimensional dense embeddings of high-dimensional objects. The embeddings
    are learned in a way that preserves the semantics of the relationship between pairs of
    objects in the original space in the embedding space.
    """
    repo_name: str = ...
    repo_version: str = ...
    MINI_BATCH_SIZE: int = ...
    enc_dim: hp = ...
    mini_batch_size: hp = ...
    epochs: hp = ...
    early_stopping_patience: hp = ...
    early_stopping_tolerance: hp = ...
    dropout: hp = ...
    weight_decay: hp = ...
    bucket_width: hp = ...
    num_classes: hp = ...
    mlp_layers: hp = ...
    mlp_dim: hp = ...
    mlp_activation: hp = ...
    output_layer: hp = ...
    optimizer: hp = ...
    learning_rate: hp = ...
    negative_sampling_rate: hp = ...
    comparator_list: hp = ...
    tied_token_embedding_weight: hp = ...
    token_embedding_storage_type: hp = ...
    enc0_network: hp = ...
    enc1_network: hp = ...
    enc0_cnn_filter_width: hp = ...
    enc1_cnn_filter_width: hp = ...
    enc0_max_seq_len: hp = ...
    enc1_max_seq_len: hp = ...
    enc0_token_embedding_dim: hp = ...
    enc1_token_embedding_dim: hp = ...
    enc0_vocab_size: hp = ...
    enc1_vocab_size: hp = ...
    enc0_layers: hp = ...
    enc1_layers: hp = ...
    enc0_freeze_pretrained_embedding: hp = ...
    enc1_freeze_pretrained_embedding: hp = ...
    def __init__(self, role: Optional[Union[str, PipelineVariable]] = ..., instance_count: Optional[Union[int, PipelineVariable]] = ..., instance_type: Optional[Union[str, PipelineVariable]] = ..., epochs: Optional[int] = ..., enc0_max_seq_len: Optional[int] = ..., enc0_vocab_size: Optional[int] = ..., enc_dim: Optional[int] = ..., mini_batch_size: Optional[int] = ..., early_stopping_patience: Optional[int] = ..., early_stopping_tolerance: Optional[float] = ..., dropout: Optional[float] = ..., weight_decay: Optional[float] = ..., bucket_width: Optional[int] = ..., num_classes: Optional[int] = ..., mlp_layers: Optional[int] = ..., mlp_dim: Optional[int] = ..., mlp_activation: Optional[str] = ..., output_layer: Optional[str] = ..., optimizer: Optional[str] = ..., learning_rate: Optional[float] = ..., negative_sampling_rate: Optional[int] = ..., comparator_list: Optional[str] = ..., tied_token_embedding_weight: Optional[bool] = ..., token_embedding_storage_type: Optional[str] = ..., enc0_network: Optional[str] = ..., enc1_network: Optional[str] = ..., enc0_cnn_filter_width: Optional[int] = ..., enc1_cnn_filter_width: Optional[int] = ..., enc1_max_seq_len: Optional[int] = ..., enc0_token_embedding_dim: Optional[int] = ..., enc1_token_embedding_dim: Optional[int] = ..., enc1_vocab_size: Optional[int] = ..., enc0_layers: Optional[int] = ..., enc1_layers: Optional[int] = ..., enc0_freeze_pretrained_embedding: Optional[bool] = ..., enc1_freeze_pretrained_embedding: Optional[bool] = ..., **kwargs) -> None:
        """Object2Vec is :class:`Estimator` used for anomaly detection.

        This Estimator may be fit via calls to
        :meth:`~sagemaker.amazon.amazon_estimator.AmazonAlgorithmEstimatorBase.fit`.
        There is an utility
        :meth:`~sagemaker.amazon.amazon_estimator.AmazonAlgorithmEstimatorBase.record_set`
        that can be used to upload data to S3 and creates
        :class:`~sagemaker.amazon.amazon_estimator.RecordSet` to be passed to
        the `fit` call.

        After this Estimator is fit, model data is stored in S3. The model
        may be deployed to an Amazon SageMaker Endpoint by invoking
        :meth:`~sagemaker.amazon.estimator.EstimatorBase.deploy`. As well as
        deploying an Endpoint, deploy returns a
        :class:`~sagemaker.amazon.Predictor` object that can be used for
        inference calls using the trained model hosted in the SageMaker
        Endpoint.

        Object2Vec Estimators can be configured by setting hyperparameters.
        The available hyperparameters for Object2Vec are documented below.

        For further information on the AWS Object2Vec algorithm, please
        consult AWS technical documentation:
        https://docs.aws.amazon.com/sagemaker/latest/dg/object2vec.html

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
            epochs (int): Total number of epochs for SGD training
            enc0_max_seq_len (int): Maximum sequence length
            enc0_vocab_size (int): Vocabulary size of tokens
            enc_dim (int): Optional. Dimension of the output of the embedding
                layer
            mini_batch_size (int): Optional. mini batch size for SGD training
            early_stopping_patience (int): Optional. The allowed number of
                consecutive epochs without improvement before early stopping is
                applied
            early_stopping_tolerance (float): Optional. The value used to
                determine whether the algorithm has made improvement between two
                consecutive epochs for early stopping
            dropout (float): Optional. Dropout probability on network layers
            weight_decay (float): Optional. Weight decay parameter during
                optimization
            bucket_width (int): Optional. The allowed difference between data
                sequence length when bucketing is enabled
            num_classes (int): Optional. Number of classes for classification
                training (ignored for regression problems)
            mlp_layers (int): Optional. Number of MLP layers in the network
            mlp_dim (int): Optional. Dimension of the output of MLP layer
            mlp_activation (str): Optional. Type of activation function for the
                MLP layer
            output_layer (str): Optional. Type of output layer
            optimizer (str): Optional. Type of optimizer for training
            learning_rate (float): Optional. Learning rate for SGD training
            negative_sampling_rate (int): Optional. Negative sampling rate
            comparator_list (str): Optional. Customization of comparator
                operator
            tied_token_embedding_weight (bool): Optional. Tying of token
                embedding layer weight
            token_embedding_storage_type (str): Optional. Type of token
                embedding storage
            enc0_network (str): Optional. Network model of encoder "enc0"
            enc1_network (str): Optional. Network model of encoder "enc1"
            enc0_cnn_filter_width (int): Optional. CNN filter width
            enc1_cnn_filter_width (int): Optional. CNN filter width
            enc1_max_seq_len (int): Optional. Maximum sequence length
            enc0_token_embedding_dim (int): Optional. Output dimension of token
                embedding layer
            enc1_token_embedding_dim (int): Optional. Output dimension of token
                embedding layer
            enc1_vocab_size (int): Optional. Vocabulary size of tokens
            enc0_layers (int): Optional. Number of layers in encoder
            enc1_layers (int): Optional. Number of layers in encoder
            enc0_freeze_pretrained_embedding (bool): Optional. Freeze pretrained
                embedding weights
            enc1_freeze_pretrained_embedding (bool): Optional. Freeze pretrained
                embedding weights
            **kwargs: base class keyword argument values.

        .. tip::

            You can find additional parameters for initializing this class at
            :class:`~sagemaker.estimator.amazon_estimator.AmazonAlgorithmEstimatorBase` and
            :class:`~sagemaker.estimator.EstimatorBase`.
        """
        ...
    
    def create_model(self, vpc_config_override=..., **kwargs):
        """Return a :class:`~sagemaker.amazon.Object2VecModel`.

        It references the latest s3 model data produced by this Estimator.

        Args:
            vpc_config_override (dict[str, list[str]]): Optional override for VpcConfig set on
                the model. Default: use subnets and security groups from this Estimator.
                * 'Subnets' (list[str]): List of subnet ids.
                * 'SecurityGroupIds' (list[str]): List of security group ids.
            **kwargs: Additional kwargs passed to the Object2VecModel constructor.
        """
        ...
    


class Object2VecModel(Model):
    """Reference Object2Vec s3 model data.

    Calling :meth:`~sagemaker.model.Model.deploy` creates an Endpoint and returns a
    Predictor that calculates anomaly scores for datapoints.
    """
    def __init__(self, model_data: Union[str, PipelineVariable], role: Optional[str] = ..., sagemaker_session: Optional[Session] = ..., **kwargs) -> None:
        """Initialization for Object2VecModel class.

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
    


