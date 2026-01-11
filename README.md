# ticket-booking-assignment

A simple backend service to manage event ticket bookings with correct handling of race conditions.

## Tech Stack
- Python 3.9
- Django & Django REST Framework
- PostgreSQL
- Docker & Docker Compose

## Features
- Create events with a fixed number of tickets
- Book tickets with concurrency safety
- Limit users to a maximum of 2 tickets per event
- Cancel tickets and return them to the pool

## Concurrency Handling
To avoid overselling tickets, database row-level locking is used when booking tickets. This ensures only one request can update the available ticket count at a time, even under heavy concurrent load.

## Running the Project

```bash
docker compose up --build
docker compose exec web python manage.py migrate
docker compose exec web python manage.py test

## API Endpoints

### Create Event
POST /api/events/
{
  "name": "Concert",
  "total_seats": 100
}

### Book Ticket
POST /api/book/
{
  "event_id": 1,
  "user_id": 10
}

### Cancel Ticket
POST /api/cancel/
{
  "ticket_id": 5
}