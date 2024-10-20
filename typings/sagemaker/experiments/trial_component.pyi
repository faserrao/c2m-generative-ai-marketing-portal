"""
This type stub file was generated by pyright.
"""

from sagemaker.apiutils import _base_types

"""Contains the TrialComponent class."""
class _TrialComponent(_base_types.Record):
    """This class represents a SageMaker trial component object.

    A trial component is a stage in a trial.
    Trial components are created automatically within the SageMaker runtime and
    may not be created directly. To automatically associate trial components with
    a trial and experiment, supply an experiment config when creating a job.
    For example: https://docs.aws.amazon.com/sagemaker/latest/dg/API_CreateTrainingJob.html

    Attributes:
        trial_component_name (str): The name of the trial component. Generated by SageMaker
            from the name of the source job with a suffix specific to the type of source job.
        trial_component_arn (str): The ARN of the trial component.
        display_name (str): The name of the trial component that will appear in UI,
            such as SageMaker Studio.
        source (TrialComponentSource): A TrialComponentSource object with a source_arn attribute.
        status (str): Status of the source job.
        start_time (datetime): When the source job started.
        end_time (datetime): When the source job ended.
        creation_time (datetime): When the source job was created.
        created_by (obj): Contextual info on which account created the trial component.
        last_modified_time (datetime): When the trial component was last modified.
        last_modified_by (obj): Contextual info on which account last modified the trial component.
        parameters (dict): Dictionary of parameters to the source job.
        input_artifacts (dict): Dictionary of input artifacts.
        output_artifacts (dict): Dictionary of output artifacts.
        metrics (obj): Aggregated metrics for the job.
        parameters_to_remove (list): The hyperparameters to remove from the component.
        input_artifacts_to_remove (list): The input artifacts to remove from the component.
        output_artifacts_to_remove (list): The output artifacts to remove from the component.
        tags (List[Dict[str, str]]): A list of tags to associate with the trial component.
    """
    trial_component_name = ...
    trial_component_arn = ...
    display_name = ...
    source = ...
    status = ...
    start_time = ...
    end_time = ...
    creation_time = ...
    created_by = ...
    last_modified_time = ...
    last_modified_by = ...
    parameters = ...
    input_artifacts = ...
    output_artifacts = ...
    metrics = ...
    parameters_to_remove = ...
    input_artifacts_to_remove = ...
    output_artifacts_to_remove = ...
    tags = ...
    _boto_load_method = ...
    _boto_create_method = ...
    _boto_update_method = ...
    _boto_delete_method = ...
    _custom_boto_types = ...
    _boto_update_members = ...
    _boto_delete_members = ...
    def __init__(self, sagemaker_session=..., **kwargs) -> None:
        """Init for _TrialComponent"""
        ...
    
    def save(self):
        """Save the state of this TrialComponent to SageMaker."""
        ...
    
    def delete(self, force_disassociate=...):
        """Delete this TrialComponent from SageMaker.

        Args:
            force_disassociate (boolean): Indicates whether to force disassociate the
                trial component with the trials before deletion (default: False).
                If set to true, force disassociate the trial component with associated trials
                first, then delete the trial component.
                If it's not set or set to false, it will delete the trial component directory
                without disassociation.

          Returns:
            dict: Delete trial component response.
        """
        ...
    
    @classmethod
    def load(cls, trial_component_name, sagemaker_session=...):
        """Load an existing trial component and return an `_TrialComponent` object representing it.

        Args:
            trial_component_name (str): Name of the trial component
            sagemaker_session (sagemaker.session.Session): Session object which
                manages interactions with Amazon SageMaker APIs and any other
                AWS services needed. If not specified, one is created using the
                default AWS configuration chain.

        Returns:
            experiments.trial_component._TrialComponent: A SageMaker `_TrialComponent` object
        """
        ...
    
    @classmethod
    def create(cls, trial_component_name, display_name=..., tags=..., sagemaker_session=...):
        """Create a trial component and return a `_TrialComponent` object representing it.

        Args:
            trial_component_name (str): The name of the trial component.
            display_name (str): Display name of the trial component used by Studio (default: None).
            tags (List[Dict[str, str]]): Tags to add to the trial component (default: None).
            sagemaker_session (sagemaker.session.Session): Session object which
                manages interactions with Amazon SageMaker APIs and any other
                AWS services needed. If not specified, one is created using the
                default AWS configuration chain.

        Returns:
            experiments.trial_component._TrialComponent: A SageMaker `_TrialComponent` object.
        """
        ...
    
    @classmethod
    def list(cls, source_arn=..., created_before=..., created_after=..., sort_by=..., sort_order=..., sagemaker_session=..., trial_name=..., experiment_name=..., max_results=..., next_token=...):
        """Return a list of trial component summaries.

        Args:
            source_arn (str): A SageMaker Training or Processing Job ARN (default: None).
            created_before (datetime.datetime): Return trial components created before this instant
                (default: None).
            created_after (datetime.datetime): Return trial components created after this instant
                (default: None).
            sort_by (str): Which property to sort results by. One of 'Name', 'CreationTime'
                (default: None).
            sort_order (str): One of 'Ascending', or 'Descending' (default: None).
            sagemaker_session (sagemaker.session.Session): Session object which
                manages interactions with Amazon SageMaker APIs and any other
                AWS services needed. If not specified, one is created using the
                default AWS configuration chain.
            trial_name (str): If provided only trial components related to the trial are returned
                (default: None).
            experiment_name (str): If provided only trial components related to the experiment are
                returned (default: None).
            max_results (int): maximum number of trial components to retrieve (default: None).
            next_token (str): token for next page of results (default: None).
        Returns:
            collections.Iterator[experiments._api_types.TrialComponentSummary]: An iterator
                over `TrialComponentSummary` objects.
        """
        ...
    
    @classmethod
    def search(cls, search_expression=..., sort_by=..., sort_order=..., max_results=..., sagemaker_session=...):
        """Search Experiment Trail Component.

        Returns SearchResults in the account matching the search criteria.

        Args:
            search_expression: (SearchExpression): A Boolean conditional statement (default: None).
                Resource objects must satisfy this condition to be included in search results.
                You must provide at least one subexpression, filter, or nested filter.
            sort_by (str): The name of the resource property used to sort the SearchResults
                (default: None).
            sort_order (str): How SearchResults are ordered. Valid values are Ascending or
                Descending (default: None).
            max_results (int): The maximum number of results to return in a SearchResponse
                (default: None).
            sagemaker_session (sagemaker.session.Session): Session object which
                manages interactions with Amazon SageMaker APIs and any other
                AWS services needed. If not specified, one is created using the
                default AWS configuration chain.

        Returns:
            collections.Iterator[SearchResult] : An iterator over search results matching the
            search criteria.
        """
        ...
    


