import click
from flask.cli import with_appcontext
from werkzeug.security import generate_password_hash

from backend.exceptions import APIException
from backend.models import User


@click.command('create_user')
@with_appcontext
@click.argument('user_name', required=True)
@click.argument('password', required=True)
def create_admin_user(user_name: str, password: str) -> None:
    password_hash = generate_password_hash(password, method='sha256')
    user = User(user_name=user_name, password_hash=password_hash, is_admin=True)
    try:
        user.save()
    except APIException as api_exc:
        click.echo(f'An error occurred while creating new user. Check for further errors below. \n{api_exc}')
    else:
        click.echo(f'Successfully created user with username: `{user_name}`.')
