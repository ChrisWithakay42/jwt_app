import datetime
import jwt
from flask import Blueprint
from flask import current_app
from flask import jsonify
from flask import make_response
from flask import request
from werkzeug.security import check_password_hash

from backend.models import User

login_bp = Blueprint('login_bp', __name__, url_prefix='/auth')


@login_bp.route('/login', methods=['POST'])
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    user = User.query.filter(User.user_name == auth['username']).one_or_none()

    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    if check_password_hash(user.password_hash, auth.password):
        token = jwt.encode({
            'user_uuid': str(user.user_uuid),
            'exp': datetime.datetime.now() + datetime.timedelta(minutes=180),
        },
            current_app.config['SECRET_KEY'],
            algorithm="HS256"
        )
        return jsonify({'token': token})

    return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
