from backend.api.users import users


@users.route('/users', methods=['POST'])
def create_user():
    return ''


@users.route('/users', methods=['GET'])
def get_all_users():
    return ''


@users.route('/users/<user_id>', methods=['GET'])
def get_user():
    return ''


@users.route('/users/<user_id>', methods=['PUT'])
def promote_user():
    return ''


@users.route('/users/<user_id', methods=['DELETE'])
def delete_user():
    return ''
