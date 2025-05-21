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
    assert response.completed is False
    assert isinstance(response.id, UUID)
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
