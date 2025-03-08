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
        retrieved_task = db.session.get(Task, task.id)
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
        retrieved_task = db.session.get(Task, task.id)
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

        # Update the task's status using the new method
        new_status = "in progress"
        task.update_status(new_status)  # Use the method we created

        # Verify the in-memory object's status
        assert task.status == new_status

        # Verify the database record's status
        retrieved_task = db.session.get(Task, task.id)
        assert retrieved_task.status == new_status

def test_update_task_deadline(app):
    """Test updating a task's deadline saves the change to the database."""
    with app.app_context():
        from backend.app.models import create_team, create_task, update_task_deadline
        from datetime import datetime
        import datetime as dt

        # Create a team and a task
        team = create_team(name="Test Team", description="Test team")
        task = create_task(
            title="Test Task",
            description="This is a test task",
            team_id=team.id,
        )

        # New deadline (1 week from now), avoiding deprecated utcnow()
        new_deadline = dt.datetime.now(dt.UTC).replace(tzinfo=None) + dt.timedelta(days=7)

        # Update the deadline using the function
        update_task_deadline(task.id, new_deadline)

        # Verify the database record's deadline
        retrieved_task = db.session.get(Task, task.id)
        assert retrieved_task.deadline == new_deadline