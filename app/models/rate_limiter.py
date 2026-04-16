from sqlalchemy import Column, String, Integer, Float, DateTime
from datetime import datetime, timezone
from app.core.database import Base

class RateLimiter(Base):
    __tablename__ = "rate_limiters"

    client_id = Column(String(100), primary_key=True, index=True)

    capacity = Column(Integer, nullable=False)
    tokens = Column(Float, nullable=False)

    refill_rate = Column(Float, nullable=False)

    # IMPORTANT: timezone-aware
    last_refill_ts = Column(
        DateTime(timezone=True),
        nullable=False
    )

    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )
