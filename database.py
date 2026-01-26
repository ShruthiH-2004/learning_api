from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLite database URL
DATABASE_URL = "sqlite:///./users.db"

# Create engine (connects to DB)
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

# Session to talk to DB
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()
