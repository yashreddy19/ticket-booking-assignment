from django.core.exceptions import ValidationError
from django.db import transaction

from .models import Event, Ticket


def create_event(name: str, total_seats: int):
    return Event.objects.create(
        name=name,
        total_seats=total_seats,
        available_seats=total_seats,
    )


def book_ticket(event_id: int, user_id: int):
    with transaction.atomic():
        event = Event.objects.select_for_update().get(id=event_id)

        # Enforce max 2 tickets per user per event
        user_ticket_count = Ticket.objects.filter(event=event, user_id=user_id).count()

        if user_ticket_count >= 2:
            raise ValidationError("User cannot book more than 2 tickets for this event")

        if event.available_seats <= 0:
            raise ValidationError("No seats available")

        event.available_seats -= 1
        event.save()

        return Ticket.objects.create(event=event, user_id=user_id)


def cancel_ticket(ticket_id: int):
    with transaction.atomic():
        ticket = Ticket.objects.select_for_update().get(id=ticket_id)
        event = ticket.event

        ticket.delete()
        event.available_seats += 1
        event.save()
