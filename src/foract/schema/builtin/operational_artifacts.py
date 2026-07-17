from __future__ import annotations

from datetime import datetime
from uuid import UUID

from foract.enums.schema import (
    ExecutionReportStatus,
    SchemaCategory,
    VerificationResult,
)
from foract.schema.definition import SchemaDefinition

from ._helpers import field

# ============================================================================
# Execution Record
# ============================================================================
# NOTE:
# This schema represents the ExecutionRecord ontology.
# It should remain synchronized with the concrete
# ExecutionRecord model implemented in Phase 2.
EXECUTION_RECORD_SCHEMA = SchemaDefinition(
    name="ExecutionRecord",
    category=SchemaCategory.OPERATIONAL_ARTIFACT,
    version="1.0",
    description="Immutable record of a single plugin execution.",
    fields=[
        field("id", UUID, identity=True),
        field("plugin_name", str),
        field("capability", str),
        field("status", str),
        field("started_at", datetime),
        field("completed_at", datetime),
    ],
)

# ============================================================================
# Execution Report
# ============================================================================

EXECUTION_REPORT_SCHEMA = SchemaDefinition(
    name="ExecutionReport",
    category=SchemaCategory.OPERATIONAL_ARTIFACT,
    version="1.0",
    description="Summary of an orchestration execution.",
    fields=[
        field("id", UUID, identity=True),
        field("batch_id", str),
        field(
            "status",
            ExecutionReportStatus,
        ),
        field("completed_nodes", list),
        field("failed_nodes", list),
        field("skipped_nodes", list),
        field("started_at", datetime),
        field("completed_at", datetime),
    ],
)

# ============================================================================
# Verification Report
# ============================================================================

VERIFICATION_REPORT_SCHEMA = SchemaDefinition(
    name="VerificationReport",
    category=SchemaCategory.OPERATIONAL_ARTIFACT,
    version="1.0",
    description="Result of a single hypothesis verification.",
    fields=[
        field("id", UUID, identity=True),
        field("hypothesis_id", UUID),
        field("hypothesis_update_count", int),
        field(
            "verification_result",
            VerificationResult,
        ),
        field(
            "confidence_before",
            float,
            validation_rule=lambda x: 0.0 <= x <= 1.0,
        ),
        field(
            "confidence_after",
            float,
            validation_rule=lambda x: 0.0 <= x <= 1.0,
        ),
        field("supporting_evidence_ids", list),
        field("contradicting_evidence_ids", list),
        field("created_at", datetime),
    ],
)

OPERATIONAL_ARTIFACT_SCHEMAS = (
    EXECUTION_RECORD_SCHEMA,
    EXECUTION_REPORT_SCHEMA,
    VERIFICATION_REPORT_SCHEMA,
)
