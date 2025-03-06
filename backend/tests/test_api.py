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
        # Create a test user for login tests
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

def test_create_user_api_success(client, app):
    data = {
        'username': 'api_test_user',
        'email': 'api_test@example.com',
        'password': 'password',
        'role': 'admin'
    }
    response = client.post('/users', json=data)
    assert response.status_code == 201

    with app.app_context():
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

def test_login_api_success(client):
    data = {
        'username': 'testuser',
        'password': 'password'
    }
    response = client.post('/login', json=data)
    assert response.status_code == 200
    assert 'id' in response.json
    assert 'username' in response.json
    assert 'email' in response.json
    assert 'role' in response.json
    assert response.json['username'] == 'testuser'

def test_login_api_failure(client):
    data = {
        'username': 'testuser',
        'password': 'wrongpassword'
    }
    response = client.post('/login', json=data)
    assert response.status_code == 401
    assert response.json == {'message': 'Invalid credentials'}
