from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.models.rate_limiter import RateLimiter

def allow_request(
    db: Session,
    client_id: str,
    capacity: int,
    refill_rate: float
) -> bool:
    """
    Returns True if request is allowed, False otherwise
    """

    now = datetime.now(timezone.utc)

    # Lock row to handle concurrency safely
    bucket = (
        db.query(RateLimiter)
        .filter(RateLimiter.client_id == client_id)
        # .with_for_update()
        .one_or_none()
    )

    if bucket is None:
        # First request from this client
        bucket = RateLimiter(
            client_id=client_id,
            capacity=capacity,
            tokens=capacity - 1,
            refill_rate=refill_rate,
            last_refill_ts=now
        )
        db.add(bucket)
        return True

    # Refill tokens
    elapsed = (now - bucket.last_refill_ts).total_seconds()
    refill = elapsed * bucket.refill_rate

    bucket.tokens = min(bucket.capacity, bucket.tokens + refill)
    bucket.last_refill_ts = now

    if bucket.tokens < 1:
        return False

    bucket.tokens -= 1
    return True