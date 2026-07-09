from foract.exceptions.base import FORACTError


class ExecutionError(FORACTError):
    """Base exception for the execution subsystem."""


class DuplicateExecutionError(ExecutionError):
    """Raised when an execution with the same ID already exists."""


class ExecutionNotFoundError(ExecutionError):
    """Raised when an execution record cannot be found."""
