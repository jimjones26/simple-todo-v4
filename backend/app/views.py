from flask import request, jsonify, Blueprint
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
    team = Team.query.get(team_id)
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
    team = Team.query.get(team_id)
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
