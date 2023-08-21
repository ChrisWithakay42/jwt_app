from flask import Blueprint
from flask import jsonify
from flask import make_response
from flask import request
from werkzeug.security import check_password_hash

from backend.jwt import generate_jwt
from backend.models import User

login_bp = Blueprint('login_bp', __name__, url_prefix='')


@login_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data or 'username' not in data or 'password' not in data:
        return make_response(jsonify({'message': 'Invalid credentials'}), 401)

    user = User.query.filter(User.name == data['username']).one_or_none()

    if not check_password_hash(user.password_hash, data['password']):
        return make_response(jsonify({'message': 'Invalid credentials'}), 401)

    token = generate_jwt(user_uuid=user.user_uuid, signer='secret')
    return jsonify({'token': token})
