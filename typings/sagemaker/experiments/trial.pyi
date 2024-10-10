"""
This type stub file was generated by pyright.
"""

from sagemaker.apiutils import _base_types

"""Contains the Trial class."""
class _Trial(_base_types.Record):
    """An execution of a data-science workflow with an experiment.

    Consists of a list of trial component objects, which document individual
    activities within the workflow.

    Attributes:
        trial_name (str): The name of the trial.
        experiment_name (str): The name of the trial's experiment.
        display_name (str): The name of the trial that will appear in UI,
            such as SageMaker Studio.
        tags (List[Dict[str, str]]): A list of tags to associate with the trial.
    """
    trial_name = ...
    experiment_name = ...
    display_name = ...
    tags = ...
    _boto_create_method = ...
    _boto_load_method = ...
    _boto_delete_method = ...
    _boto_update_method = ...
    _boto_update_members = ...
    _boto_delete_members = ...
    def save(self):
        """Save the state of this Trial to SageMaker.

        Returns:
            dict: Update trial response.
        """
        ...
    
    def delete(self):
        """Delete this Trial from SageMaker.

        Does not delete associated Trial Components.

        Returns:
            dict: Delete trial response.
        """
        ...
    
    @classmethod
    def load(cls, trial_name, sagemaker_session=...):
        """Load an existing trial and return a `_Trial` object.

        Args:
            trial_name: (str): Name of the Trial.
            sagemaker_session (sagemaker.session.Session): Session object which
                manages interactions with Amazon SageMaker APIs and any other
                AWS services needed. If not specified, one is created using the
                default AWS configuration chain.

        Returns:
            experiments.trial._Trial: A SageMaker `_Trial` object
        """
        ...
    
    @classmethod
    def create(cls, experiment_name, trial_name, display_name=..., tags=..., sagemaker_session=...):
        """Create a new trial and return a `_Trial` object.

        Args:
            experiment_name: (str): Name of the experiment to create this trial in.
            trial_name: (str): Name of the Trial.
            display_name (str): Name of the trial that will appear in UI,
                such as SageMaker Studio (default: None).
            tags (List[dict]): A list of tags to associate with the trial (default: None).
            sagemaker_session (sagemaker.session.Session): Session object which
                manages interactions with Amazon SageMaker APIs and any other
                AWS services needed. If not specified, one is created using the
                default AWS configuration chain.

        Returns:
            experiments.trial._Trial: A SageMaker `_Trial` object
        """
        ...
    
    @classmethod
    def list(cls, experiment_name=..., trial_component_name=..., created_before=..., created_after=..., sort_by=..., sort_order=..., sagemaker_session=...):
        """List all trials matching the specified criteria.

        Args:
            experiment_name (str): Name of the experiment. If specified, only trials in
                the experiment will be returned (default: None).
            trial_component_name (str): Name of the trial component. If specified, only
                trials with this trial component name will be returned (default: None).
            created_before (datetime.datetime): Return trials created before this instant
                (default: None).
            created_after (datetime.datetime): Return trials created after this instant
                (default: None).
            sort_by (str): Which property to sort results by. One of 'Name', 'CreationTime'
                (default: None).
            sort_order (str): One of 'Ascending', or 'Descending' (default: None).
            sagemaker_session (sagemaker.session.Session): Session object which
                manages interactions with Amazon SageMaker APIs and any other
                AWS services needed. If not specified, one is created using the
                default AWS configuration chain.
        Returns:
            collections.Iterator[experiments._api_types.TrialSummary]: An iterator over trials
                matching the specified criteria.
        """
        ...
    
    def add_trial_component(self, trial_component):
        """Add the specified trial component to this trial.

        A trial component may belong to many trials and a trial may have many trial components.

        Args:
            trial_component (str or _TrialComponent): The trial component to add.
                Can be one of a _TrialComponent instance, or a string containing
                the name of the trial component to add.
        """
        ...
    
    def remove_trial_component(self, trial_component):
        """Remove the specified trial component from this trial.

        Args:
            trial_component (str or _TrialComponent): The trial component to add.
                Can be one of a _TrialComponent instance, or a string containing
                the name of the trial component to add.
        """
        ...
    
    def list_trial_components(self, created_before=..., created_after=..., sort_by=..., sort_order=..., max_results=..., next_token=...):
        """List trial components in this trial matching the specified criteria.

        Args:
            created_before (datetime.datetime): Return trials created before this instant
                (default: None).
            created_after (datetime.datetime): Return trials created after this instant
                (default: None).
            sort_by (str): Which property to sort results by. One of 'Name',
                'CreationTime' (default: None).
            sort_order (str): One of 'Ascending', or 'Descending' (default: None).
            max_results (int): maximum number of trial components to retrieve (default: None).
            next_token (str): token for next page of results (default: None).

        Returns:
            collections.Iterator[experiments._api_types.TrialComponentSummary] : An iterator over
                trials matching the criteria.
        """
        ...
    


