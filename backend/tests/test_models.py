import unittest
from backend.app import create_app
from backend.app import db
from backend.app.models import User, Team, Task  # Import the models
import pytest

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()

    yield app
    with app.app_context():
        db.session.remove()
        db.drop_all()

@pytest.fixture
def new_user():
    user = User(username='testuser', email='test@example.com')
    user.set_password('password')
    return user

@pytest.fixture
def new_task():
    task = Task(title='testtask', description='test description', status='not started')
    return task

class TestModels(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use an in-memory database for testing
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_user_model_exists(self):
        with self.app.app_context():
            self.assertTrue(hasattr(User, '__tablename__'))

    def test_team_model_exists(self):
        with self.app.app_context():
            self.assertTrue(hasattr(Team, '__tablename__'))

    def test_task_model_exists(self):
        with self.app.app_context():
            self.assertTrue(hasattr(Task, '__tablename__'))

def test_user_model(new_user):
    assert new_user.username == 'testuser'
    assert new_user.email == 'test@example.com'
    assert new_user.password_hash is not None

def test_user_team_association(app, new_user):
    with app.app_context():
        team = Team(name='testteam', description='test description')
        new_user.teams.append(team)
        db.session.add(new_user)
        db.session.add(team)
        db.session.commit()

        assert len(new_user.teams) == 1
        assert new_user.teams[0].name == 'testteam'

def test_task_model(app, new_task):
    with app.app_context():
        team = Team(name='testteam', description='test description')
        db.session.add(team)
        db.session.commit()

        new_task.team_id = team.id  # Assign the team_id
        db.session.add(new_task)
        db.session.commit()

        assert new_task.title == 'testtask'
        assert new_task.description == 'test description'
        assert new_task.status == 'not started'
        assert new_task.team_id == team.id
