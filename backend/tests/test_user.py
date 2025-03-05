import pytest
from backend.app.models import User, create_user
from backend.app import db, create_app

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use an in-memory database for testing
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_create_user_success(app):
    with app.app_context():
        username = 'testuser'
        email = 'test@example.com'
        password = 'password'
        role = 'admin'

        user = create_user(username=username, email=email, password=password, role=role)

        # Query the database to confirm the user is saved
        retrieved_user = User.query.filter_by(username=username).first()

        assert retrieved_user is not None
        assert retrieved_user.username == username
        assert retrieved_user.email == email
        assert retrieved_user.role == role
        assert retrieved_user.check_password(password)
