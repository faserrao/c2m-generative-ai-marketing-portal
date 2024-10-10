"""
This type stub file was generated by pyright.
"""

from datetime import datetime
from typing import Iterator, List, Optional
from sagemaker.apiutils import _base_types
from sagemaker.lineage import association
from sagemaker.lineage._api_types import ContextSummary
from sagemaker.lineage.query import LineageQueryDirectionEnum
from sagemaker.lineage.artifact import Artifact
from sagemaker.lineage.action import Action
from sagemaker.lineage.lineage_trial_component import LineageTrialComponent

"""This module contains code to create and manage SageMaker ``Context``."""
class Context(_base_types.Record):
    """An Amazon SageMaker context, which is part of a SageMaker lineage.

    Attributes:
        context_arn (str): The ARN of the context.
        context_name (str): The name of the context.
        context_type (str): The type of the context.
        description (str): A description of the context.
        source (obj): The source of the context with a URI and type.
        properties (dict): Dictionary of properties.
        tags (List[dict[str, str]]): A list of tags to associate with the context.
        creation_time (datetime): When the context was created.
        created_by (obj): Contextual info on which account created the context.
        last_modified_time (datetime): When the context was last modified.
        last_modified_by (obj): Contextual info on which account created the context.
    """
    context_arn: str = ...
    context_name: str = ...
    context_type: str = ...
    properties: dict = ...
    tags: list = ...
    creation_time: datetime = ...
    created_by: str = ...
    last_modified_time: datetime = ...
    last_modified_by: str = ...
    _boto_load_method: str = ...
    _boto_create_method: str = ...
    _boto_update_method: str = ...
    _boto_delete_method: str = ...
    _custom_boto_types = ...
    _boto_update_members = ...
    _boto_delete_members = ...
    def save(self) -> Context:
        """Save the state of this Context to SageMaker.

        Returns:
            obj: boto API response.
        """
        ...
    
    def delete(self, disassociate: bool = ...): # -> Any:
        """Delete the context object.

        Args:
            disassociate (bool): When set to true, disassociate incoming and outgoing association.

        Returns:
            obj: boto API response.
        """
        ...
    
    def set_tag(self, tag=...):
        """Add a tag to the object.

        Args:
            tag (obj): Key value pair to set tag.

        Returns:
            list({str:str}): a list of key value pairs
        """
        ...
    
    def set_tags(self, tags=...):
        """Add tags to the object.

        Args:
            tags ([{key:value}]): list of key value pairs.

        Returns:
            list({str:str}): a list of key value pairs
        """
        ...
    
    @classmethod
    def load(cls, context_name: str, sagemaker_session=...) -> Context:
        """Load an existing context and return an ``Context`` object representing it.

        Examples:
            .. code-block:: python

                from sagemaker.lineage import context

                my_context = context.Context.create(
                    context_name='MyContext',
                    context_type='Endpoint',
                    source_uri='arn:aws:...')

                my_context.properties["added"] = "property"
                my_context.save()

                for ctx in context.Context.list():
                    print(ctx)

                my_context.delete()

            Args:
                context_name (str): Name of the context
                sagemaker_session (sagemaker.session.Session): Session object which
                    manages interactions with Amazon SageMaker APIs and any other
                    AWS services needed. If not specified, one is created using the
                    default AWS configuration chain.

            Returns:
                Context: A SageMaker ``Context`` object
        """
        ...
    
    @classmethod
    def create(cls, context_name: str = ..., source_uri: str = ..., source_type: str = ..., context_type: str = ..., description: str = ..., properties: dict = ..., tags: dict = ..., sagemaker_session=...) -> Context:
        """Create a context and return a ``Context`` object representing it.

        Args:
            context_name (str): The name of the context.
            source_uri (str): The source URI of the context.
            source_type (str): The type of the source.
            context_type (str): The type of the context.
            description (str): Description of the context.
            properties (dict): Metadata associated with the context.
            tags (dict): Tags to add to the context.
            sagemaker_session (sagemaker.session.Session): Session object which
                manages interactions with Amazon SageMaker APIs and any other
                AWS services needed. If not specified, one is created using the
                default AWS configuration chain.

        Returns:
            Context: A SageMaker ``Context`` object.
        """
        ...
    
    @classmethod
    def list(cls, source_uri: Optional[str] = ..., context_type: Optional[str] = ..., created_after: Optional[datetime] = ..., created_before: Optional[datetime] = ..., sort_by: Optional[str] = ..., sort_order: Optional[str] = ..., max_results: Optional[int] = ..., next_token: Optional[str] = ..., sagemaker_session=...) -> Iterator[ContextSummary]:
        """Return a list of context summaries.

        Args:
            source_uri (str, optional): A source URI.
            context_type (str, optional): An context type.
            created_before (datetime.datetime, optional): Return contexts created before this
                instant.
            created_after (datetime.datetime, optional): Return contexts created after this instant.
            sort_by (str, optional): Which property to sort results by.
                One of 'SourceArn', 'CreatedBefore', 'CreatedAfter'
            sort_order (str, optional): One of 'Ascending', or 'Descending'.
            max_results (int, optional): maximum number of contexts to retrieve
            next_token (str, optional): token for next page of results
            sagemaker_session (sagemaker.session.Session): Session object which
                manages interactions with Amazon SageMaker APIs and any other
                AWS services needed. If not specified, one is created using the
                default AWS configuration chain.

        Returns:
            collections.Iterator[ContextSummary]: An iterator
                over ``ContextSummary`` objects.
        """
        ...
    
    def actions(self, direction: LineageQueryDirectionEnum) -> List[Action]:
        """Use the lineage query to retrieve actions that use this context.

        Args:
            direction (LineageQueryDirectionEnum): The query direction.

        Returns:
            list of Actions: Actions.
        """
        ...
    


