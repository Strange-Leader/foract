# FORACT Development Guidelines

## Code Style

- Python 3.12+
- Black
- Ruff
- MyPy (strict)

## Imports

- Use absolute imports.
- No wildcard imports.

## Classes

- One public class per file.
- Public classes require docstrings.

## Testing

- Every new module must include tests.
- New features are not complete until tests pass.

## Architecture

- Lower layers must not import higher layers.
- Do not change public APIs without discussion.
