import pytest
from backend.app.models import User, Team, Task

@pytest.fixture
def new_task():
    task = Task(title='testtask', description='test description', status='not started')
    return task

class TestModels:
    def test_user_model_exists(self, app):
        with app.app_context():
            assert hasattr(User, '__tablename__')

    def test_team_model_exists(self, app):
        with app.app_context():
            assert hasattr(Team, '__tablename__')

    def test_task_model_exists(self, app):
        with app.app_context():
            assert hasattr(Task, '__tablename__')

    def test_new_user(self, new_user):
        assert new_user.username == 'testuser'
        assert new_user.email == 'test@example.com'
        assert new_user.check_password('password')

    def test_new_task(self, new_task):
        assert new_task.title == 'testtask'
        assert new_task.description == 'test description'
        assert new_task.status == 'not started'