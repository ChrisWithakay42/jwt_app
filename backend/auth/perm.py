from functools import wraps

import jwt
from flask import current_app
from flask import jsonify
from flask import request
from jwt import DecodeError
from jwt import ExpiredSignatureError

from backend.models import User


def authorize(f: callable):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'data': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
        except ExpiredSignatureError:
            return jsonify({'data': 'Token has expired!'}), 401
        except DecodeError as e:
            return jsonify({'data': e})
        else:
            current_user = User.query.filter(User.user_uuid == data['user_uuid']).one()
            return f(current_user, *args, **kwargs)

    return decorated



