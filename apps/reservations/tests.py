from datetime import date, time

from django.test import TestCase

from apps.reservations.models import (
    AccountStatus,
    ReservationStatus,
    Resource,
    ResourceType,
    User,
    UserRole,
)
from apps.reservations.services import CreateReservationService


class CreateReservationServiceTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            name="Juan Perez",
            email="juan@example.com",
            role=UserRole.STUDENT,
            account_status=AccountStatus.ACTIVE,
        )
        self.resource = Resource.objects.create(
            name="Sala 101",
            resource_type=ResourceType.STUDY_ROOM,
            capacity=8,
            is_premium=False,
            is_active=True,
        )

    def test_should_create_confirmed_reservation(self):
        service = CreateReservationService()

        reservation = service.execute(
            user_id=self.user.id,
            resource_id=self.resource.id,
            date=date(2026, 3, 10),
            start_time=time(10, 0),
            end_time=time(11, 0),
        )

        self.assertEqual(reservation.status, ReservationStatus.CONFIRMED)
        self.assertEqual(reservation.user.id, self.user.id)
        self.assertEqual(reservation.resource.id, self.resource.id)