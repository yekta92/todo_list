from uuid import UUID
import datetime
from test.models.test_model import TodoItem
from api.routers.todo_api import create_todos, get_todos, get_todo, update_todo


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
    response = get_todo(todo_id=UUID(int=0x12345678123456781234567812345678))
    assert isinstance(response.id, UUID)
    assert isinstance(response.completed, bool)
    assert all(hasattr(todo, "title") for todo in [response])
    assert all(isinstance(todo.title, str) for todo in [response])



def test_update_todo():
    response = update_todo(
    id=UUID(int=0x12345678123456781234567812345678),
    title = 'this is my task',
    description = 'important',
    completed = True,
    created_at=datetime.datetime.now()
)

    assert isinstance(response[0].id, UUID)
    assert isinstance(response[0].completed, bool)
    assert all(todo.completed in [True, False] for todo in response)

    assert all(hasattr(todo, "title") for todo in response)
    assert all(isinstance(todo.title, str) for todo in response)
    assert all(len(todo.title) > 0 for todo in response)

    ids = [todo.id for todo in response]
    assert len(ids) == len(set(ids))
