"""Hugging Face TGI configuration factory."""
from typing import Any, Dict

import sagemaker.session
from sagemaker.huggingface import get_huggingface_llm_image_uri

from infra.constructs.llm_endpoints.config_factory.base import NonProprietaryModelEndpointConfigurationFactory
from infra.constructs.llm_endpoints.constants import NAME_SEPARATOR

DEFAULT_TGI_SERVER_VERSION = "0.8.2"
# To get the list of the server versions for which a DLC is available, see:
# https://github.com/aws/deep-learning-containers/blob/master/available_images.md#huggingface-text-generation-inference-containers


class HuggingFaceTGIEndpointConfigurationFactory(NonProprietaryModelEndpointConfigurationFactory):
    def __init__(self, model_id: str, region_name: str, user_config: Dict[str, Any], resource_prefix: str) -> None:
        self.model_id = model_id  # HuggingFace Hub model ID, e.g. "tiiuae/falcon-7b"
        self.region_name = region_name
        resource_prefix = NAME_SEPARATOR.join([resource_prefix, "tgi"])
        super().__init__(user_config=user_config, resource_prefix=resource_prefix)

    def create_container_definition_config(self) -> Dict[str, Any]:
        """Create a SageMaker container definition configuration.

        The configuration will be a dictionary with the following keys:

        - "environment": A dictionary with a single key-value pair: "HF_MODEL_ID" with the model ID.
        - "image": The URI of the container image.

        The user can override the default value of these keys in their configuration file.
        """
        base_config = super().create_container_definition_config()
        environment = {"HF_MODEL_ID": self.model_id}
        environment.update(base_config.pop("environment", {}))
        config = {"environment": environment}
        if "image" not in base_config:
            session = sagemaker.session.Session()
            image_uri = get_huggingface_llm_image_uri(
                backend="huggingface",
                version=self.user_config.get("model_server_version", DEFAULT_TGI_SERVER_VERSION),
                region=self.region_name,
                session=session,
            )
            config.update({"image": image_uri})
        config.update(base_config)
        return config

    def create_production_variant_config(self) -> Dict[str, Any]:
        """Create a SageMaker production variant configuration.

        The configuration will be a dictionary with the following keys:

        - "instance_type": The type of instance to run the production variant on.
        - The other keys are the same as the keyword arguments for the ``deploy`` method of the
          :class:`sagemaker.model.Model` class.

        The user can override the default value of these keys in their configuration file.

        :return: A dictionary of configuration.
        """
        base_config = super().create_production_variant_config()
        if "instance_type" not in base_config:
            raise ValueError("Missing mandatory configuration: instance type")
        return base_config
