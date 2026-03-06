from django.urls import path

from apps.reservations.views import (
    ReservationCancelAPIView,
    ReservationCreateAPIView,
    ResourceListAPIView,
    UserReservationHistoryAPIView,
)

urlpatterns = [
    path("resources/", ResourceListAPIView.as_view(), name="resource-list"),
    path("reservations/", ReservationCreateAPIView.as_view(), name="reservation-create"),
    path(
        "reservations/<int:reservation_id>/cancel/",
        ReservationCancelAPIView.as_view(),
        name="reservation-cancel",
    ),
    path(
        "users/<int:user_id>/reservations/",
        UserReservationHistoryAPIView.as_view(),
        name="user-reservation-history",
    ),
]