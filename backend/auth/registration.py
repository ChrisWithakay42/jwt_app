from flask import Blueprint
from flask import jsonify
from flask import request
from werkzeug.security import generate_password_hash

from backend.models import User

register = Blueprint('register', __name__, url_prefix='auth')


@register.route('/registration', methods=['POST'])
def register_user() -> tuple:
    data = request.get_json()

    hashed_password = generate_password_hash(data['password'], method='sha256')

    model = User(user_name=data['user_name'], password_hash=hashed_password)

    model.save()

    return jsonify({'data': 'Success!'}), 200


