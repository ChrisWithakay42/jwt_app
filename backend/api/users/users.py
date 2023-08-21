import uuid

from flask import Blueprint
from flask import jsonify
from flask import request
from werkzeug.security import generate_password_hash

from backend.models import User

users_bp = Blueprint('users_bp', __name__, url_prefix='/app')


@users_bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()

    hashed_password = generate_password_hash(data['password'], method='sha256')

    new_user = User(user_uuid=str(uuid.uuid4()), name=data['name'], password_hash=hashed_password, is_admin=False)
    new_user.save()
    return jsonify({'message': 'New user created.'})


@users_bp.route('/users', methods=['GET'])
def get_all_users():
    return ''


@users_bp.route('/users/<user_id>', methods=['GET'])
def get_user():
    return ''


@users_bp.route('/users/<user_id>', methods=['PUT'])
def promote_user():
    return ''


@users_bp.route('/users/<user_id>', methods=['DELETE'])
def delete_user():
    return ''
