from enum import StrEnum


class ExecutionStatus(StrEnum):
    """
    Terminal status of a completed plugin execution.
    """

    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    TIMEOUT = "TIMEOUT"
    CANCELLED = "CANCELLED"
