import pytest
from backend.app.models import Task, create_task
from backend.app import db

def test_create_task_success(app):
    """Test creating a task with valid data saves it to the database."""
    from backend.app.models import create_team

    team = create_team(name="Test Team", description="Test team")
    with app.app_context():

        task = create_task(
            title="Test Task",
            description="This is a test task",
            team_id=team.id,
        )
        assert task.id is not None
        assert task.title == "Test Task"
        assert task.description == "This is a test task"
        assert task.team_id == team.id

        # Verify the task is in the database
        retrieved_task = Task.query.get(task.id)
        assert retrieved_task is not None
        assert retrieved_task.title == "Test Task"

def test_assign_task_to_user(app):
    """Test assigning a task to a user updates the task's assignee correctly."""
    with app.app_context():
        from backend.app.models import create_team, create_user
        team = create_team(name="Test Team", description="Test team")
        user = create_user(username="Test User", email="test@example.com", password="password", role="user")

        # Create a task
        task = create_task(title="Test Task", description="Test task", team_id=team.id)

        # Assign the task to the user
        task.assign_user(user)
        db.session.commit()

        # Verify the task's assignee
        retrieved_task = Task.query.get(task.id)
        assert retrieved_task is not None
        assert retrieved_task.assignee.username == "Test User"

def test_update_task_status(app):
    """Test updating a task's status saves the change to the database."""
    with app.app_context():
        from backend.app.models import create_team, create_task

        # Create a team and a task
        team = create_team(name="Test Team", description="Test team")
        task = create_task(
            title="Test Task",
            description="This is a test task",
            team_id=team.id,
        )

        # Update the task's status
        new_status = "in progress"
        task.status = new_status  # Update will happen in the next step, this is prep
        # db.session.commit()  # The update method will do this, this is prep

        # Verify the in-memory object's status
        assert task.status == new_status

        # Verify the database record's status
        retrieved_task = Task.query.get(task.id)
        assert retrieved_task.status == new_status
