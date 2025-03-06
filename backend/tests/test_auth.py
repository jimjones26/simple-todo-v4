import pytest
from backend.app import login_manager
from backend.app.models import User
from backend.app import db
from flask_login import current_user

@pytest.fixture(autouse=True)
def setup_test_user(app):
    with app.app_context():
        test_user = User(username='testuser', email='test@example.com', role='user')
        test_user.set_password('password')
        db.session.add(test_user)
        db.session.commit()
        yield
        db.session.query(User).delete()
        db.session.commit()

def test_login_manager(app):
    with app.app_context():
        assert login_manager.login_view == 'auth.login'

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