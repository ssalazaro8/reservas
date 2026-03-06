from django.contrib import admin

from apps.reservations.models import Reservation, Resource, Schedule, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "role", "account_status")
    search_fields = ("name", "email")
    list_filter = ("role", "account_status")


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "resource_type", "capacity", "is_premium", "is_active")
    search_fields = ("name",)
    list_filter = ("resource_type", "is_premium", "is_active")


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ("id", "date", "start_time", "end_time")
    list_filter = ("date",)


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "resource", "status", "total_cost", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("user__name", "resource__name")