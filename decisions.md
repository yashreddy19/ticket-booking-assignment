# Design Decisions

## 1. Database Structure
A relational database with separate `Event` and `Ticket` tables was chosen to maintain strong consistency, support per-user booking limits, and allow safe ticket cancellation.

## 2. Race Condition Handling
Row-level locking using database transactions (`SELECT FOR UPDATE`) was used to prevent overselling under concurrent requests.

## 3. Scaling Considerations
At very high traffic, contention on popular event rows becomes the bottleneck. This could be addressed in the future using Redis-based distributed locking to reduce database contention.