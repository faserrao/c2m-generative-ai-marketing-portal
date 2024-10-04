"""Model Spec Jumpstarter."""
from typing import Any, Dict

from sagemaker import environment_variables, image_uris, instance_types, model_uris
from sagemaker.jumpstart.utils import verify_model_region_and_return_specs
from sagemaker.utils import volume_size_supported

from infra.constructs.llm_endpoints.config_factory.base import NonProprietaryModelEndpointConfigurationFactory
from infra.constructs.llm_endpoints.constants import NAME_SEPARATOR


class JumpStartModelSpecParser:
    SCOPE = "inference"

    def __init__(self, model_id: str, model_version: str, region_name: str) -> None:
        """
        Args:
            model_id (str): JumpStart model ID.
            model_version (str): JumpStart model version.
            region_name (str): AWS region name.

        Attributes:
            model_id (str): JumpStart model ID.
            model_version (str): JumpStart model version.
            region_name (str): AWS region name.
            model_spec (Dict[str, Any]): JumpStart model spec.
        """
        self.model_id = model_id
        self.model_version = model_version
        self.tolerate_deprecated_model = False
        self.tolerate_vulnerable_model = False
        self.region_name = region_name
        self.model_spec = verify_model_region_and_return_specs(
            model_id=self.model_id,
            version=self.model_version,
            region=self.region_name,
            scope=self.SCOPE,
            tolerate_deprecated_model=self.tolerate_deprecated_model,
            tolerate_vulnerable_model=self.tolerate_vulnerable_model,
        )

    def get_model_data_url(self) -> str:
        """Get the model data URL.

        Returns:
            str: Model data URL.
        """
        return model_uris.retrieve(
            model_scope=self.SCOPE,
            model_id=self.model_id,
            model_version=self.model_version,
            region=self.region_name,
            tolerate_deprecated_model=self.tolerate_deprecated_model,
            tolerate_vulnerable_model=self.tolerate_vulnerable_model,
        )

    def get_instance_type(self) -> str:
        """Get the instance type.

        Returns:
            str: Instance type.
        """
        return instance_types.retrieve_default(
            scope=self.SCOPE,
            model_id=self.model_id,
            model_version=self.model_version,
            region=self.region_name,
            tolerate_deprecated_model=self.tolerate_deprecated_model,
            tolerate_vulnerable_model=self.tolerate_vulnerable_model,
        )

    def get_image_uri(self) -> str:
        """Get the image URI.

        Returns:
            str: Image URI.
        """
        return image_uris.retrieve(
            image_scope=self.SCOPE,
            model_id=self.model_id,
            model_version=self.model_version,
            region=self.region_name,
            framework=None,
            instance_type=self.get_instance_type(),
            tolerate_deprecated_model=self.tolerate_deprecated_model,
            tolerate_vulnerable_model=self.tolerate_vulnerable_model,
        )

    def get_container_environment(self) -> Dict[str, str]:
        """Get the container environment variables.

        Returns:
            Dict[str, str]: Container environment variables.
        """
        return environment_variables.retrieve_default(
            model_id=self.model_id,
            model_version=self.model_version,
            region=self.region_name,
            include_aws_sdk_env_vars=False,
            tolerate_deprecated_model=self.tolerate_deprecated_model,
            tolerate_vulnerable_model=self.tolerate_vulnerable_model,
        )

    def get_deployment_kwargs(self) -> Dict[str, Any]:
        """Get the deployment kwargs.

        Returns:
            Dict[str, Any]: Deployment kwargs.
        """

        deploy_kwargs = self.model_spec.deploy_kwargs
        deploy_kwargs = {
            "model_data_download_timeout_in_seconds": self.model_spec.deploy_kwargs.get(
                "model_data_download_timeout", None
            ),
            "container_startup_health_check_timeout_in_seconds": self.model_spec.deploy_kwargs.get(
                "container_startup_health_check_timeout", None
            ),
        }

        instance_type = self.get_instance_type()
        if volume_size_supported(instance_type) and self.model_spec.inference_volume_size is not None:
            deploy_kwargs.update({"volume_size_in_gb": self.model_spec.inference_volume_size})

        return deploy_kwargs


class JumpStartEndpointConfigurationFactory(NonProprietaryModelEndpointConfigurationFactory):
    def __init__(
        self, model_id: str, model_version: str, region_name: str, user_config: Dict[str, Any], resource_prefix: str
    ) -> None:
        """Initialize the factory.

        :param model_id: JumpStart model ID.
        :param model_version: JumpStart model version.
        :param region_name: AWS region name.
        :param user_config: A dictionary of user-provided configuration.
        :param resource_prefix: A string prefix for all resources created by this factory.
        """
        self.model_spec_parser = JumpStartModelSpecParser(
            model_id=model_id, model_version=model_version, region_name=region_name
        )
        resource_prefix = NAME_SEPARATOR.join([resource_prefix, "jumpstart"])
        super().__init__(user_config=user_config, resource_prefix=resource_prefix)

    def create_container_definition_config(self) -> Dict[str, Any]:
        """Create a SageMaker container definition configuration.

        The configuration will be a dictionary with the following keys:

        - "model_data_url": The URL of the model data.
        - "image": The URI of the container image.
        - "environment": A dictionary of environment variables.

        The user can override the default value of these keys in their configuration file.

        :return: A dictionary of configuration.
        """
        base_config = super().create_container_definition_config()
        environment = self.model_spec_parser.get_container_environment()
        environment.update(base_config.pop("environment", {}))
        config = {
            "model_data_url": self.model_spec_parser.get_model_data_url(),
            "image": self.model_spec_parser.get_image_uri(),
            "environment": environment,
        }
        config.update(base_config)
        return config

    def create_model_config(self) -> Dict[str, Any]:
        """Create a SageMaker model configuration.

        The configuration will be a dictionary with the following key:

        - "enable_network_isolation": Whether the model should be run in network isolation mode.

        The user can override the default value of this key in their configuration file.

        :return: A dictionary of configuration.
        """
        base_config = super().create_model_config()
        config = {
            "enable_network_isolation": self.model_spec_parser.model_spec.inference_enable_network_isolation,
        }
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
        config = {
            "instance_type": self.model_spec_parser.get_instance_type(),
            **self.model_spec_parser.get_deployment_kwargs(),
        }
        config.update(base_config)
        return config
