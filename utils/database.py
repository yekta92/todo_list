"""
SQL Database Configurations
"""

from sqlmodel import Session, SQLModel, create_engine


# SQLite database URL and engine setup
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url)


# Create the database tables
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


# Dependency to get DB session
def get_session():
    with Session(engine) as session:
        yield session
