"""
SQL Database Configurations
"""

from sqlmodel import SQLModel, create_engine,Session


# Database URL for SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./todos.db"

# Create the SQLAlchemy engine with echo=True for SQL output
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True, connect_args={"check_same_thread": False})

def create_db_and_tables():
    SQLModel.metadata.create_all(bind=engine)
    print("Database and tables created successfully.")

def get_session():
    with Session(engine) as session:
        print("get session successfully.")
        yield session

def test_connection():
    try:
        with engine.connect() as connection:
            print("Connection to database established successfully.")
    except Exception as e:
        print(f"Failed to connect to the database: {e}")



if __name__ == "__main__":
    test_connection()
    create_db_and_tables()
    get_session()

