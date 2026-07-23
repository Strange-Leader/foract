from __future__ import annotations

from foract.exceptions.base import FORACTError


class ExecutionError(FORACTError):
    """
    Base exception for the execution subsystem.
    """


class DuplicateArtifactError(ExecutionError):
    """
    Raised when an operational artifact with the same ID
    already exists in Execution Memory.
    """


class ArtifactNotFoundError(ExecutionError):
    """
    Raised when an operational artifact cannot be found.
    """


class InvalidArtifactTypeError(ExecutionError):
    """
    Raised when an operation is requested for an
    incompatible operational artifact type.
    """


class DuplicateBlobError(ExecutionError):
    """
    Raised when attempting to store a blob whose ID
    already exists.
    """


class BlobNotFoundError(ExecutionError):
    """
    Raised when a requested blob cannot be found.
    """
