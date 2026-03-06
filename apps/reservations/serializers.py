from rest_framework import serializers

from apps.reservations.models import Reservation, Resource, Schedule, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "name", "email", "role", "account_status"]


class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = [
            "id",
            "name",
            "resource_type",
            "capacity",
            "is_premium",
            "is_active",
        ]


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = ["id", "date", "start_time", "end_time"]


class ReservationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    resource = ResourceSerializer(read_only=True)
    schedule = ScheduleSerializer(read_only=True)

    class Meta:
        model = Reservation
        fields = [
            "id",
            "created_at",
            "status",
            "total_cost",
            "user",
            "resource",
            "schedule",
        ]


class CreateReservationInputSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    resource_id = serializers.IntegerField()
    date = serializers.DateField()
    start_time = serializers.TimeField()
    end_time = serializers.TimeField()


class CancelReservationOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ["id", "status"]