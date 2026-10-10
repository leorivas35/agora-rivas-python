class DomainError(Exception):
    """Base exception for domain-level validation errors."""


class InvalidEmailError(DomainError):
    """Raised when an email address does not pass validation."""
