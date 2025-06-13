import pytest
from uuid import UUID
from uuid import uuid4
import datetime
from fastapi.testclient import TestClient
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, Session, create_engine, select

from main import app  
from api.models.todo_model import TodoItem
from test.models.test_model import TodoItem

client = TestClient(app)


sample_id = str(uuid4())



SQLALCHEMY_DATABASE_URL = "sqlite:///./todos.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def test_engine():
    engine = create_engine("sqlite:///:memory:", echo=True)
    SQLModel.metadata.create_all(engine)
    return engine

@pytest.fixture
def session(test_engine: Engine):
    with Session(test_engine) as session:
        yield session

def test_create_and_read_todo(session: Session):
    # Create a new Todo
    todo = TodoItem(title="Write tests", completed=False)
    session.add(todo)
    session.commit()
    session.refresh(todo)

    # Query the Todo
    statement = select(TodoItem).where(TodoItem.id == todo.id)
    result = session.exec(statement).first()

    assert result is not None
    assert result.title == "Write tests"
    assert result.completed is False



def test_create_todos():
    response = client.post(TodoItem(id=sample_id,title= "Test Todo",completed= False,))
   
    assert response.title == "Test Todo"
    assert response.description == "Test description"
    assert response.status == 'pending'
    assert type(response.created_at) is datetime.datetime
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Todo"
    assert data["status"] == "pending"
    print("create_todos passed")



def test_get_todos():
    response = client.get(f"/create/{sample_id}")

    assert isinstance(response[0].id, UUID)
    assert isinstance(response[0].completed, bool)
    assert all(len(todo.title) > 0 for todo in response)
    assert all(hasattr(todo, "title") for todo in response)
    assert all(isinstance(todo.title, str) for todo in response)
    assert response.status_code == 200


def test_get_todo():
    response = client.get(f"/todos/{sample_id}")
    
    assert isinstance(response.id, UUID)
    assert isinstance(response.completed, bool)
    assert all(hasattr(todo, "title") for todo in [response])
    assert all(isinstance(todo.title, str) for todo in [response])


def test_update_todo():
    response = client.put(f"/todos/{sample_id}",TodoItem(
                                                        id=sample_id,
                                                        title= "this is my task",
                                                        completed= True
                                                    )
                                                )
  
    assert isinstance(response.id, UUID)
    assert isinstance(response.completed, bool)


def test_delete_todo():
    response = client.post(f"/todos/{sample_id}")

    assert response == {"message": "Todo item deleted successfully"}

def test_get_todo_stats(client):
    response = client.get("/todos/stats")
    assert response.status_code == 200
    stats = response.json()
    assert isinstance(stats, dict)

