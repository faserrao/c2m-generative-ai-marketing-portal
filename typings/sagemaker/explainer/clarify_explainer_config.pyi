"""
This type stub file was generated by pyright.
"""

from typing import List, Optional

"""
This type stub file was generated by pyright.
"""
class ClarifyTextConfig:
    """A parameter used to configure the SageMaker Clarify explainer to treat text features as text so that explanations are provided for individual units of text. Required only for NLP explainability."""
    def __init__(self, language: str, granularity: str) -> None:
        """Initialize a config object for text explainability.

        Args:
            language (str): Specifies the language of the text features in `ISO 639-1
                <https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes>`__ or `ISO 639-3
                <https://en.wikipedia.org/wiki/ISO_639-3>`__ code of a supported
                language. See valid values `here
                <https://docs.aws.amazon.com/sagemaker/latest/APIReference/API_ClarifyTextConfig.html#sagemaker-Type-ClarifyTextConfig-Language>`__.
            granularity (str): The unit of granularity for the analysis of text features. For
                example, if the unit is ``"token"``, then each token (like a word in English) of the
                text is treated as a feature. SHAP values are computed for each unit/feature.
                Accepted values are ``"token"``, ``"sentence"``, or ``"paragraph"``.
        """
        ...
    


class ClarifyShapBaselineConfig:
    """Configuration for the SHAP baseline of the Kernal SHAP algorithm."""
    def __init__(self, mime_type: Optional[str] = ..., shap_baseline: Optional[str] = ..., shap_baseline_uri: Optional[str] = ...) -> None:
        """Initialize a config object for SHAP baseline.

        Args:
            mime_type (str): Optional. The MIME type of the baseline data. Choose
                from ``"text/csv"`` or ``"application/jsonlines"``. (Default: ``"text/csv"``)
            shap_baseline (str): Optional. The inline SHAP baseline data in string format.
                ShapBaseline can have one or multiple records to be used as the baseline dataset.
                The format of the SHAP baseline file should be the same format as the training
                dataset. For example, if the training dataset is in CSV format and each record
                contains four features, and all features are numerical, then the format of the
                baseline data should also share these characteristics. For NLP of text columns, the
                baseline value should be the value used to replace the unit of text specified by
                the ``granularity`` of the
                :class:`~sagemaker.explainer.clarify_explainer_config.ClarifyTextConfig`
                parameter. The size limit for ``shap_baseline`` is 4 KB. Use the
                ``shap_baseline_uri`` parameter if you want to provide more than 4 KB of baseline
                data.
            shap_baseline_uri (str): Optional. The S3 URI where the SHAP baseline file is stored.
                The format of the SHAP baseline file should be the same format as the format of
                the training dataset. For example, if the training dataset is in CSV format,
                and each record in the training dataset has four features, and all features are
                numerical, then the baseline file should also have this same format. Each record
                should contain only the features. If you are using a virtual private cloud (VPC),
                the ``shap_baseline_uri`` should be accessible to the VPC.
        """
        ...
    


class ClarifyShapConfig:
    """Configuration for SHAP analysis using SageMaker Clarify Explainer."""
    def __init__(self, shap_baseline_config: ClarifyShapBaselineConfig, number_of_samples: Optional[int] = ..., seed: Optional[int] = ..., use_logit: Optional[bool] = ..., text_config: Optional[ClarifyTextConfig] = ...) -> None:
        """Initialize a config object for SHAP analysis.

        Args:
            shap_baseline_config (:class:`~sagemaker.explainer.clarify_explainer_config.ClarifyShapBaselineConfig`):
                The configuration for the SHAP baseline of the Kernal SHAP algorithm.
            number_of_samples (int): Optional. The number of samples to be used for analysis by the
                Kernal SHAP algorithm. The number of samples determines the size of the synthetic
                dataset, which has an impact on latency of explainability requests. For more
                information, see the `Synthetic data` of `Configure and create an endpoint
                <https://docs.aws.amazon.com/sagemaker/latest/dg/clarify-online-explainability-create-endpoint.html>`__.
            seed (int): Optional. The starting value used to initialize the random number generator
                in the explainer. Provide a value for this parameter to obtain a deterministic SHAP
                result.
            use_logit (bool): Optional. A Boolean toggle to indicate if you want to use the logit
                function (true) or log-odds units (false) for model predictions. (Default: false)
            text_config (:class:`~sagemaker.explainer.clarify_explainer_config.ClarifyTextConfig`):
                Optional. A parameter that indicates if text features are treated as text and
                explanations are provided for individual units of text. Required for NLP
                explainability only.
        """
        ...
    


