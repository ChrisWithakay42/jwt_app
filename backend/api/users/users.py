import uuid

from flask import Blueprint
from flask import jsonify
from flask import request
from werkzeug.security import generate_password_hash

from backend.auth.perm import authorize
from backend.models import User

users_api = Blueprint('users_api', __name__, url_prefix='/api')


@users_api.route('/users', methods=['POST'])
@authorize
def create_user(current_user: User) -> tuple:
    if not current_user.is_admin:
        return jsonify({'error': 'Permission Denied'}), 403

    data = request.get_json()

    hashed_password = generate_password_hash(data['password'], method='sha256')

    model = User(user_name=data['user_name'], password_hash=hashed_password, is_admin=False)
    model.save()
    return jsonify({'data': 'New User Created.'}), 200


@users_api.route('/users', methods=['GET'])
@authorize
def get_all_users(current_user: User) -> tuple:
    if not current_user.is_admin:
        return jsonify({'error': 'Permission Denied!'}), 403

    users = User.query.all()
    output = []

    for user in users:
        user_data = dict()
        user_data['user_uuid'] = user.user_uuid
        user_data['user_name'] = user.user_name
        user_data['password'] = user.password_hash
        user_data['is_admin'] = user.is_admin
        output.append(user_data)

    return jsonify({'data': output}), 200


@users_api.route('/users/<user_uuid>', methods=['GET'])
@authorize
def get_user(current_user: User, user_uuid: uuid) -> tuple:

    if not current_user.is_admin:
        return jsonify({'error': 'Permission Denied!'}), 403

    user = User.query.filter(User.user_uuid == user_uuid).one_or_none()

    if user is None:
        return jsonify({'error': 'User Not Found!'}), 404

    user_data = dict()
    user_data['user_uuid'] = user.user_uuid
    user_data['user_name'] = user.user_name
    user_data['password'] = user.password_hash
    user_data['is_admin'] = user.is_admin

    return jsonify({'data': user_data}), 200


@users_api.route('/users/<user_uuid>', methods=['PUT'])
@authorize
def promote_user(current_user: User, user_uuid: uuid) -> tuple:

    if not current_user.is_admin:
        return jsonify({'error': 'Permission Denied!'}), 403

    user = User.query.filter(User.user_uuid == user_uuid).one_or_none()
    if user is None:
        return jsonify({'error': 'User Not Found!'}), 404
    user.is_admin = True
    user.save()
    return jsonify({'data': 'User Successfully Promoted to Admin Role!'}), 200


@users_api.route('/users/<user_uuid>', methods=['DELETE'])
@authorize
def delete_user(current_user: User, user_uuid: uuid):

    if not current_user.is_admin:
        return jsonify({'data': 'Permission Denied!'}), 403

    user = User.query.filter(User.user_uuid == user_uuid).one_or_none()
    if user is None:
        return jsonify({'data': 'User Not Found!'}), 404

    user.delete()
    return jsonify({'data': {}}), 201
