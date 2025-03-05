from flask import request, jsonify, Blueprint, current_app
from backend.app.models import create_user
from sqlalchemy.exc import IntegrityError

bp = Blueprint('users', __name__, url_prefix='/users')

@bp.route('', methods=['POST'])
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
        db = current_app.extensions['sqlalchemy'].db
        db.session.rollback()
        return jsonify({'message': 'User with this username or email already exists.'}), 409