from django.core.exceptions import ValidationError
from django.db import models


class UserRole(models.TextChoices):
    STUDENT = "student", "Student"
    TEACHER = "teacher", "Teacher"
    ADMIN = "admin", "Admin"


class AccountStatus(models.TextChoices):
    ACTIVE = "active", "Active"
    SUSPENDED = "suspended", "Suspended"


class ResourceType(models.TextChoices):
    STUDY_ROOM = "study_room", "Study Room"
    LABORATORY = "laboratory", "Laboratory"
    SPORTS_COURT = "sports_court", "Sports Court"
    TUTORING = "tutoring", "Tutoring"


class ReservationStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    CONFIRMED = "confirmed", "Confirmed"
    CANCELLED = "cancelled", "Cancelled"


class User(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=UserRole.choices)
    account_status = models.CharField(
        max_length=20,
        choices=AccountStatus.choices,
        default=AccountStatus.ACTIVE,
    )

    class Meta:
        db_table = "users"
        ordering = ["name"]

    def clean(self) -> None:
        if not self.name.strip():
            raise ValidationError({"name": "Name cannot be empty."})

    def __str__(self) -> str:
        return f"{self.name} <{self.email}>"


class Resource(models.Model):
    name = models.CharField(max_length=120)
    resource_type = models.CharField(max_length=30, choices=ResourceType.choices)
    capacity = models.PositiveIntegerField()
    is_premium = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "resources"
        ordering = ["name"]

    def clean(self) -> None:
        if self.capacity <= 0:
            raise ValidationError({"capacity": "Capacity must be greater than zero."})

    def __str__(self) -> str:
        return self.name


class Schedule(models.Model):
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        db_table = "schedules"
        ordering = ["date", "start_time"]

    def clean(self) -> None:
        if self.start_time >= self.end_time:
            raise ValidationError(
                {"end_time": "End time must be greater than start time."}
            )

    def __str__(self) -> str:
        return f"{self.date} {self.start_time} - {self.end_time}"


class Reservation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=ReservationStatus.choices,
        default=ReservationStatus.PENDING,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="reservations",
    )
    resource = models.ForeignKey(
        Resource,
        on_delete=models.PROTECT,
        related_name="reservations",
    )
    schedule = models.OneToOneField(
        Schedule,
        on_delete=models.PROTECT,
        related_name="reservation",
    )
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        db_table = "reservations"
        ordering = ["-created_at"]

    def clean(self) -> None:
        if self.total_cost < 0:
            raise ValidationError({"total_cost": "Total cost cannot be negative."})

    def __str__(self) -> str:
        return f"Reservation #{self.pk} - {self.status}"