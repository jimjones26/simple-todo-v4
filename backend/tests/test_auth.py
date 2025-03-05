import pytest
from backend.app import create_app, login_manager
from backend.app.models import User
from backend.app import db  # Import db
from flask_login import LoginManager

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()
        # Create a test user
        test_user = User(username='testuser', email='test@example.com', role='user')
        test_user.set_password('password')
        db.session.add(test_user)
        db.session.commit()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_login_manager():
    app = create_app()
    #login_manager = LoginManager() #remove this line
    #login_manager.init_app(app)  # Remove this line

    with app.app_context():
        assert login_manager.login_view == 'login'

def test_authenticate_user_success(app):
    with app.app_context():
        from backend.app.views import authenticate_user
        user = authenticate_user('testuser', 'password')
        assert user is not None
        assert user.username == 'testuser'

def test_authenticate_user_failure(app):
    with app.app_context():
        from backend.app.views import authenticate_user
        user = authenticate_user('testuser', 'wrongpassword')
        assert user is None
