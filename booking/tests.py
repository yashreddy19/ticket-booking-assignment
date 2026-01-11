import threading

from django.db import connection
from django.test import TransactionTestCase

from .models import Event, Ticket
from .services import book_ticket


class TicketBookingConcurrencyTest(TransactionTestCase):
    def setUp(self):
        self.movie_event = Event.objects.create(name="Movie", total_seats=1, available_seats=1)
        self.concert_event = Event.objects.create(name="Concert", total_seats=5, available_seats=5)

    def attempt_booking(self, results, user_id):
        connection.close()
        try:
            result = book_ticket(event_id=self.movie_event.id, user_id=user_id)
            results.append("SUCCESS")
        except Exception:
            results.append("FAILED")

    def test_concurrent_booking(self):
        results = []
        threads = []

        for user_id in range(5):
            t = threading.Thread(target=self.attempt_booking, args=(results, user_id))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        self.assertEqual(results.count("SUCCESS"), 1, f"Results: {results}")
        self.assertEqual(Ticket.objects.count(), 1)

    def test_user_cannot_book_more_than_two_tickets(self):

        # First booking
        book_ticket(event_id=self.concert_event.id, user_id=1)
        # Second booking
        book_ticket(event_id=self.concert_event.id, user_id=1)

        # Third booking fails
        with self.assertRaises(Exception):
            book_ticket(event_id=self.concert_event.id, user_id=1)

        self.assertEqual(Ticket.objects.filter(event=self.concert_event, user_id=1).count(), 2)
