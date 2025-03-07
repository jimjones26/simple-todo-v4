import pytest
from backend.app.models import User, Team, create_team, create_user
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

def test_add_users_to_team_api(client):
    """Test adding users to a team through API endpoint"""
    # Create admin user and login
    admin_data = {
        'username': 'teamadmin',
        'email': 'teamadmin@example.com',
        'password': 'adminpass',
        'role': 'admin'
    }
    client.post('/users', json=admin_data)
    login_response = client.post('/login', json={'username': 'teamadmin', 'password': 'adminpass'})
    assert login_response.status_code == 200

    # Create test team and users
    team = create_test_team(client)
    user_ids = []
    for i in range(3):
        user_data = {
            'username': f'teamuser{i}',
            'email': f'user{i}@team.test',
            'password': 'pass',
            'role': 'user'
        }
        response = client.post('/users', json=user_data)
        user_ids.append(response.json['id'])

    # Test valid user addition
    response = client.post(f'/teams/{team.id}/users', json={'user_ids': user_ids})
    assert response.status_code == 200
    assert response.json == {'message': f'Added {len(user_ids)} users to team'}

    # Verify database state
    with client.application.app_context():
        updated_team = Team.query.get(team.id)
        assert len(updated_team.users) == 3
        assert {user.id for user in updated_team.users} == set(user_ids)

    # Test invalid team ID
    response = client.post('/teams/9999/users', json={'user_ids': user_ids})
    assert response.status_code == 404

    # Test missing user IDs
    response = client.post(f'/teams/{team.id}/users', json={})
    assert response.status_code == 400

    # Test invalid user IDs
    response = client.post(f'/teams/{team.id}/users', json={'user_ids': [9999]})
    assert response.status_code == 404

def create_test_team(client):
    """Helper to create a test team in the database"""
    team_data = {
        'name': 'Test Team API',
        'description': 'Test team for API operations'
    }
    response = client.post('/teams', json=team_data)
    return Team.query.filter_by(name=team_data['name']).first()

def test_remove_users_from_team_api(client):
    """Integration test for removing users from a team via API"""
    with client.application.app_context():
        try:
            # Create test admin user (required for authentication)
            admin = create_user(username="admin_remove", email="admin_remove@test.com", password="adminpass", role="admin")

            # Create test team and users
            test_team = create_team(name="API Removal Test Team", description="Team for API removal test")
            user1 = create_user(username="remove_api_1", email="remove1@api.test", password="pass", role="user")
            user2 = create_user(username="remove_api_2", email="remove2@api.test", password="pass", role="user")
            user3 = create_user(username="keep_api_3", email="keep3@api.test", password="pass", role="user")
            test_team.add_users([user1, user2, user3])
            db.session.commit()
            team_id = test_team.id

            # Authenticate as admin and verify login success
            login_response = client.post('/login', json={
                'username': 'admin_remove',
                'password': 'adminpass'
            })
            assert login_response.status_code == 200, f"Login failed: {login_response.get_json()}"

            # Make API request to remove first two users
            response = client.delete(
                f'/teams/{team_id}/users',
                json={'user_ids': [user1.id, user2.id]}
            )

            # Verify response
            assert response.status_code == 200, f"Remove failed: {response.get_json()}"
            assert response.json['message'] == "Users removed successfully"

            # Verify database state
            updated_team = Team.query.get(team_id)
            assert len(updated_team.users) == 1
            remaining_usernames = {u.username for u in updated_team.users}
            assert 'keep_api_3' in remaining_usernames
            assert 'remove_api_1' not in remaining_usernames

        finally:
            # Cleanup database
            db.session.delete(test_team)
            db.session.delete(admin)
            db.session.delete(user1)
            db.session.delete(user2)
            db.session.delete(user3)
            db.session.commit()

def test_create_task_api(client):
    """Test task creation API"""
    # Create admin user and login
    admin_data = {
        'username': 'taskadmin',
        'email': 'taskadmin@example.com',
        'password': 'adminpass123',
        'role': 'admin'
    }
    create_response = client.post('/users', json=admin_data)
    assert create_response.status_code == 201

    login_response = client.post('/login', json={
        'username': 'taskadmin',
        'password': 'adminpass123'
    })
    assert login_response.status_code == 200

    # Create a team
    team_data = {
        'name': 'Task Team',
        'description': 'Team for task creation test'
    }
    team_response = client.post('/teams', json=team_data)
    assert team_response.status_code == 201
    team_id = team_response.json['id']

    # Test valid task creation
    task_data = {
        'title': 'Test Task API',
        'description': 'Task created via API',
        'team_id': team_id
    }
    response = client.post('/tasks', json=task_data)

    # Verify response
    assert response.status_code == 201
    json_data = response.get_json()
    assert 'id' in json_data
    assert json_data['title'] == task_data['title']
    assert json_data['description'] == task_data['description']
    assert json_data['team_id'] == task_data['team_id']

    # Check database persistence
    with client.application.app_context():
        from backend.app.models import Task
        created_task = Task.query.filter_by(title=task_data['title']).first()
        assert created_task is not None
        assert created_task.description == task_data['description']
        assert created_task.team_id == task_data['team_id']

    # Test invalid request (missing title)
    invalid_data = {
        'description': 'Invalid task data',
        'team_id': team_id
    }
    response = client.post('/tasks', json=invalid_data)
    assert response.status_code == 400
    assert 'message' in response.get_json()

    # Test invalid request (missing team_id)
    invalid_data = {
        'title': 'Invalid task data',
        'description': 'Invalid task data',
    }
    response = client.post('/tasks', json=invalid_data)
    assert response.status_code == 400
    assert 'message' in response.get_json()
