from foract.exceptions import ValidationError
from foract.schema import PROCESS_SCHEMA, validate_node


def main() -> None:
    print("=" * 60)
    print("FORACT Schema Validation Example")
    print("=" * 60)

    valid_node = {
        "pid": 4,
        "ppid": 0,
        "name": "System",
        "path": r"C:\Windows\System32\System",
    }

    try:
        validate_node(PROCESS_SCHEMA, valid_node)
        print("✓ Valid node passed validation.")
    except ValidationError as exc:
        print(f"✗ Validation failed: {exc}")

    print()

    invalid_node = {
        "pid": "four",  # Wrong type
        "name": "System",
    }

    try:
        validate_node(PROCESS_SCHEMA, invalid_node)
        print("✓ Invalid node passed validation.")
    except ValidationError as exc:
        print(f"✗ Validation failed as expected: {exc}")


if __name__ == "__main__":
    main()
