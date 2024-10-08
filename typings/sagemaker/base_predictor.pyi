"""
This type stub file was generated by pyright.
"""

import abc
from typing import Any, Tuple

"""
This type stub file was generated by pyright.
"""
class PredictorBase(abc.ABC):
    """An object that encapsulates a deployed model."""
    @abc.abstractmethod
    def predict(self, *args, **kwargs) -> Any:
        """Perform inference on the provided data and return a prediction."""
        ...
    
    @abc.abstractmethod
    def delete_predictor(self, *args, **kwargs) -> None:
        """Destroy resources associated with this predictor."""
        ...
    
    @property
    @abc.abstractmethod
    def content_type(self) -> str:
        """The MIME type of the data sent to the inference server."""
        ...
    
    @property
    @abc.abstractmethod
    def accept(self) -> Tuple[str]:
        """The content type(s) that are expected from the inference server."""
        ...
    
    def __str__(self) -> str:
        """Overriding str(*) method to make more human-readable."""
        ...
    


class Predictor(PredictorBase):
    """Make prediction requests to an Amazon SageMaker endpoint."""
    def __init__(self, endpoint_name, sagemaker_session=..., serializer=..., deserializer=..., **kwargs) -> None:
        """Initialize a ``Predictor``.

        Behavior for serialization of input data and deserialization of
        result data can be configured through initializer arguments. If not
        specified, a sequence of bytes is expected and the API sends it in the
        request body without modifications. In response, the API returns the
        sequence of bytes from the prediction result without any modifications.

        Args:
            endpoint_name (str): Name of the Amazon SageMaker endpoint to which
                requests are sent.
            sagemaker_session (sagemaker.session.Session): A SageMaker Session
                object, used for SageMaker interactions (default: None). If not
                specified, one is created using the default AWS configuration
                chain.
            serializer (:class:`~sagemaker.serializers.BaseSerializer`): A
                serializer object, used to encode data for an inference endpoint
                (default: :class:`~sagemaker.serializers.IdentitySerializer`).
            deserializer (:class:`~sagemaker.deserializers.BaseDeserializer`): A
                deserializer object, used to decode data from an inference
                endpoint (default: :class:`~sagemaker.deserializers.BytesDeserializer`).
        """
        ...
    
    def predict(self, data, initial_args=..., target_model=..., target_variant=..., inference_id=..., custom_attributes=...):
        """Return the inference from the specified endpoint.

        Args:
            data (object): Input data for which you want the model to provide
                inference. If a serializer was specified when creating the
                Predictor, the result of the serializer is sent as input
                data. Otherwise the data must be sequence of bytes, and the
                predict method then sends the bytes in the request body as is.
            initial_args (dict[str,str]): Optional. Default arguments for boto3
                ``invoke_endpoint`` call. Default is None (no default
                arguments).
            target_model (str): S3 model artifact path to run an inference request on,
                in case of a multi model endpoint. Does not apply to endpoints hosting
                single model (Default: None)
            target_variant (str): The name of the production variant to run an inference
                request on (Default: None). Note that the ProductionVariant identifies the
                model you want to host and the resources you want to deploy for hosting it.
            inference_id (str): If you provide a value, it is added to the captured data
                when you enable data capture on the endpoint (Default: None).
            custom_attributes (str): Provides additional information about a request for an
                inference submitted to a model hosted at an Amazon SageMaker endpoint.
                The information is an opaque value that is forwarded verbatim. You could use this
                value, for example, to provide an ID that you can use to track a request or to
                provide other metadata that a service endpoint was programmed to process. The value
                must consist of no more than 1024 visible US-ASCII characters.

                The code in your model is responsible for setting or updating any custom attributes
                in the response. If your code does not set this value in the response, an empty
                value is returned. For example, if a custom attribute represents the trace ID, your
                model can prepend the custom attribute with Trace ID: in your post-processing
                function (Default: None).

        Returns:
            object: Inference for the given input. If a deserializer was specified when creating
                the Predictor, the result of the deserializer is
                returned. Otherwise the response returns the sequence of bytes
                as is.
        """
        ...
    
    def update_endpoint(self, initial_instance_count=..., instance_type=..., accelerator_type=..., model_name=..., tags=..., kms_key=..., data_capture_config_dict=..., wait=...):
        """Update the existing endpoint with the provided attributes.

        This creates a new EndpointConfig in the process. If ``initial_instance_count``,
        ``instance_type``, ``accelerator_type``, or ``model_name`` is specified, then a new
        ProductionVariant configuration is created; values from the existing configuration
        are not preserved if any of those parameters are specified.

        Args:
            initial_instance_count (int): The initial number of instances to run in the endpoint.
                This is required if ``instance_type``, ``accelerator_type``, or ``model_name`` is
                specified. Otherwise, the values from the existing endpoint configuration's
                ProductionVariants are used.
            instance_type (str): The EC2 instance type to deploy the endpoint to.
                This is required if ``initial_instance_count`` or ``accelerator_type`` is specified.
                Otherwise, the values from the existing endpoint configuration's
                ``ProductionVariants`` are used.
            accelerator_type (str): The type of Elastic Inference accelerator to attach to
                the endpoint, e.g. "ml.eia1.medium". If not specified, and
                ``initial_instance_count``, ``instance_type``, and ``model_name`` are also ``None``,
                the values from the existing endpoint configuration's ``ProductionVariants`` are
                used. Otherwise, no Elastic Inference accelerator is attached to the endpoint.
            model_name (str): The name of the model to be associated with the endpoint.
                This is required if ``initial_instance_count``, ``instance_type``, or
                ``accelerator_type`` is specified and if there is more than one model associated
                with the endpoint. Otherwise, the existing model for the endpoint is used.
            tags (list[dict[str, str]]): The list of tags to add to the endpoint
                config. If not specified, the tags of the existing endpoint configuration are used.
                If any of the existing tags are reserved AWS ones (i.e. begin with "aws"),
                they are not carried over to the new endpoint configuration.
            kms_key (str): The KMS key that is used to encrypt the data on the storage volume
                attached to the instance hosting the endpoint If not specified,
                the KMS key of the existing endpoint configuration is used.
            data_capture_config_dict (dict): The endpoint data capture configuration
                for use with Amazon SageMaker Model Monitoring. If not specified,
                the data capture configuration of the existing endpoint configuration is used.

        Raises:
            ValueError: If there is not enough information to create a new ``ProductionVariant``:

                - If ``initial_instance_count``, ``accelerator_type``, or ``model_name`` is
                  specified, but ``instance_type`` is ``None``.
                - If ``initial_instance_count``, ``instance_type``, or ``accelerator_type`` is
                  specified and either ``model_name`` is ``None`` or there are multiple models
                  associated with the endpoint.
        """
        ...
    
    def delete_endpoint(self, delete_endpoint_config=...):
        """Delete the Amazon SageMaker endpoint backing this predictor.

        This also delete the endpoint configuration attached to it if
        delete_endpoint_config is True.

        Args:
            delete_endpoint_config (bool, optional): Flag to indicate whether to
                delete endpoint configuration together with endpoint. Defaults
                to True. If True, both endpoint and endpoint configuration will
                be deleted. If False, only endpoint will be deleted.
        """
        ...
    
    delete_predictor = ...
    def delete_model(self):
        """Deletes the Amazon SageMaker models backing this predictor."""
        ...
    
    def enable_data_capture(self):
        """Enables data capture by updating DataCaptureConfig.

        This function updates the DataCaptureConfig for the Predictor's associated Amazon SageMaker
        Endpoint to enable data capture. For a more customized experience, refer to
        update_data_capture_config, instead.
        """
        ...
    
    def disable_data_capture(self):
        """Disables data capture by updating DataCaptureConfig.

        This function updates the DataCaptureConfig for the Predictor's associated Amazon SageMaker
        Endpoint to disable data capture. For a more customized experience, refer to
        update_data_capture_config, instead.
        """
        ...
    
    def update_data_capture_config(self, data_capture_config):
        """Updates the DataCaptureConfig for the Predictor's associated Amazon SageMaker Endpoint.

        Update is done using the provided DataCaptureConfig.

        Args:
            data_capture_config (sagemaker.model_monitor.DataCaptureConfig): The
                DataCaptureConfig to update the predictor's endpoint to use.
        """
        ...
    
    def list_monitors(self):
        """Generates ModelMonitor objects (or DefaultModelMonitors).

        Objects are generated based on the schedule(s) associated with the endpoint
        that this predictor refers to.

        Returns:
            [sagemaker.model_monitor.model_monitoring.ModelMonitor]: A list of
                ModelMonitor (or DefaultModelMonitor) objects.

        """
        ...
    
    def endpoint_context(self):
        """Retrieves the lineage context object representing the endpoint.

        Examples:
            .. code-block:: python

            predictor = Predictor()
            ...
            context = predictor.endpoint_context()
            models = context.models()

        Returns:
            ContextEndpoint: The context for the endpoint.
        """
        ...
    
    @property
    def content_type(self):
        """The MIME type of the data sent to the inference endpoint."""
        ...
    
    @property
    def accept(self):
        """The content type(s) that are expected from the inference endpoint."""
        ...
    
    @content_type.setter
    def content_type(self, val: str):
        """Set the MIME type of the data sent to the inference endpoint."""
        ...
    
    @accept.setter
    def accept(self, val: str):
        """Set the content type(s) that are expected from the inference endpoint."""
        ...
    
    @property
    def endpoint(self):
        """Deprecated attribute. Please use endpoint_name."""
        ...
    


csv_serializer = ...
json_serializer = ...
npy_serializer = ...
csv_deserializer = ...
json_deserializer = ...
numpy_deserializer = ...
RealTimePredictor = ...
