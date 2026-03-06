from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.reservations.domain.exceptions import (
    InvalidScheduleError,
    PaymentFailedError,
    ReservationAlreadyCancelledError,
    ReservationNotFoundError,
    ResourceNotFoundError,
    ResourceUnavailableError,
    UserNotEligibleError,
    UserNotFoundError,
)
from apps.reservations.models import Resource
from apps.reservations.serializers import (
    CancelReservationOutputSerializer,
    CreateReservationInputSerializer,
    ReservationSerializer,
    ResourceSerializer,
)
from apps.reservations.services import (
    CancelReservationService,
    CreateReservationService,
    ListUserReservationHistoryService,
)


class ResourceListAPIView(APIView):
    def get(self, request):
        resources = Resource.objects.all()
        serializer = ResourceSerializer(resources, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ReservationCreateAPIView(APIView):
    def post(self, request):
        input_serializer = CreateReservationInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        service = CreateReservationService(payment_provider="fake")

        try:
            reservation = service.execute(**input_serializer.validated_data)
        except (UserNotFoundError, ResourceNotFoundError) as exc:
            return Response(
                {"detail": str(exc)},
                status=status.HTTP_404_NOT_FOUND,
            )
        except (
            InvalidScheduleError,
            UserNotEligibleError,
            PaymentFailedError,
        ) as exc:
            return Response(
                {"detail": str(exc)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except ResourceUnavailableError as exc:
            return Response(
                {"detail": str(exc)},
                status=status.HTTP_409_CONFLICT,
            )

        output_serializer = ReservationSerializer(reservation)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)


class ReservationCancelAPIView(APIView):
    def delete(self, request, reservation_id: int):
        service = CancelReservationService()

        try:
            reservation = service.execute(reservation_id=reservation_id)
        except ReservationNotFoundError as exc:
            return Response(
                {"detail": str(exc)},
                status=status.HTTP_404_NOT_FOUND,
            )
        except ReservationAlreadyCancelledError as exc:
            return Response(
                {"detail": str(exc)},
                status=status.HTTP_409_CONFLICT,
            )

        serializer = CancelReservationOutputSerializer(reservation)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserReservationHistoryAPIView(APIView):
    def get(self, request, user_id: int):
        service = ListUserReservationHistoryService()

        try:
            reservations = service.execute(user_id=user_id)
        except UserNotFoundError as exc:
            return Response(
                {"detail": str(exc)},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = ReservationSerializer(reservations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)