from functools import wraps
from typing import Callable

import jwt
from flask import current_app
from flask import jsonify
from flask import request
from jwt import DecodeError
from jwt import ExpiredSignatureError

from backend.models import User


def authorize(f: Callable) -> Callable:
    @wraps(f)
    def decorated(*args, **kwargs) -> tuple:
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'error': 'Unauthorized! TOKEN Missing!'}), 401

        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
        except ExpiredSignatureError:
            return jsonify({'error': 'Unauthorized! TOKEN Expired!'}), 401
        except DecodeError:
            return jsonify({'error': 'I\'m a Tea Pot; and your token is Missing Fragments...'}), 418
        else:
            current_user = User.query.filter(User.user_uuid == data['user_uuid']).one()
            return f(current_user, *args, **kwargs)

    return decorated
