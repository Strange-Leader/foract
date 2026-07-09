from __future__ import annotations

from foract.exceptions.base import FORACTError


class GraphError(FORACTError):
    """Base class for all graph-related exceptions."""


class DuplicateNodeError(GraphError):
    """Raised when a node with the same ID already exists."""


class DuplicateEdgeError(GraphError):
    """Raised when an edge with the same ID already exists."""


class NodeNotFoundError(GraphError):
    """Raised when a node cannot be found."""


class EdgeNotFoundError(GraphError):
    """Raised when an edge cannot be found."""
