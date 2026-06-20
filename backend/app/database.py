from sqlalchemy import create_engine, String, TypeDecorator, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from .config import settings
import uuid

# Check if using SQLite
is_sqlite = settings.DATABASE_URL.startswith("sqlite")

# Create SQLAlchemy engine
engine = create_engine(
    settings.DATABASE_URL,
    poolclass=NullPool,
    echo=settings.DEBUG,
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for models
Base = declarative_base()


# Custom UUID type that works with both PostgreSQL and SQLite
if is_sqlite:
    # For SQLite, use String and handle UUID conversion
    UUID = String(36)
    # For SQLite, use JSON instead of ARRAY
    ARRAY = JSON
else:
    # For PostgreSQL, use native UUID type
    from sqlalchemy.dialects.postgresql import UUID, ARRAY


# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
