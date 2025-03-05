import pytest
import json
from backend.app import create_app, db
from backend.app.models import User

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_create_user_api_success(client):
    data = {
        'username': 'api_test_user',
        'email': 'api_test@example.com',
        'password': 'password',
        'role': 'admin'
    }
    response = client.post('/users', json=data)
    assert response.status_code == 201

    with client.application.app_context():
        user = User.query.filter_by(username='api_test_user').first()
        assert user is not None
        assert user.email == 'api_test@example.com'

def test_create_user_api_invalid(client):
    data = {
        'username': '',
        'email': 'invalid-email',
        'password': '',
        'role': ''
    }
    response = client.post('/users', json=data)
    assert response.status_code == 400
