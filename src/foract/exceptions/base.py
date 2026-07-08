"""
FORACT exception hierarchy.

Every project-specific exception must inherit from FORACTError.
"""


class FORACTError(Exception):
    """Base exception for all FORACT errors."""


# ---------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------


class ConfigurationError(FORACTError):
    """Raised when configuration loading or validation fails."""


# ---------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------


class RegistryError(FORACTError):
    """Base class for registry-related errors."""


class SchemaError(RegistryError):
    """Raised when schema registration or lookup fails."""


class PluginError(RegistryError):
    """Raised when plugin registration or lookup fails."""


# ---------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------


class ValidationError(FORACTError):
    """Raised when data validation fails."""


# ---------------------------------------------------------------------
# Execution
# ---------------------------------------------------------------------


class ExecutionError(FORACTError):
    """Raised when an execution step fails."""
