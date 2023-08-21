from functools import wraps

from flask import request


def token_required(f: callable):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
