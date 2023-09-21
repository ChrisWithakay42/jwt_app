import datetime

import jwt
from flask import Blueprint
from flask import Response
from flask import current_app
from flask import jsonify
from flask import request
from werkzeug.security import check_password_hash

from backend.models import User

login_bp = Blueprint('login_bp', __name__, url_prefix='/auth')


@login_bp.route('/login', methods=['POST'])
def login() -> tuple[Response, int]:
    data = request.get_json()
    user_name = data.get('user_name', None)
    password = data.get('password', None)

    if user_name is None or password is None:
        return jsonify({'message': 'Missing username or password'}), 400

    user = User.query.filter(User.user_name == user_name).one_or_none()

    if not user:
        return jsonify({'message': 'Could not verify User.'}), 401

    if check_password_hash(user.password_hash, password):
        token = jwt.encode({
            'user_uuid': str(user.user_uuid),
            'exp': datetime.datetime.now() + datetime.timedelta(minutes=180),
        },
            current_app.config['SECRET_KEY'],
            algorithm="HS256"
        )
        return jsonify({'token': f'Bearer {token}'}), 200

    return jsonify({'message': 'Could not verify Password.'}), 401
