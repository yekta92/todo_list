from uuid import UUID
import datetime
from test.models.test_model import TodoItem
from api.routers.todo_api import (
    create_todos,
    get_todos,
    get_todo,
    update_todo,
    delete_todo,
)

sample_id = UUID(int=0x12345678123456781234567812345678)


def test_create_todos():
    response = create_todos(
        title="Test Todo",
        description="Test description",
        completed=False,
    )
    assert response.title == "Test Todo"
    assert response.description == "Test description"
    assert response.completed is False
    assert isinstance(response.id, UUID)
    assert type(response.created_at) is datetime.datetime
    print("create_todos passed")


def test_get_todos():
    response = get_todos()
    assert isinstance(response[0].id, UUID)
    assert isinstance(response[0].completed, bool)
    assert all(len(todo.title) > 0 for todo in response)
    assert all(hasattr(todo, "title") for todo in response)
    assert all(isinstance(todo.title, str) for todo in response)


def test_get_todo():
    response = get_todo(todo_id=sample_id)
    assert isinstance(response.id, UUID)
    assert isinstance(response.completed, bool)
    assert all(hasattr(todo, "title") for todo in [response])
    assert all(isinstance(todo.title, str) for todo in [response])


def test_update_todo():
    response = update_todo(
        todo_update=TodoItem(
            id=sample_id,
            title="this is my task",
            completed=True,
        )
    )
    assert isinstance(response.id, UUID)
    assert isinstance(response.completed, bool)


def test_delete_todo():
    response = delete_todo(id=sample_id)

    assert response == {"message": "Todo item deleted successfully"}
