"""
This type stub file was generated by pyright.
"""

from typing import Optional, Union
from sagemaker.workflow.entities import PipelineVariable

"""
This type stub file was generated by pyright.
"""
class ModelMetrics:
    """Accepts model metrics parameters for conversion to request dict."""
    def __init__(self, model_statistics: Optional[MetricsSource] = ..., model_constraints: Optional[MetricsSource] = ..., model_data_statistics: Optional[MetricsSource] = ..., model_data_constraints: Optional[MetricsSource] = ..., bias: Optional[MetricsSource] = ..., explainability: Optional[MetricsSource] = ..., bias_pre_training: Optional[MetricsSource] = ..., bias_post_training: Optional[MetricsSource] = ...) -> None:
        """Initialize a ``ModelMetrics`` instance and turn parameters into dict.

        Args:
            model_statistics (MetricsSource): A metric source object that represents
                model statistics (default: None).
            model_constraints (MetricsSource): A metric source object that represents
                model constraints (default: None).
            model_data_statistics (MetricsSource): A metric source object that represents
                model data statistics (default: None).
            model_data_constraints (MetricsSource): A metric source object that represents
                model data constraints (default: None).
            bias (MetricsSource): A metric source object that represents bias report
                (default: None).
            explainability (MetricsSource): A metric source object that represents
                explainability report (default: None).
            bias_pre_training (MetricsSource): A metric source object that represents
                Pre-training report (default: None).
            bias_post_training (MetricsSource): A metric source object that represents
                Post-training report (default: None).
        """
        ...
    


class MetricsSource:
    """Accepts metrics source parameters for conversion to request dict."""
    def __init__(self, content_type: Union[str, PipelineVariable], s3_uri: Union[str, PipelineVariable], content_digest: Optional[Union[str, PipelineVariable]] = ...) -> None:
        """Initialize a ``MetricsSource`` instance and turn parameters into dict.

        Args:
            content_type (str or PipelineVariable): Specifies the type of content
                in S3 URI
            s3_uri (str or PipelineVariable): The S3 URI of the metric
            content_digest (str or PipelineVariable): The digest of the metric
                (default: None)
        """
        ...
    


class FileSource:
    """Accepts file source parameters for conversion to request dict."""
    def __init__(self, s3_uri: Union[str, PipelineVariable], content_digest: Optional[Union[str, PipelineVariable]] = ..., content_type: Optional[Union[str, PipelineVariable]] = ...) -> None:
        """Initialize a ``FileSource`` instance and turn parameters into dict.

        Args:
            s3_uri (str or PipelineVariable): The S3 URI of the metric
            content_digest (str or PipelineVariable): The digest of the metric
                (default: None)
            content_type (str or PipelineVariable): Specifies the type of content
                in S3 URI (default: None)
        """
        ...
    


