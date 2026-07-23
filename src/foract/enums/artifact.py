from enum import StrEnum


class ArtifactType(StrEnum):
    """
    Types of operational artifacts stored in Execution Memory.

    These values identify the concrete artifact subtype while allowing
    ExecutionMemory to store and retrieve all artifacts through a common
    interface.
    """

    EXECUTION_RECORD = "execution_record"
    EXECUTION_REPORT = "execution_report"
    VERIFICATION_REPORT = "verification_report"
