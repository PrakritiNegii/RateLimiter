from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import DATABASE_URL

'''create_engine, sessionmaker, declarative_base are factory/helper functions
   (functions that create important objects) and return configured objects 
   that are used later.'''

# Engine = central connection manager for the database
engine = create_engine(DATABASE_URL)

# Session factory — creates DB sessions for each request
SessionLocal = sessionmaker(bind=engine)

# Base class for all ORM models (tables will inherit from this)
Base = declarative_base()
