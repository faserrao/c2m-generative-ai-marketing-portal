"""
This type stub file was generated by pyright.
"""

from typing import TYPE_CHECKING
from sagemaker.experiments import Run

"""Contains the SageMaker Experiment _RunContext class."""
if TYPE_CHECKING:
    ...
class _RunContext:
    """A static context variable to keep track of the current Run object"""
    _context_run = ...
    @classmethod
    def add_run_object(cls, run: Run): # -> None:
        """Keep track of the current executing Run object

        by adding it to a class static variable.

        Args:
            run (Run): The current Run object to be tracked.
        """
        ...
    
    @classmethod
    def drop_current_run(cls) -> Run:
        """Drop the Run object tracked in the global static variable

        as its execution finishes (its "with" block ends).

        Return:
            Run: the dropped Run object.
        """
        ...
    
    @classmethod
    def get_current_run(cls) -> Run:
        """Return the current Run object without dropping it.

        Return:
            Run: the current Run object to be returned.
        """
        ...
    