class EndpointContext(Context):
    """An Amazon SageMaker endpoint context, which is part of a SageMaker lineage."""
    def models(self) -> List[association.Association]:
        """Use Lineage API to get all models deployed by this endpoint.

        Returns:
            list of Associations: Associations that destination represents an endpoint's model.
        """
        ...
    
    def models_v2(self, direction: LineageQueryDirectionEnum = ...) -> List[Artifact]:
        """Use the lineage query to retrieve downstream model artifacts that use this endpoint.

        Args:
            direction (LineageQueryDirectionEnum, optional): The query direction.

        Returns:
            list of Artifacts: Artifacts representing a model.
        """
        ...
    
    def dataset_artifacts(self, direction: LineageQueryDirectionEnum = ...) -> List[Artifact]:
        """Use the lineage query to retrieve datasets that use this endpoint.

        Args:
            direction (LineageQueryDirectionEnum, optional): The query direction.

        Returns:
            list of Artifacts: Artifacts representing a dataset.
        """
        ...
    
    def training_job_arns(self, direction: LineageQueryDirectionEnum = ...) -> List[str]:
        """Get ARNs for all training jobs that appear in the endpoint's lineage.

        Args:
            direction (LineageQueryDirectionEnum, optional): The query direction.

        Returns:
            list of str: Training job ARNs.
        """
        ...
    
    def processing_jobs(self, direction: LineageQueryDirectionEnum = ...) -> List[LineageTrialComponent]:
        """Use the lineage query to retrieve processing jobs that use this endpoint.

        Args:
            direction (LineageQueryDirectionEnum, optional): The query direction.

        Returns:
            list of LineageTrialComponent: Lineage trial component that represent Processing jobs.
        """
        ...
    
    def transform_jobs(self, direction: LineageQueryDirectionEnum = ...) -> List[LineageTrialComponent]:
        """Use the lineage query to retrieve transform jobs that use this endpoint.

        Args:
            direction (LineageQueryDirectionEnum, optional): The query direction.

        Returns:
            list of LineageTrialComponent: Lineage trial component that represent Transform jobs.
        """
        ...
    
    def trial_components(self, direction: LineageQueryDirectionEnum = ...) -> List[LineageTrialComponent]:
        """Use the lineage query to retrieve trial components that use this endpoint.

        Args:
            direction (LineageQueryDirectionEnum, optional): The query direction.

        Returns:
            list of LineageTrialComponent: Lineage trial component.
        """
        ...
    
    def pipeline_execution_arn(self, direction: LineageQueryDirectionEnum = ...) -> str:
        """Get the ARN for the pipeline execution associated with this endpoint (if any).

        Args:
            direction (LineageQueryDirectionEnum, optional): The query direction.

        Returns:
            str: A pipeline execution ARN.
        """
        ...
    


class ModelPackageGroup(Context):
    """An Amazon SageMaker model package group context, which is part of a SageMaker lineage."""
    def pipeline_execution_arn(self) -> str:
        """Get the ARN for the pipeline execution associated with this model package group (if any).

        Returns:
            str: A pipeline execution ARN.
        """
        ...
    


