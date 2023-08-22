import uuid

from flask import Blueprint
from flask import jsonify
from flask import request
from werkzeug.security import generate_password_hash

from backend.auth.perm import token_required
from backend.models import User

users_bp = Blueprint('users_bp', __name__, url_prefix='/app')


@users_bp.route('/users', methods=['POST'])
@token_required
def create_user(current_user):
    data = request.get_json()

    hashed_password = generate_password_hash(data['password'], method='sha256')

    model = User(user_uuid=str(uuid.uuid4()), name=data['name'], password_hash=hashed_password, is_admin=False)
    model.save()
    return jsonify({'data': 'New user created.'})


@users_bp.route('/users', methods=['GET'])
@token_required
def get_all_users(current_user):
    if not current_user.is_admin:
        return jsonify({'data': 'Can not perform that action!'}), 403

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
@token_required
def get_user(current_user, user_uuid):
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
@token_required
def promote_user(current_user, user_uuid):
    user = User.query.filter(User.user_uuid == user_uuid).one_or_none()
    if user is None:
        return jsonify({'data': 'No User found'})
    user.is_admin = True
    user.save()
    return jsonify({'data': 'User has been promoted to Admin role.'}), 200


@users_bp.route('/users/<user_uuid>', methods=['DELETE'])
@token_required
def delete_user(current_user, user_uuid):
    user = User.query.filter(User.user_uuid == user_uuid).one_or_none()
    if user is None:
        return jsonify({'data': 'No User found'})

    user.delete()
    return jsonify({'data': 'User has been deleted.'})
