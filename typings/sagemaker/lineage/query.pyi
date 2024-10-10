"""
This type stub file was generated by pyright.
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union

"""This module contains code to query SageMaker lineage."""
class LineageEntityEnum(Enum):
    """Enum of lineage entities for use in a query filter."""
    TRIAL = ...
    ACTION = ...
    ARTIFACT = ...
    CONTEXT = ...
    TRIAL_COMPONENT = ...


class LineageSourceEnum(Enum):
    """Enum of lineage types for use in a query filter."""
    CHECKPOINT = ...
    DATASET = ...
    ENDPOINT = ...
    IMAGE = ...
    MODEL = ...
    MODEL_DATA = ...
    MODEL_DEPLOYMENT = ...
    MODEL_GROUP = ...
    MODEL_REPLACE = ...
    TENSORBOARD = ...
    TRAINING_JOB = ...
    APPROVAL = ...
    PROCESSING_JOB = ...
    TRANSFORM_JOB = ...


class LineageQueryDirectionEnum(Enum):
    """Enum of query filter directions."""
    BOTH = ...
    ASCENDANTS = ...
    DESCENDANTS = ...


class Edge:
    """A connecting edge for a lineage graph."""
    def __init__(self, source_arn: str, destination_arn: str, association_type: str) -> None:
        """Initialize ``Edge`` instance."""
        ...
    
    def __hash__(self) -> int:
        """Define hash function for ``Edge``."""
        ...
    
    def __eq__(self, other) -> bool:
        """Define equal function for ``Edge``."""
        ...
    
    def __str__(self) -> str:
        """Define string representation of ``Edge``.

        Format:
            {
                'source_arn': 'string',
                'destination_arn': 'string',
                'association_type': 'string'
            }

        """
        ...
    
    def __repr__(self):
        """Define string representation of ``Edge``.

        Format:
            {
                'source_arn': 'string',
                'destination_arn': 'string',
                'association_type': 'string'
            }

        """
        ...
    


class Vertex:
    """A vertex for a lineage graph."""
    def __init__(self, arn: str, lineage_entity: str, lineage_source: str, sagemaker_session) -> None:
        """Initialize ``Vertex`` instance."""
        ...
    
    def __hash__(self) -> int:
        """Define hash function for ``Vertex``."""
        ...
    
    def __eq__(self, other) -> bool:
        """Define equal function for ``Vertex``."""
        ...
    
    def __str__(self) -> str:
        """Define string representation of ``Vertex``.

        Format:
            {
                'arn': 'string',
                'lineage_entity': 'string',
                'lineage_source': 'string',
                '_session': <sagemaker.session.Session object>
            }

        """
        ...
    
    def __repr__(self):
        """Define string representation of ``Vertex``.

        Format:
            {
                'arn': 'string',
                'lineage_entity': 'string',
                'lineage_source': 'string',
                '_session': <sagemaker.session.Session object>
            }

        """
        ...
    
    def to_lineage_object(self):
        """Convert the ``Vertex`` object to its corresponding lineage object.

        Returns:
            A ``Vertex`` object to its corresponding ``Artifact``,``Action``, ``Context``
            or ``TrialComponent`` object.
        """
        ...
    


class PyvisVisualizer:
    """Create object used for visualizing graph using Pyvis library."""
    def __init__(self, graph_styles, pyvis_options: Optional[Dict[str, Any]] = ...) -> None:
        """Init for PyvisVisualizer.

        Args:
            graph_styles: A dictionary that contains graph style for node and edges by their type.
                Example: Display the nodes with different color by their lineage entity / different
                    shape by start arn.
                        lineage_graph_styles = {
                            "TrialComponent": {
                                "name": "Trial Component",
                                "style": {"background-color": "#f6cf61"},
                                "isShape": "False",
                            },
                            "Context": {
                                "name": "Context",
                                "style": {"background-color": "#ff9900"},
                                "isShape": "False",
                            },
                            "StartArn": {
                                "name": "StartArn",
                                "style": {"shape": "star"},
                                "isShape": "True",
                                "symbol": "★", # shape symbol for legend
                            },
                        }
            pyvis_options(optional): A dict containing PyVis options to customize visualization.
                (see https://visjs.github.io/vis-network/docs/network/#options for supported fields)
        """
        ...
    
    def render(self, elements, path=...):
        """Render graph for lineage query result.

        Args:
            elements: A dictionary that contains the node and the edges of the graph.
                Example:
                    elements["nodes"] contains list of tuples, each tuple represents a node
                        format: (node arn, node lineage source, node lineage entity,
                            node is start arn)
                    elements["edges"] contains list of tuples, each tuple represents an edge
                        format: (edge source arn, edge destination arn, edge association type)

            path(optional): The path/filename of the rendered graph html file.
                (default path: "lineage_graph_pyvis.html")

        Returns:
            display graph: The interactive visualization is presented as a static HTML file.

        """
        ...
    


class LineageQueryResult:
    """A wrapper around the results of a lineage query."""
    def __init__(self, edges: List[Edge] = ..., vertices: List[Vertex] = ..., startarn: List[str] = ...) -> None:
        """Init for LineageQueryResult.

        Args:
            edges (List[Edge]): The edges of the query result.
            vertices (List[Vertex]): The vertices of the query result.
        """
        ...
    
    def __str__(self) -> str:
        """Define string representation of ``LineageQueryResult``.

        Format:
        {
            'edges':[
                {
                    'source_arn': 'string',
                    'destination_arn': 'string',
                    'association_type': 'string'
                },
            ],

            'vertices':[
                {
                    'arn': 'string',
                    'lineage_entity': 'string',
                    'lineage_source': 'string',
                    '_session': <sagemaker.session.Session object>
                },
            ],

            'startarn':['string', ...]
        }

        """
        ...
    
    def visualize(self, path: Optional[str] = ..., pyvis_options: Optional[Dict[str, Any]] = ...): # -> Any:
        """Visualize lineage query result.

        Creates a PyvisVisualizer object to render network graph with Pyvis library.
        Pyvis library should be installed before using this method (run "pip install pyvis")
        The elements(nodes & edges) are preprocessed in this method and sent to
        PyvisVisualizer for rendering graph.

        Args:
            path(optional): The path/filename of the rendered graph html file.
                (default path: "lineage_graph_pyvis.html")
            pyvis_options(optional): A dict containing PyVis options to customize visualization.
                (see https://visjs.github.io/vis-network/docs/network/#options for supported fields)

        Returns:
            display graph: The interactive visualization is presented as a static HTML file.
        """
        ...
    


class LineageFilter:
    """A filter used in a lineage query."""
    def __init__(self, entities: Optional[List[Union[LineageEntityEnum, str]]] = ..., sources: Optional[List[Union[LineageSourceEnum, str]]] = ..., created_before: Optional[datetime] = ..., created_after: Optional[datetime] = ..., modified_before: Optional[datetime] = ..., modified_after: Optional[datetime] = ..., properties: Optional[Dict[str, str]] = ...) -> None:
        """Initialize ``LineageFilter`` instance."""
        ...
    


class LineageQuery:
    """Creates an object used for performing lineage queries."""
    def __init__(self, sagemaker_session) -> None:
        """Initialize ``LineageQuery`` instance."""
        ...
    
    def query(self, start_arns: List[str], direction: LineageQueryDirectionEnum = ..., include_edges: bool = ..., query_filter: LineageFilter = ..., max_depth: int = ...) -> LineageQueryResult:
        """Perform a lineage query.

        Args:
            start_arns (List[str]): A list of ARNs that will be used as the starting point
                for the query.
            direction (LineageQueryDirectionEnum, optional): The direction of the query.
            include_edges (bool, optional): If true, return edges in addition to vertices.
            query_filter (LineageQueryFilter, optional): The query filter.

        Returns:
            LineageQueryResult: The lineage query result.
        """
        ...
    


