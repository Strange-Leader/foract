from __future__ import annotations

from typing import TYPE_CHECKING

from foract.schema.definition import SchemaDefinition
from foract.schema.field import FieldDefinition

if TYPE_CHECKING:
    from foract.registry import SchemaRegistry

PROCESS_SCHEMA = SchemaDefinition(
    name="Process",
    version="1.0",
    description="Operating system process.",
    fields=[
        FieldDefinition(name="pid", field_type=int, identity=True),
        FieldDefinition(name="ppid", field_type=int),
        FieldDefinition(name="name", field_type=str),
        FieldDefinition(name="path", field_type=str, required=False),
        FieldDefinition(name="create_time", field_type=str, required=False),
    ],
)

FILE_SCHEMA = SchemaDefinition(
    name="File",
    version="1.0",
    description="Filesystem object.",
    fields=[
        FieldDefinition(
            name="path",
            field_type=str,
            identity=True,
        ),
        FieldDefinition(name="size", field_type=int),
        FieldDefinition(name="created", field_type=str, required=False),
        FieldDefinition(name="modified", field_type=str, required=False),
    ],
)

PE_SCHEMA = SchemaDefinition(
    name="PE",
    version="1.0",
    description="Portable Executable metadata.",
    fields=[
        FieldDefinition(
            name="path",
            field_type=str,
            identity=True,
        ),
        FieldDefinition(name="architecture", field_type=str),
        FieldDefinition(name="entry_point", field_type=int),
        FieldDefinition(name="image_base", field_type=int),
    ],
)

SOCKET_SCHEMA = SchemaDefinition(
    name="Socket",
    version="1.0",
    description="Network socket.",
    fields=[
        FieldDefinition(name="protocol", field_type=str),
        FieldDefinition(name="local_address", field_type=str),
        FieldDefinition(
            name="remote_address",
            field_type=str,
            required=False,
        ),
        FieldDefinition(name="state", field_type=str),
    ],
)

REGISTRY_KEY_SCHEMA = SchemaDefinition(
    name="RegistryKey",
    version="1.0",
    description="Windows Registry key.",
    fields=[
        FieldDefinition(
            name="path",
            field_type=str,
            identity=True,
        ),
        FieldDefinition(name="last_write_time", field_type=str),
    ],
)

EXECUTION_RECORD_SCHEMA = SchemaDefinition(
    name="ExecutionRecord",
    version="1.0",
    description="Program execution record.",
    fields=[
        FieldDefinition(name="process_name", field_type=str),
        FieldDefinition(name="path", field_type=str),
        FieldDefinition(name="execution_time", field_type=str),
    ],
)

BUILTIN_SCHEMAS = [
    PROCESS_SCHEMA,
    FILE_SCHEMA,
    PE_SCHEMA,
    SOCKET_SCHEMA,
    REGISTRY_KEY_SCHEMA,
    EXECUTION_RECORD_SCHEMA,
]


def register_builtin_schemas(registry: SchemaRegistry) -> None:
    for schema in BUILTIN_SCHEMAS:
        registry.register(schema)
