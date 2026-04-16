from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from fastapi.responses import JSONResponse
from app.core.database import SessionLocal
from app.services.token_bucket import allow_request
from app.core.config import RATE_LIMIT_CAPACITY, RATE_LIMIT_REFILL_RATE
from app.utils.client import get_client_id

EXCLUDED_PATHS = {"/docs", "/openapi.json", "/redoc"}

class RateLimiterMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):

        # Skip rate limiting for certain routes
        if request.url.path in EXCLUDED_PATHS or request.url.path.startswith("/debug"):
            return await call_next(request)

        db = SessionLocal()

        try:
            #identify client 
            client_id = get_client_id(request)

            #apply rate limiting logic
            allowed = allow_request(
                db=db,
                client_id=client_id,
                capacity=RATE_LIMIT_CAPACITY,
                refill_rate=RATE_LIMIT_REFILL_RATE
            )

            if not allowed:
                db.rollback()  # important because we might have updated the bucket state
                return JSONResponse(
                    status_code=429,
                    content={"detail": "Rate limit exceeded"}
                )

            response = await call_next(request)
            db.commit()
            return response

        except Exception:
            db.rollback()
            raise

        finally:
            db.close()