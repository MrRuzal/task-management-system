import pytest
from dataclasses import dataclass
from datetime import date
from app.main import app
from app.entrypoints.api.dependencies import get_current_user
from app.container import Container


@dataclass
class MockTask:
    id: int
    title: str
    description: str
    due_date: str
    user_id: int


class TestTaskService:
    def __init__(self):
        self.tasks = {}
        self.next_id = 1

    async def create_task(self, task_create, user_id):
        task = MockTask(
            id=self.next_id,
            title=task_create.title,
            description=task_create.description,
            due_date=task_create.due_date,
            user_id=user_id,
        )
        self.tasks[self.next_id] = task
        self.next_id += 1
        return task

    async def get_all_tasks(self):
        return list(self.tasks.values())

    async def get_all_tasks_by_user_id(self, user_id):
        return [
            task for task in self.tasks.values() if task.user_id == user_id
        ]

    async def get_task_by_id(self, task_id):
        return self.tasks.get(task_id)

    async def update_task(self, task_update, task_id, user_id):
        task = self.tasks.get(task_id)
        if task and task.user_id == user_id:
            task.title = task_update.title
            task.description = task_update.description
            task.due_date = task_update.due_date
            self.tasks[task_id] = task
            return task
        return None

    async def delete_task(self, task_id):
        if task_id in self.tasks:
            del self.tasks[task_id]


class TestUser:
    id = 1
    username = "taskuser"
    email = "taskuser@example.com"
    is_active = True


@pytest.fixture
def override_dependencies():
    Container.task_service.override(TestTaskService())
    app.dependency_overrides[get_current_user] = lambda: TestUser()
    yield
    Container.task_service.reset_override()
    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_create_task(async_client, override_dependencies):
    task_data = {
        "title": "Test Task",
        "description": "Test Description",
        "due_date": date.today().isoformat(),
    }
    response = await async_client.post("/tasks/", json=task_data)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == task_data["title"]
    assert data["description"] == task_data["description"]
    assert data["user_id"] == 1


@pytest.mark.asyncio
async def test_get_all_tasks(async_client, override_dependencies):
    task_data = {
        "title": "Test Task",
        "description": "Test Description",
        "due_date": date.today().isoformat(),
    }
    await async_client.post("/tasks/", json=task_data)

    response = await async_client.get("/tasks/")
    assert response.status_code == 200
    tasks = response.json()
    assert isinstance(tasks, list)
    assert len(tasks) == 1
    assert tasks[0]["title"] == "Test Task"


@pytest.mark.asyncio
async def test_get_tasks_by_user(async_client, override_dependencies):
    task_data = {
        "title": "User Task",
        "description": "Test Description",
        "due_date": date.today().isoformat(),
    }
    await async_client.post("/tasks/", json=task_data)

    response = await async_client.get("/tasks/user")
    assert response.status_code == 200
    tasks = response.json()
    assert isinstance(tasks, list)
    assert len(tasks) == 1
    assert tasks[0]["user_id"] == TestUser.id
    assert tasks[0]["title"] == task_data["title"]


@pytest.mark.asyncio
async def test_get_task_by_id(async_client, override_dependencies):
    task_data = {
        "title": "Single Task",
        "description": "Test Description",
        "due_date": date.today().isoformat(),
    }
    response_create = await async_client.post("/tasks/", json=task_data)
    task_id = response_create.json()["id"]

    response = await async_client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    task = response.json()
    assert task["id"] == task_id
    assert task["title"] == task_data["title"]
    assert task["description"] == task_data["description"]


@pytest.mark.asyncio
async def test_update_task(async_client, override_dependencies):
    task_data = {
        "title": "Original Task",
        "description": "Original Test Test Description",
        "due_date": date.today().isoformat(),
    }
    response_create = await async_client.post("/tasks/", json=task_data)
    task_id = response_create.json()["id"]

    update_data = {
        "title": "Updated Task",
        "description": "Updated Test Test Description",
        "due_date": date.today().isoformat(),
    }

    response_update = await async_client.put(
        f"/tasks/{task_id}", json=update_data
    )
    assert response_update.status_code == 200
    updated_task = response_update.json()
    assert updated_task["title"] == update_data["title"]
    assert updated_task["description"] == update_data["description"]


@pytest.mark.asyncio
async def test_delete_task(async_client, override_dependencies):
    task_data = {
        "title": "Task to delete",
        "description": "Delete Test Description",
        "due_date": date.today().isoformat(),
    }
    response_create = await async_client.post("/tasks/", json=task_data)
    task_id = response_create.json()["id"]

    response_delete = await async_client.delete(f"/tasks/{task_id}")
    assert response_delete.status_code == 204

    response_get = await async_client.get(f"/tasks/{task_id}")
    assert response_get.status_code == 404
