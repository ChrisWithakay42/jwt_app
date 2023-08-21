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
    return jsonify({'data': 'New user created.'})


@users_bp.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    output = []

    for user in users:
        user_data = dict()
        user_data['user_uuid'] = user.user_uuid
        user_data['name'] = user.name
        user_data['password'] = user.password_hash
        user_data['is_admin'] = user.is_admin
        output.append(user_data)

    return jsonify({'data': output})


@users_bp.route('/users/<user_uuid>', methods=['GET'])
def get_user(user_uuid):
    user = User.query.filter(User.user_uuid == user_uuid).one_or_none()
    if user is None:
        return jsonify({'data': 'No User found'})

    user_data = dict()
    user_data['user_uuid'] = user.user_uuid
    user_data['name'] = user.name
    user_data['password'] = user.password_hash
    user_data['is_admin'] = user.is_admin

    return jsonify({'data': user_data})


@users_bp.route('/users/<user_uuid>', methods=['PUT'])
def promote_user(user_uuid):
    user = User.query.filter(User.user_uuid == user_uuid).one_or_none()
    if user is None:
        return jsonify({'data': 'No User found'})
    user.is_admin = True
    user.save()
    return jsonify({'data': user}), 200


@users_bp.route('/users/<user_uuid>', methods=['DELETE'])
def delete_user(user_uuid):
    user = User.query.filter(User.user_uuid == user_uuid).one_or_none()
    if user is None:
        return jsonify({'data': 'No User found'})

    user.delete()
    return jsonify({'data': ''}), 204
