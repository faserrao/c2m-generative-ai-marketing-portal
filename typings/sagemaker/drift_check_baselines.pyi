"""
This type stub file was generated by pyright.
"""

from typing import Optional
from sagemaker.model_metrics import FileSource, MetricsSource

"""
This type stub file was generated by pyright.
"""
class DriftCheckBaselines:
    """Accepts drift check baselines parameters for conversion to request dict."""
    def __init__(self, model_statistics: Optional[MetricsSource] = ..., model_constraints: Optional[MetricsSource] = ..., model_data_statistics: Optional[MetricsSource] = ..., model_data_constraints: Optional[MetricsSource] = ..., bias_config_file: Optional[FileSource] = ..., bias_pre_training_constraints: Optional[MetricsSource] = ..., bias_post_training_constraints: Optional[MetricsSource] = ..., explainability_constraints: Optional[MetricsSource] = ..., explainability_config_file: Optional[FileSource] = ...) -> None:
        """Initialize a ``DriftCheckBaselines`` instance and turn parameters into dict.

        Args:
            model_statistics (MetricsSource): A metric source object that represents
                model statistics (default: None).
            model_constraints (MetricsSource): A metric source object that represents
                model constraints (default: None).
            model_data_statistics (MetricsSource): A metric source object that represents
                model data statistics (default: None).
            model_data_constraints (MetricsSource): A metric source object that represents
                model data constraints (default: None).
            bias_config_file (FileSource): A file source object that represents bias config
                (default: None).
            bias_pre_training_constraints (MetricsSource):
                A metric source object that represents Pre-training constraints (default: None).
            bias_post_training_constraints (MetricsSource):
                A metric source object that represents Post-training constraits (default: None).
            explainability_constraints (MetricsSource):
                A metric source object that represents explainability constraints (default: None).
            explainability_config_file (FileSource): A file source object that represents
                explainability config (default: None).
        """
        ...
    


