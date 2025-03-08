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

def test_assign_task_to_user(app):
    """Test assigning a task to a user updates the task's assignee correctly."""
    with app.app_context():
        # Create a team and a user
        from backend.app.models import create_team, create_user
        team = create_team(name="Test Team", description="Test team")
        user = create_user(username="Test User", email="test@example.com", password="password", role="user")

        # Create a task
        task = create_task(title="Test Task", description="Test task", team_id=team.id)

        # Assign the task to the user
        task.assignee_id = user.id
        db.session.commit()

        # Verify the task's assignee
        retrieved_task = Task.query.get(task.id)
        assert retrieved_task is not None
        assert retrieved_task.assignee_id == user.id
        assert retrieved_task.assignee.username == "Test User"
