# Rate Limiter

A backend rate limiting service built using **FastAPI** and **PostgreSQL** by applying the **Token Bucket Algorithm**.

This project was created to understand how rate limiting works in real backend systems, how middleware can intercept requests, and how token refill logic can be implemented using database-backed state.

---

## What is Rate Limiting?

Rate limiting is a security and performance technique that controls the number of requests a user or client can make to a server within a specific timeframe.

It helps in:

- Preventing abuse or spam
- Protecting backend resources
- Improving API stability
- Handling traffic bursts in a controlled way
- Defending against brute-force or denial-of-service style request floods or attacks

For example, if a client keeps sending requests too quickly, the server can reject extra requests with a **429 Too Many Requests** response.

---

## Token Bucket Algorithm

This project uses the **Token Bucket** algorithm.

### How it works

- Each client has a bucket
- The bucket has a maximum capacity
- Tokens are added back to the bucket at a fixed refill rate
- Every incoming request consumes 1 token
- If the bucket has at least 1 token, the request is allowed
- If the bucket is empty, the request is rejected

### Why Token Bucket?

The token bucket algorithm allows short bursts of traffic while still enforcing an average rate over time.

This makes it more flexible than a strict fixed-window approach.

### Example

Suppose:

- Bucket capacity = 10
- Refill rate = 1 token/second

Then:

- A client can make up to 10 requests immediately if the bucket is full
- After that, tokens refill gradually at 1 per second
- If the client sends requests faster than refill happens, requests will start getting rejected

---

## Features

- FastAPI-based middleware integration
- Token Bucket rate limiting logic
- PostgreSQL-backed token storage
- Per-client request tracking using client IP
- Automatic token refill based on elapsed time
- Debug routes for testing bucket state
- Exclusion for docs and debug endpoints from rate limiting

---

## Tech Stack

- **Python**
- **FastAPI**
- **PostgreSQL**
- **SQLAlchemy**
- **Starlette Middleware**

---

## Project Structure

```bash
app/
│
├── core/
│   ├── config.py
│   └── database.py
│
├── models/
│   └── rate_limiter.py
│
├── services/
│   └── token_bucket.py
│
├── middleware/
│   └── rate_limiter.py
│
│── utils/
│   └── client.py
│
└── main.py