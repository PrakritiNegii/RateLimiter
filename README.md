# Rate Limiter

A backend rate limiting service built using **FastAPI** and **PostgreSQL** by applying the **Token Bucket Algorithm**.

This project was created to understand how rate limiting works in real backend systems, how middleware can intercept requests, and how token refill logic can be implemented using database-backed state.

## Versions
- V1: PostgreSQL-based rate limiter (current main branch)
- V2: Redis-based rate limiter (v2-redis branch)

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

### Architecture Flow

```mermaid
flowchart TD
    A[Client Request] --> B[RateLimiterMiddleware]
    B --> C{Excluded Path?}
    C -->|Yes| D[Forward Request]
    C -->|No| E[Identify Client by IP]
    E --> F[Fetch Bucket from PostgreSQL]
    F --> G[Refill Tokens Based on Time Elapsed]
    G --> H{Token Available?}
    H -->|Yes| I[Consume 1 Token]
    I --> J[Allow Request]
    H -->|No| K[Return 429 Too Many Requests]
 ```

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
```

---
# How to run 
git clone https://github.com/PrakritiNegii/RateLimiter

### create virtual environment
python -m venv venv

### activate it (Windows)
venv\Scripts\activate

### install dependencies
pip install -r requirements.txt

### run server
uvicorn app.main:app --reload

### Open in browser:
http://127.0.0.1:8000/docs