from rest_framework import serializers

from .models import Event, Ticket


class CreateEventSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    total_seats = serializers.IntegerField(min_value=1)


class TicketBookingSerializer(serializers.Serializer):
    event_id = serializers.IntegerField()
    user_id = serializers.IntegerField()

    def validate_event_id(self, value):
        if not Event.objects.filter(id=value).exists():
            raise serializers.ValidationError("Event not found")
        return value


class CancelTicketSerializer(serializers.Serializer):
    ticket_id = serializers.IntegerField()

    def validate_ticket_id(self, value):
        if not Ticket.objects.filter(id=value).exists():
            raise serializers.ValidationError("Ticket not found")
        return value
