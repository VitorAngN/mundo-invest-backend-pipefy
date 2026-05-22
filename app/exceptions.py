class DomainError(Exception):
    """Base exception for business-rule errors."""


class ClienteAlreadyExistsError(DomainError):
    pass


class ClienteNotFoundError(DomainError):
    pass

