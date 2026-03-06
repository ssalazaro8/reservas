from decimal import Decimal

from apps.reservations.models import Reservation, ReservationStatus


class ReservationBuilder:
    def __init__(self) -> None:
        self._user = None
        self._resource = None
        self._schedule = None
        self._status = ReservationStatus.PENDING
        self._total_cost = Decimal("0.00")

    def with_user(self, user):
        self._user = user
        return self

    def with_resource(self, resource):
        self._resource = resource
        return self

    def with_schedule(self, schedule):
        self._schedule = schedule
        return self

    def with_status(self, status: str):
        self._status = status
        return self

    def with_total_cost(self, total_cost):
        self._total_cost = total_cost
        return self

    def build(self) -> Reservation:
        if self._user is None:
            raise ValueError("User is required.")
        if self._resource is None:
            raise ValueError("Resource is required.")
        if self._schedule is None:
            raise ValueError("Schedule is required.")

        return Reservation(
            user=self._user,
            resource=self._resource,
            schedule=self._schedule,
            status=self._status,
            total_cost=self._total_cost,
        )