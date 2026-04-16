from fastapi import FastAPI

from app.core.database import SessionLocal
from app.models.rate_limiter import RateLimiter
from datetime import datetime, timezone

from app.middleware.rate_limiter import RateLimiterMiddleware

app = FastAPI(title="Rate Limiter Service")

# Middleware (REAL LOGIC)
app.add_middleware(RateLimiterMiddleware)

# Actual test endpoint (goes through middleware)
@app.get("/test")
def test():
    return {"message": "Request allowed"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/debug/create_bucket")
def create_bucket():
    db = SessionLocal()
    bucket = RateLimiter(
       client_id="test_client",
       capacity=10,
       tokens=10,
       refill_rate=1,
       last_refill_ts=datetime.now(timezone.utc)
    )
    db.merge(bucket)
    db.commit()
    db.close()
    return {"status": "created"}

@app.get("/debug/bucket/{client_id}")
def get_bucket(client_id: str):
    db = SessionLocal()
    try:
        bucket = db.query(RateLimiter).filter(RateLimiter.client_id == client_id).first()

        if not bucket:
            return {"message": "Bucket not found"}

        return {
            "client_id": bucket.client_id,
            "capacity": bucket.capacity,
            "tokens": bucket.tokens,
            "refill_rate": bucket.refill_rate,
            "last_refill_ts": bucket.last_refill_ts,
            "updated_at": bucket.updated_at
        }
    finally:
        db.close()
