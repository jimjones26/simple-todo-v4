import pytest
from backend.app.models import Task, create_task, create_user, create_team
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

def test_get_user_tasks(app):
    """Test fetching tasks assigned to a specific user."""
    with app.app_context():
        # Create a team
        team = create_team(name="Test Team", description="Test team")

        # Create a user
        user1 = create_user(username="Test User 1", email="test1@example.com", password="password", role="user")
        user2 = create_user(username="Test User 2", email="test2@example.com", password="password", role="user")

        # Create tasks assigned to the user
        task1 = create_task(title="Task 1", description="Task 1 for Test User 1", team_id=team.id)
        task2 = create_task(title="Task 2", description="Task 2 for Test User 1", team_id=team.id)
        task3 = create_task(title="Task 3", description="Task 3 for Test User 2", team_id=team.id)

        task1.assign_user(user1)
        task2.assign_user(user1)
        task3.assign_user(user2)

        db.session.commit()

        # Fetch tasks for user1 (This part will fail until get_user_tasks is implemented)
        from backend.app.models import get_user_tasks  # Import when needed
        user1_tasks = get_user_tasks(user1.id)

        # Assert that the correct tasks are returned
        assert len(user1_tasks) == 2
        assert task1 in user1_tasks
        assert task2 in user1_tasks
        assert task3 not in user1_tasks

        # Fetch tasks for user2
        user2_tasks = get_user_tasks(user2.id)
        assert len(user2_tasks) == 1
        assert task3 in user2_tasks

def test_fetch_team_tasks(app):
    """Test fetching tasks for a specific team."""
    with app.app_context():
        # Create a team
        team1 = create_team(name="Team 1", description="Test Team 1")
        team2 = create_team(name="Team 2", description="Test Team 2")

        # Create tasks for team 1
        task1 = create_task(title="Task 1", description="Task 1 for Team 1", team_id=team1.id)
        task2 = create_task(title="Task 2", description="Task 2 for Team 1", team_id=team1.id)

        # Create a task for team 2
        task3 = create_task(title="Task 3", description="Task 3 for Team 2", team_id=team2.id)

        # Fetch tasks for team 1 (This will fail until fetch_team_tasks is implemented)
        from backend.app.models import fetch_team_tasks  # Import when needed
        team1_tasks = fetch_team_tasks(team1.id)

        # Assert that the correct tasks are returned for team 1
        assert len(team1_tasks) == 2
        assert task1 in team1_tasks
        assert task2 in team1_tasks
        assert task3 not in team1_tasks

        # Fetch tasks for team 2
        team2_tasks = fetch_team_tasks(team2.id)
        assert len(team2_tasks) == 1
        assert task3 in team2_tasks

        # Test case: Team not found (should return empty list)
        team_not_found_tasks = fetch_team_tasks(9999)
        assert len(team_not_found_tasks) == 0
