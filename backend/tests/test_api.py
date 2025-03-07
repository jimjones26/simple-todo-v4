import pytest
from backend.app.models import User, Team
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

def test_logout_api(client):
    """Test logout API"""
    # First, log in
    login_data = {
        'username': 'testuser',
        'password': 'password'
    }
    login_response = client.post('/login', json=login_data)
    assert login_response.status_code == 200

    # Then, log out
    logout_response = client.get('/logout')
    assert logout_response.status_code == 200
    assert logout_response.json == {'message': 'Logged out successfully'}

    # Verify that the user is no longer authenticated
    auth_status_response = client.get('/auth/status')
    assert auth_status_response.status_code == 401

def test_create_team_api(client):
    """Test team creation via API creates team in database"""
    # Create admin user through existing API
    admin_data = {
        'username': 'teamadmin',
        'email': 'teamadmin@example.com',
        'password': 'adminpass123',
        'role': 'admin'
    }
    create_response = client.post('/users', json=admin_data)
    assert create_response.status_code == 201

    # Login as admin
    login_response = client.post('/login', json={
        'username': 'teamadmin',
        'password': 'adminpass123'
    })
    assert login_response.status_code == 200

    # Test valid team creation
    team_data = {
        'name': 'Development Team',
        'description': 'Software development team'
    }
    response = client.post('/teams', json=team_data)
    
    # Verify response
    assert response.status_code == 201
    json_data = response.get_json()
    assert 'id' in json_data
    assert json_data['name'] == team_data['name']
    assert json_data['description'] == team_data['description']

    # Check database persistence
    with client.application.app_context():
        created_team = Team.query.filter_by(name=team_data['name']).first()
        assert created_team is not None
        assert created_team.description == team_data['description']

    # Test invalid request (missing name)
    invalid_data = {'description': 'Invalid team data'}
    response = client.post('/teams', json=invalid_data)
    assert response.status_code == 400
    assert 'message' in response.get_json()
