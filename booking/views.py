from django.core.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.viewsets import ViewSet

from booking.serializers import CancelTicketSerializer, CreateEventSerializer, TicketBookingSerializer
from booking.services import book_ticket, cancel_ticket, create_event


class TicketViewSet(ViewSet):
    def create_event(self, request):
        serializer = CreateEventSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"success": False, "errors": serializer.errors, "message": "Invalid request data"},
                status=HTTP_400_BAD_REQUEST,
            )

        event = create_event(
            name=serializer.validated_data["name"], total_seats=serializer.validated_data["total_seats"]
        )

        return Response(
            {
                "success": True,
                "event_id": event.id,
                "available_seats": event.available_seats,
            }
        )

    def book_ticket(self, request):
        serializer = TicketBookingSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"success": False, "errors": serializer.errors},
                status=HTTP_400_BAD_REQUEST,
            )

        data = serializer.validated_data

        try:
            ticket = book_ticket(event_id=data["event_id"], user_id=data["user_id"])
            return Response(
                {
                    "success": True,
                    "message": "Ticket booked successfully",
                    "ticket_id": ticket.id,
                }
            )
        except ValidationError as e:
            return Response(
                {"success": False, "errors": e.messages, "message": e.message},
                status=HTTP_400_BAD_REQUEST,
            )

    def cancel_ticket(self, request):
        serializer = CancelTicketSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"success": False, "errors": serializer.errors, "message": "Invalid request data"},
                status=HTTP_400_BAD_REQUEST,
            )

        cancel_ticket(ticket_id=serializer.validated_data["ticket_id"])

        return Response(
            {
                "success": True,
                "message": "Ticket cancelled successfully",
            }
        )
