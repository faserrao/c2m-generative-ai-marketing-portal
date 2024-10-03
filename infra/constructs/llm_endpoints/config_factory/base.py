from abc import ABC, abstractmethod
from typing import Any, Dict

from infra.constructs.llm_endpoints.constants import NAME_SEPARATOR
from infra.constructs.llm_endpoints.utils import create_resource_name


class BaseEndpointConfigurationFactory(ABC):
    """Base class for all endpoint configuration factories.

    :param user_config: A dictionary of user-provided configuration.
    :param resource_prefix: A string prefix for all resources created by this factory.
    """

    def __init__(self, user_config: Dict[str, Any], resource_prefix: str) -> None:
        """Initialize the factory.

        :param user_config: A dictionary of user-provided configuration.
        :param resource_prefix: A string prefix for all resources created by this factory.
        """
        self.user_config = user_config
        self.prefix = resource_prefix

    @abstractmethod
    def create_container_definition_config(self) -> Dict[str, Any]:
        pass

    @abstractmethod
    def create_model_config(self) -> Dict[str, Any]:
        pass

    @abstractmethod
    def create_production_variant_config(self) -> Dict[str, Any]:
        pass

    @abstractmethod
    def create_endpoint_config_config(self) -> Dict[str, Any]:
        pass

    @abstractmethod
    def create_endpoint_config(self) -> Dict[str, Any]:
        pass


class BasicEndpointConfigurationFactory(BaseEndpointConfigurationFactory):
    def create_container_definition_config(self) -> Dict[str, Any]:
        """Create a SageMaker container definition configuration.

        :return: A dictionary of configuration.
        """
        config = {"mode": "SingleModel"}
        # If the user has provided environment variables, add them to the config
        if "env" in self.user_config:
            config.update({"environment": self.user_config["env"]})
        return config

    def create_model_config(self) -> Dict[str, Any]:
        """Create a SageMaker model configuration.

        :return: A dictionary of configuration.
        """

        return {
            "model_name": create_resource_name(base_name=NAME_SEPARATOR.join([self.prefix, "model"])),
        }

    def create_production_variant_config(self) -> Dict[str, Any]:
        """Create a SageMaker production variant configuration.

        The configuration will be a dictionary with the following keys:

        - "variant_name": The name of the production variant.
        - "initial_instance_count": The initial number of instances to run for the production variant.
        - "initial_variant_weight": The initial weight of the production variant.
        - "volume_size_in_gb": The size of the volume in GB that will be attached to the production variant.
        - "model_data_download_timeout_in_seconds": The timeout in seconds for downloading the model data.
        - "container_startup_health_check_timeout_in_seconds": The timeout in seconds for the container health check.
        - "instance_type": The type of instance to run the production variant on.

        The user can override the default values of these keys in their configuration file.
        """
        config = {
            "variant_name": "AllTraffic",
            "initial_instance_count": 1,
            "initial_variant_weight": 1.0,
        }
        pv_config_names = [
            "volume_size_in_gb",
            "model_data_download_timeout_in_seconds",
            "container_startup_health_check_timeout_in_seconds",
            "instance_type",
        ]
        user_config = {key: self.user_config[key] for key in pv_config_names if key in self.user_config}
        config.update(user_config)
        return config

    def create_endpoint_config_config(self) -> Dict[str, Any]:
        """Create a SageMaker endpoint configuration configuration.

        The configuration will be a dictionary with the following key:

        - "endpoint_config_name": The name of the endpoint configuration.

        The user can override the default value of this key in their configuration file.
        """
        return {
            "endpoint_config_name": create_resource_name(
                base_name=NAME_SEPARATOR.join([self.prefix, "endpoint", "config"])
            ),
        }

    def create_endpoint_config(self) -> Dict[str, Any]:
        """Create a SageMaker endpoint configuration.

        The configuration will be a dictionary with the following key:

        - "endpoint_name": The name of the endpoint.

        The user can override the default value of this key in their configuration file.

        :return: A dictionary of configuration.
        """
        return {
            "endpoint_name": create_resource_name(base_name=NAME_SEPARATOR.join([self.prefix, "endpoint"])),
        }


class NonProprietaryModelEndpointConfigurationFactory(BasicEndpointConfigurationFactory):
    def create_container_definition_config(self) -> Dict[str, Any]:
        """Create a SageMaker container definition configuration.

        The configuration will be a dictionary with the following keys:

        - "container_name": The name of the container.
        - "image": The URI of the container image.
        - "model_data_url": The URL of the model data.

        The user can override the default value of these keys in their configuration file.

        :return: A dictionary of configuration.
        """
        config = super().create_container_definition_config()
        if "model_data_url" in self.user_config:
            config.update({"model_data_url": self.user_config["model_data_url"]})
        if "image_uri" in self.user_config:
            config.update({"image": self.user_config["image_uri"]})
        return config
