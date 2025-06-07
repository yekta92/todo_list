"""
SQL Database Configurations
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlmodel import SQLModel, Field
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager

SQLALCHEMY_DATABASE_URL = "sqlite:///./todos.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency function for FastAPI to get DB session
def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create the database tables
def create_db_and_tables():
    SQLModel.metadata.create_all(bind=engine)

