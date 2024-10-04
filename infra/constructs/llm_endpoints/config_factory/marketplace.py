"""The `BaseEndpointConfigurationFactory` is an abstract base class that
defines the structure of a factory for creating configurations for SageMaker
endpoints. It is an abstract base class, meaning it cannot be instantiated
directly.

Here is a succinct explanation of what each method does:

- `__init__`: Initializes the factory with the user-provided configuration and a resource prefix.

- `create_container_definition_config`: Creates a configuration for a SageMaker container definition.

- `create_model_config`: Creates a configuration for a SageMaker model.

- `create_production_variant_config`: Creates a configuration for a SageMaker production variant.

- `create_endpoint_config_config`: Creates a configuration for a SageMaker endpoint configuration.

- `create_endpoint_config`: Creates a configuration for a SageMaker endpoint.

All of these methods are abstract, meaning they must be implemented in any class that inherits from `BaseEndpointConfigurationFactory`.
"""
from typing import Any, Dict

from infra.constructs.llm_endpoints.config_factory.base import BasicEndpointConfigurationFactory
from infra.constructs.llm_endpoints.constants import NAME_SEPARATOR


class MarketplaceModelEndpointConfigurationFactory(BasicEndpointConfigurationFactory):
    def __init__(self, model_package_arn: str, user_config: Dict[str, Any], resource_prefix: str) -> None:
        """Initialize the factory.

        :param model_package_arn: The ARN of the marketplace model package.
        :param user_config: A dictionary of user-provided configuration.
        :param resource_prefix: A string prefix for all resources created by this factory.
        """
        self.model_package_arn = model_package_arn
        resource_prefix = NAME_SEPARATOR.join([resource_prefix, "marketplace"])
        super().__init__(user_config=user_config, resource_prefix=resource_prefix)

    def create_container_definition_config(self) -> Dict[str, Any]:
        """Create a SageMaker container definition configuration.

        The configuration will be a dictionary with the following key:

        - "model_package_name": The ARN of the marketplace model package.

        The user can override the default value of this key in their configuration file.

        :return: A dictionary of configuration.
        """
        allowed_config_names = ["environment"]
        base_config = super().create_container_definition_config()
        base_config = {k: v for k, v in base_config.items() if k in allowed_config_names}
        config = {"model_package_name": self.model_package_arn}
        config.update(base_config)
        return config

    def create_model_config(self) -> Dict[str, Any]:
        """Create a SageMaker model configuration.

        The configuration will be a dictionary with the following key:

        - "enable_network_isolation": Whether to enable network isolation for the model.

        The user can override the default value of this key in their configuration file.

        :return: A dictionary of configuration.
        """
        base_config = super().create_model_config()
        config = {
            "enable_network_isolation": True,
        }
        config.update(base_config)
        return config
