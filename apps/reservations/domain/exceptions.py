class DomainException(Exception):
    """Base exception for domain and application errors."""


class UserNotFoundError(DomainException):
    pass


class ResourceNotFoundError(DomainException):
    pass


class ReservationNotFoundError(DomainException):
    pass


class UserNotEligibleError(DomainException):
    pass


class ResourceUnavailableError(DomainException):
    pass


class InvalidScheduleError(DomainException):
    pass


class PaymentFailedError(DomainException):
    pass


class ReservationAlreadyCancelledError(DomainException):
    pass