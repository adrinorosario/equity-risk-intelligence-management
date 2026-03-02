# TLDR; Shared exception types for services/engine.
# TODO: Add domain-specific error mapping to HTTP responses in the API layer.


class ERIMSError(Exception):
    """Base exception for ERIMS backend."""


class NotImplementedFeatureError(ERIMSError):
    """Raised when an endpoint/service is intentionally scaffolded only."""
