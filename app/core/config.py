import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

RATE_LIMIT_CAPACITY = int(os.getenv("RATE_LIMIT_CAPACITY", 10))
RATE_LIMIT_REFILL_RATE = float(os.getenv("RATE_LIMIT_REFILL_RATE", 1))

