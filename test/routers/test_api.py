from uuid import UUID
import datetime
from test.models.test_model import TodoItem
from fastapi.testclient import TestClient
from main import app  

client = TestClient(app)

sample_id = UUID(int=0x12345678123456781234567812345678)


def test_create_todos():
    response = client.post(TodoItem(id=sample_id,title= "Test Todo",completed= False,))
   
    assert response.title == "Test Todo"
    assert response.description == "Test description"
    assert response.status == 'pending'
    assert type(response.created_at) is datetime.datetime
    print("create_todos passed")


def test_get_todos():
    response = client.get(f"/create/{sample_id}")

    assert isinstance(response[0].id, UUID)
    assert isinstance(response[0].completed, bool)
    assert all(len(todo.title) > 0 for todo in response)
    assert all(hasattr(todo, "title") for todo in response)
    assert all(isinstance(todo.title, str) for todo in response)


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




import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from utils.database import Base, get_db
from main import app
from api.models import todo_model

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_todos.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def test_db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="module")
def client(test_db):
    def override_get_db():
        try:
            yield test_db
        finally:
            pass
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c

# def test_create_todo(client):
#     response = client.post("/todos/", json={"title": "Test Todo", "description": "Test description"})
#     assert response.status_code == 200
#     data = response.json()
#     assert data["title"] == "Test Todo"
#     assert data["status"] == "pending"

# def test_get_todos(client):
#     response = client.get("/todos/")
#     assert response.status_code == 200
#     assert isinstance(response.json(), list)

# def test_update_todo_partial(client):
#     # Create first
#     response = client.post("/todos/", json={"title": "Update Test"})
#     todo_id = response.json()["id"]
#     # Partial update
#     response = client.patch(f"/todos/{todo_id}", json={"status": "completed"})
#     assert response.status_code == 200
#     assert response.json()["status"] == "completed"

# def test_get_todo_stats(client):
#     response = client.get("/todos/stats")
#     assert response.status_code == 200
#     stats = response.json()
#     assert isinstance(stats, dict)
