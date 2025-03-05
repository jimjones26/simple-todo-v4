import pytest
from backend.app import create_app
from backend.app.config import Config
from backend.app import db
from backend.app.models import User  # Import a model

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

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

@pytest.fixture()
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture()
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()


class TestMigrations:
    @pytest.fixture(autouse=True)
    def setup_db(self, app):
        self.app = app
        self.db = db
        with app.app_context():
            yield  # Let the test run


    def test_tables_exist(self):
        with self.app.app_context():
            user_count = User.query.count()
            assert user_count >= 0
