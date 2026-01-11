from django.urls import path

from .views import TicketViewSet

urlpatterns = [
    path("events", TicketViewSet.as_view({"post": "create_event"}), name="create-event"),
    path("book", TicketViewSet.as_view({"post": "book_ticket"}), name="ticket-booking"),
    path("cancel", TicketViewSet.as_view({"post": "cancel_ticket"}), name="ticket-cancel"),
]
