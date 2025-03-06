import pytest
from backend.app.models import User, create_user
from backend.app import db

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