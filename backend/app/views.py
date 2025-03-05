from flask import request, jsonify, Blueprint, current_app
from backend.app.models import create_user
from sqlalchemy.exc import IntegrityError

bp = Blueprint('users', __name__, url_prefix='/users')

@bp.route('', methods=['POST'])
def create_user_route():
    data = request.get_json()

    if not 
        return jsonify({'message': 'No data provided'}), 400

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')

    try:
        user = create_user(username=username, email=email, password=password, role=role)
        return jsonify({'id': user.id}), 201
    except ValueError as e:
        return jsonify({'message': str(e)}), 400
    except IntegrityError:
        db = current_app.extensions['sqlalchemy'].db # Access db through the app context
        db.session.rollback()
        return jsonify({'message': 'Could not create user.'}), 400
