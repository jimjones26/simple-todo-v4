from flask import request, jsonify, Blueprint
from datetime import datetime
from dateutil import parser
from backend.app import db
from backend.app.models import User, create_user, create_team, Team  # Import from models.py
from sqlalchemy.exc import IntegrityError
from flask_login import login_user, logout_user, login_required, current_user

bp = Blueprint('auth', __name__)

def authenticate_user(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return user
    return None

@bp.route('/users', methods=['POST'])
def create_user_route():
    data = request.get_json()

    if not data:
        return jsonify({'message': 'No data provided'}), 400

    required_fields = ['username', 'email', 'password', 'role']
    for field in required_fields:
        if field not in data:
            return jsonify({'message': f'Missing field: {field}'}), 400

    username = data['username']
    email = data['email']
    password = data['password']
    role = data['role']

    try:
        user = create_user(username=username, email=email, password=password, role=role)
        return jsonify({'id': user.id, 'username': user.username, 'role': user.role}), 201
    except ValueError as e:
        return jsonify({'message': str(e)}), 400
    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'User with this username or email already exists.'}), 409

@bp.route('/login', methods=['POST'])
def login():
    if current_user.is_authenticated:
        return jsonify(current_user.get_dict()), 200
    
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No data provided'}), 400
    
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400

    user = authenticate_user(username, password)
    if user:
        login_user(user, remember=True)
        return jsonify(user.get_dict()), 200
    return jsonify({'message': 'Invalid credentials'}), 401

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully'}), 200

@bp.route('/protected')
@login_required
def protected():
    return jsonify({
        'id': current_user.id,
        'username': current_user.username,
        'email': current_user.email,
        'role': current_user.role,
    })

@bp.route('/teams', methods=['POST'])
@login_required
def create_team_route():
    # Verify admin permissions
    if current_user.role != 'admin':
        return jsonify({'message': 'Admin access required'}), 403
    
    data = request.get_json()
    
    # Validate request data
    if not data or 'name' not in data:
        return jsonify({'message': 'Team name is required'}), 400
    
    # Extract parameters
    name = data.get('name')
    description = data.get('description', None)
    
    try:
        # Create team using model function
        team = create_team(name=name, description=description)
        return jsonify({
            'id': team.id,
            'name': team.name,
            'description': team.description
        }), 201
    except ValueError as e:
        return jsonify({'message': str(e)}), 400
    except Exception as e:
        return jsonify({'message': 'Server error creating team'}), 500

@bp.route('/auth/status')
def auth_status():
    if current_user.is_authenticated:
        return jsonify(current_user.get_dict()), 200
    return jsonify({'message': 'Not authenticated'}), 401

