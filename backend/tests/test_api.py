import pytest
from backend.app.models import User
from backend.app import db

@pytest.fixture(autouse=True)
def setup_test_user(app):
    """Create a test user for API tests"""
    with app.app_context():
        test_user = User(username='testuser', email='test@example.com', role='user')
        test_user.set_password('password')
        db.session.add(test_user)
        db.session.commit()
        yield
        db.session.query(User).delete()
        db.session.commit()

def test_login_api_success(client):
    """Test successful login API"""
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
    """Test failed login attempt"""
    data = {
        'username': 'testuser',
        'password': 'wrongpassword'
    }
    response = client.post('/login', json=data)
    assert response.status_code == 401
    assert response.json == {'message': 'Invalid credentials'}

def test_create_user_api(client):
    """Test user creation API"""
    data = {
        'username': 'newuser',
        'email': 'newuser@example.com',
        'password': 'newpassword',
        'role': 'user'
    }
    response = client.post('/users', json=data)
    assert response.status_code == 201
    assert 'id' in response.json
    assert response.json['username'] == 'newuser'
    assert response.json['role'] == 'user'

def test_get_current_user(client):
    """Test getting current user info"""
    # First login
    login_data = {
        'username': 'testuser',
        'password': 'password'
    }
    login_response = client.post('/login', json=login_data)
    assert login_response.status_code == 200  # Verify login succeeded
    
    # Then get user info using the correct endpoint
    response = client.get('/auth/status')
    assert response.status_code == 200
    assert response.json['username'] == 'testuser'