from foract.schema import FieldDefinition


def test_field_definition_defaults() -> None:
    field = FieldDefinition(
        name="pid",
        field_type=int,
    )

    assert field.name == "pid"
    assert field.field_type is int
    assert field.required is True
    assert field.description == ""


def test_optional_field() -> None:
    field = FieldDefinition(
        name="command_line",
        field_type=str,
        required=False,
        description="Process command line",
    )

    assert field.required is False
    assert field.description == "Process command line"