@bp.route('/teams/<int:team_id>/users', methods=['POST'])
@login_required
def add_users_to_team(team_id):
    """Add users to a team (admin only)"""
    # Verify admin permissions
    if current_user.role != 'admin':
        return jsonify({'message': 'Admin access required'}), 403
    
    # Find target team
    team = db.session.get(Team, team_id)
    if not team:
        return jsonify({'message': 'Team not found'}), 404

    # Validate request data
    data = request.get_json()
    if not data or 'user_ids' not in data:
        return jsonify({'message': 'User IDs are required'}), 400
    
    user_ids = data['user_ids']
    if not isinstance(user_ids, list):
        return jsonify({'message': 'User IDs must be a list'}), 400

    # Verify all users exist
    users = User.query.filter(User.id.in_(user_ids)).all()
    if len(users) != len(user_ids):
        existing_ids = {user.id for user in users}
        missing_ids = [uid for uid in user_ids if uid not in existing_ids]
        return jsonify({'message': f'Users not found: {missing_ids}'}), 404

    # Add users to team
    try:
        team.add_users(users)
        db.session.commit()
        return jsonify({'message': f'Added {len(users)} users to team'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Server error adding users to team'}), 500

@bp.route('/teams', methods=['GET'])
@login_required
def get_teams():
    """Get all teams (admin only)"""
    if current_user.role != 'admin':
        return jsonify({'message': 'Admin access required'}), 403
    
    teams = Team.query.all()
    teams_data = [{
        'id': team.id,
        'name': team.name,
        'description': team.description
    } for team in teams]
    
    return jsonify(teams_data), 200

@bp.route('/users', methods=['GET'])
@login_required
def get_users():
    """Get all users (admin only)"""
    if current_user.role != 'admin':
        return jsonify({'message': 'Admin access required'}), 403
    
    users = User.query.all()
    users_data = [{
        'id': user.id,
        'username': user.username,
        'role': user.role
    } for user in users]
    
    return jsonify(users_data), 200

@bp.route('/teams/<int:team_id>/users', methods=['DELETE'])
@login_required
def remove_users_from_team(team_id):
    """Remove users from a team (admin only)"""
    # Verify admin permissions
    if current_user.role != 'admin':
        return jsonify({'message': 'Admin access required'}), 403

    # Find target team
    team = db.session.get(Team, team_id)
    if not team:
        return jsonify({'message': 'Team not found'}), 404

    # Validate request data
    data = request.get_json()
    if not data or 'user_ids' not in data:
        return jsonify({'message': 'User IDs are required'}), 400
    
    user_ids = data['user_ids']
    if not isinstance(user_ids, list):
        return jsonify({'message': 'User IDs must be a list'}), 400

    # Execute removal
    try:
        from backend.app.models import remove_users_from_team
        remove_users_from_team(team_id=team_id, user_ids=user_ids)
        return jsonify({'message': 'Users removed successfully'}), 200
    except ValueError as e:
        return jsonify({'message': str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Server error removing users from team'}), 500

@bp.route('/tasks', methods=['POST'])
@login_required
def create_task_route():
    """Creates a new task."""
    # Verify admin permissions - only admins can create tasks
    if current_user.role != 'admin':
        return jsonify({'message': 'Admin access required'}), 403

    data = request.get_json()

    if not data:
        return jsonify({'message': 'No data provided'}), 400

    required_fields = ['title', 'team_id']
    for field in required_fields:
        if field not in data:
            return jsonify({'message': f'Missing field: {field}'}), 400

    title = data['title']
    description = data.get('description', '')  # Description is optional
    team_id = data['team_id']

    try:
        from backend.app.models import create_task  # Import here to avoid circular import
        task = create_task(title=title, description=description, team_id=team_id)
        return jsonify({
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'team_id': task.team_id
        }), 201
    except ValueError as e:
        return jsonify({'message': str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Server error creating task'}), 500

@bp.route('/tasks/<int:task_id>/assign', methods=['PATCH'])
@login_required
def assign_user_to_task(task_id):
    """Assigns a user to a task."""
    # Verify admin permissions - only admins can assign tasks
    if current_user.role != 'admin':
        return jsonify({'message': 'Admin access required'}), 403

    data = request.get_json()

    if not data or 'user_id' not in data:
        return jsonify({'message': 'User ID is required'}), 400

    user_id = data['user_id']

    try:
        from backend.app.models import Task, User  # Import here to avoid circular import
        task = db.session.get(Task, task_id)
        user = db.session.get(User, user_id)

        if not task:
            return jsonify({'message': 'Task not found'}), 404
        if not user:
            return jsonify({'message': 'User not found'}), 404

        task.assign_user(user)
        db.session.commit()

        return jsonify({'message': 'Task assigned successfully'}), 200

    except ValueError as e:
        return jsonify({'message': str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Server error assigning task'}), 500

@bp.route('/tasks/<int:task_id>/status', methods=['PATCH'])
@login_required
def update_task_status(task_id):
    """Updates the status of a specific task."""

    # Verify admin permissions
    if current_user.role != 'admin':
        return jsonify({'message': 'Admin access required'}), 403

    # Find the task
    from backend.app.models import Task  # Avoid circular import
    task = db.session.get(Task, task_id)
    if not task:
        return jsonify({'message': 'Task not found'}), 404

    # Get request data
    if not request.is_json:  # Check for JSON content type
        return jsonify({'message': 'Request must be JSON'}), 400
    data = request.get_json()
    if not data or 'status' not in data:
        return jsonify({'message': 'Status is required'}), 400

    # Update the task status
    new_status = data['status']
    try:
        task.update_status(new_status)
        return jsonify({'message': 'Task status updated'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Server error updating task status'}), 500

@bp.route('/tasks/<int:task_id>/deadline', methods=['PATCH'])
@login_required
def update_task_deadline_route(task_id):
    """Update deadline for a specific task"""
    try:
        # Verify admin permissions
        if current_user.role != 'admin':
            return jsonify({'message': 'Admin access required'}), 403
        
        # Validate request format
        if not request.is_json:
            return jsonify({'message': 'Request must be JSON'}), 400
        
        data = request.get_json()
        if 'deadline' not in data:
            return jsonify({'message': 'Deadline field required'}), 400
        
        # Convert ISO string to datetime object (supports with/without timezone)
        try:
            new_deadline = parser.isoparse(data['deadline'])
        except (ValueError, TypeError) as e:
            return jsonify({'message': f'Invalid datetime format: {str(e)}'}), 400
            
        # Update via model function
        from backend.app.models import update_task_deadline
        updated_task = update_task_deadline(task_id, new_deadline)
        return jsonify({'message': 'Deadline updated successfully'}), 200
        
    except ValueError as e:
        return jsonify({'message': str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Server error updating deadline'}), 500
