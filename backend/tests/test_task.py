import pytest
from backend.app.models import Task, create_task
from backend.app import db

def test_create_task_success(app):
    """Test creating a task with valid data saves it to the database."""
    with app.app_context():
        team_id = 1  # Replace with a valid team ID in your test database
        task = create_task(
            title="Test Task",
            description="This is a test task",
            team_id=team_id,
        )
        assert task.id is not None
        assert task.title == "Test Task"
        assert task.description == "This is a test task"
        assert task.team_id == team_id

        # Verify the task is in the database
        retrieved_task = Task.query.get(task.id)
        assert retrieved_task is not None
        assert retrieved_task.title == "Test Task"
