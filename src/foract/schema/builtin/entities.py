from __future__ import annotations

from datetime import datetime
from uuid import UUID

from foract.enums.schema import (
    HypothesisStatus,
    InvestigationStatus,
    SchemaCategory,
)
from foract.schema.definition import SchemaDefinition

from ._helpers import field

# ============================================================================
# Process
# ============================================================================

PROCESS_SCHEMA = SchemaDefinition(
    name="Process",
    category=SchemaCategory.ENTITY,
    version="1.0",
    description="Operating system process.",
    fields=[
        field("pid", int, identity=True),
        field("ppid", int),
        field("name", str),
        field("path", str, required=False),
        field("create_time", datetime, required=False),
    ],
)

# ============================================================================
# File
# ============================================================================

FILE_SCHEMA = SchemaDefinition(
    name="File",
    category=SchemaCategory.ENTITY,
    version="1.0",
    description="Filesystem object.",
    fields=[
        field("path", str, identity=True),
        field("size", int),
        field("created_at", datetime, required=False),
        field("modified_at", datetime, required=False),
    ],
)

# ============================================================================
# Portable Executable
# ============================================================================

PE_SCHEMA = SchemaDefinition(
    name="PE",
    category=SchemaCategory.ENTITY,
    version="1.0",
    description="Portable Executable metadata.",
    fields=[
        field("path", str, identity=True),
        field("architecture", str),
        field("entry_point", int),
        field("image_base", int),
    ],
)

# ============================================================================
# Socket
# ============================================================================

SOCKET_SCHEMA = SchemaDefinition(
    name="Socket",
    category=SchemaCategory.ENTITY,
    version="1.0",
    description="Network socket.",
    fields=[
        field("protocol", str),
        field("local_address", str),
        field("remote_address", str, required=False),
        field("state", str),
    ],
)

# ============================================================================
# Registry Key
# ============================================================================

REGISTRY_KEY_SCHEMA = SchemaDefinition(
    name="RegistryKey",
    category=SchemaCategory.ENTITY,
    version="1.0",
    description="Windows Registry key.",
    fields=[
        field("path", str, identity=True),
        field("last_write_time", datetime),
    ],
)

# ============================================================================
# Hypothesis
# ============================================================================

HYPOTHESIS_SCHEMA = SchemaDefinition(
    name="Hypothesis",
    category=SchemaCategory.ENTITY,
    version="1.0",
    description="Current investigative belief regarding an activity, event, or conclusion.",
    fields=[
        field("id", UUID, identity=True),
        field("title", str),
        field("description", str, required=False),
        field(
            "status",
            HypothesisStatus,
        ),
        field(
            "confidence",
            float,
            validation_rule=lambda value: 0.0 <= value <= 1.0,
        ),
        field("created_at", datetime),
        field("updated_at", datetime),
        field("last_verified_at", datetime, required=False),
        field("update_count", int),
    ],
)

# ============================================================================
# Investigation
# ============================================================================

INVESTIGATION_SCHEMA = SchemaDefinition(
    name="Investigation",
    category=SchemaCategory.ENTITY,
    version="1.0",
    description="A forensic investigation grouping hypotheses and evidence.",
    fields=[
        field("id", UUID, identity=True),
        field("title", str),
        field("description", str, required=False),
        field(
            "status",
            InvestigationStatus,
        ),
        field("started_at", datetime),
        field("completed_at", datetime, required=False),
        field("user_metadata", dict, required=False),
    ],
)

ENTITY_SCHEMAS = (
    PROCESS_SCHEMA,
    FILE_SCHEMA,
    PE_SCHEMA,
    SOCKET_SCHEMA,
    REGISTRY_KEY_SCHEMA,
    HYPOTHESIS_SCHEMA,
    INVESTIGATION_SCHEMA,
)
