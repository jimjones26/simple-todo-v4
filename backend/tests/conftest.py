import pytest
from backend.app import create_app, db
from backend.tests.config import TestConfig
from backend.app.models import User

@pytest.fixture(scope='session')
def app():
    """Create and configure a new app instance for each test session."""
    app = create_app()
    app.config.from_object(TestConfig)
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()

@pytest.fixture
def new_user():
    """Create a test user instance."""
    user = User(username='testuser', email='test@example.com')
    user.set_password('password')
    return user