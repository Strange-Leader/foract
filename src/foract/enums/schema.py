from enum import StrEnum


class SchemaCategory(StrEnum):
    """
    High-level classification of a FORACT schema.

    ENTITY:
        Semantic objects stored in the Evidence Graph.

    OPERATIONAL_ARTIFACT:
        Operational records stored in Execution Memory.
    """

    ENTITY = "entity"
    OPERATIONAL_ARTIFACT = "operational_artifact"


class HypothesisStatus(StrEnum):
    PROPOSED = "proposed"
    SUPPORTED = "supported"
    CONTRADICTED = "contradicted"
    INCONCLUSIVE = "inconclusive"
    REJECTED = "rejected"


class InvestigationStatus(StrEnum):
    ACTIVE = "active"
    COMPLETED = "completed"
    TERMINATED = "terminated"


class ExecutionReportStatus(StrEnum):
    SUCCESS = "success"
    PARTIAL_SUCCESS = "partial_success"
    FAILED = "failed"
    ABORTED = "aborted"


class VerificationResult(StrEnum):
    SUPPORTED = "supported"
    PARTIALLY_SUPPORTED = "partially_supported"
    CONTRADICTED = "contradicted"
    INCONCLUSIVE = "inconclusive"