class ClarifyInferenceConfig:
    """The inference configuration parameter for the model container."""
    def __init__(self, feature_headers: Optional[List[str]] = ..., feature_types: Optional[List[str]] = ..., features_attribute: Optional[str] = ..., probability_index: Optional[int] = ..., probability_attribute: Optional[str] = ..., label_index: Optional[int] = ..., label_attribute: Optional[str] = ..., label_headers: Optional[List[str]] = ..., max_payload_in_mb: Optional[int] = ..., max_record_count: Optional[int] = ..., content_template: Optional[str] = ...) -> None:
        """Initialize a config object for model container.

        Args:
            feature_headers (list[str]): Optional. The names of the features. If provided, these are
                included in the endpoint response payload to help readability of the
                ``InvokeEndpoint`` output.
            feature_types (list[str]): Optional. A list of data types of the features. Applicable
                only to NLP explainability. If provided, ``feature_types`` must have at least one
                ``'text'`` string (for example, ``['text']``). If ``feature_types`` is not provided,
                the explainer infers the feature types based on the baseline data. The feature
                types are included in the endpoint response payload.
            features_attribute (str): Optional. Provides the JMESPath expression to extract the
                features from a model container input in JSON Lines format. For example,
                if ``features_attribute`` is the JMESPath expression ``'myfeatures'``, it extracts a
                list of features ``[1,2,3]`` from request data ``'{"myfeatures":[1,2,3]}'``.
            probability_index (int): Optional. A zero-based index used to extract a probability
                value (score) or list from model container output in CSV format. If this value is
                not provided, the entire model container output will be treated as a probability
                value (score) or list. See examples `here
                <https://docs.aws.amazon.com/sagemaker/latest/APIReference/API_ClarifyInferenceConfig.html#sagemaker-Type-ClarifyInferenceConfig-ProbabilityIndex>`__.
            probability_attribute (str): Optional. A JMESPath expression used to extract the
                probability (or score) from the model container output if the model container
                is in JSON Lines format. See examples `here
                <https://docs.aws.amazon.com/sagemaker/latest/APIReference/API_ClarifyInferenceConfig.html#sagemaker-Type-ClarifyInferenceConfig-ProbabilityAttribute>`__.
            label_index (int): Optional. A zero-based index used to extract a label header or list
                of label headers from model container output in CSV format.
            label_attribute (str): Optional. A JMESPath expression used to locate the list of label
                headers in the model container output.
            label_headers (list[str]): Optional. For multiclass classification problems, the label
                headers are the names of the classes. Otherwise, the label header is the name of
                the predicted label. These are used to help readability for the output of the
                ``InvokeEndpoint`` API.
            max_payload_in_mb (int): Optional. The maximum payload size (MB) allowed of a request
                from the explainer to the model container. (Default: 6)
            max_record_count (int): Optional. The maximum number of records in a request that the
                model container can process when querying the model container for the predictions
                of a `synthetic dataset
                <https://docs.aws.amazon.com/sagemaker/latest/dg/clarify-online-explainability-create-endpoint.html#clarify-online-explainability-create-endpoint-synthetic>`__.
                A record is a unit of input data that inference can be made on, for example, a
                single line in CSV data. If ``max_record_count`` is ``1``, the model container
                expects one record per request. A value of 2 or greater means that the model expects
                batch requests, which can reduce overhead and speed up the inferencing process. If
                this parameter is not provided, the explainer will tune the record count per request
                according to the model container's capacity at runtime.
            content_template (str): Optional. A template string used to format a JSON record into an
                acceptable model container input. For example, a ``ContentTemplate`` string ``'{
                "myfeatures":$features}'`` will format a list of features ``[1,2,3]`` into the
                record string ``'{"myfeatures":[1,2,3]}'``. Required only when the model
                container input is in JSON Lines format.
        """
        ...
    


class ClarifyExplainerConfig:
    """The configuration parameters for the SageMaker Clarify explainer."""
    def __init__(self, shap_config: ClarifyShapConfig, enable_explanations: Optional[str] = ..., inference_config: Optional[ClarifyInferenceConfig] = ...) -> None:
        """Initialize a config object for online explainability with AWS SageMaker Clarify.

        Args:
            shap_config (:class:`~sagemaker.explainer.clarify_explainer_config.ClarifyShapConfig`):
                The configuration for SHAP analysis.
            enable_explanations (str): Optional. A `JMESPath boolean expression
                <https://docs.aws.amazon.com/sagemaker/latest/dg/clarify-online-explainability-create-endpoint.html#clarify-online-explainability-create-endpoint-enable>`__
                used to filter which records to explain (Default: None). If not specified,
                explanations are activated by default.
            inference_config (:class:`~sagemaker.explainer.clarify_explainer_config.ClarifyInferenceConfig`):
                Optional. The inference configuration parameter for the model container. (Default: None)
        """
        ...
    


