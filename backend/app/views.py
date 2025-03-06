from flask import request, jsonify, Blueprint, current_app
from backend.app.models import create_user, User, db  # Import User and db
from sqlalchemy.exc import IntegrityError
from flask_login import login_user, logout_user, login_required, current_user

# Use 'auth' as the blueprint name, and don't set a url_prefix here
bp = Blueprint('auth', __name__)

def authenticate_user(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return user
    return None

@bp.route('/users', methods=['POST'])
def create_user_route():
    data = request.get_json()

    # Check if data is provided
    if not data:
        return jsonify({'message': 'No data provided'}), 400

    # Validate required fields
    required_fields = ['username', 'email', 'password', 'role']
    for field in required_fields:
        if field not in data:
            return jsonify({'message': f'Missing field: {field}'}), 400

    # Extract fields
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
        # Access the database session correctly through the current app
        db.session.rollback()
        return jsonify({'message': 'User with this username or email already exists.'}), 409

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({'status': 'error', 'message': 'No data provided'}), 400

    username = data.get('username')
    password = data.get('password')

    user = authenticate_user(username, password)

    if user:
        login_user(user, remember=True)
        return jsonify({'status': 'success'}), 200
    else:
        return jsonify({'status': 'error', 'message': 'Invalid credentials'}), 401

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully'}), 200

@bp.route('/protected')
@login_required
def protected():
    """
    A protected endpoint that requires authentication.
    """
    return jsonify({
        'id': current_user.id,
        'username': current_user.username,
        'email': current_user.email,
        'role': current_user.role,
    })
