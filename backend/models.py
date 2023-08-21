import logging
import uuid

from sqlalchemy import UUID
from sqlalchemy.exc import IntegrityError

from backend.exceptions import APIException
from backend.extensions import db

logger = logging.getLogger(__name__)


class Model(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    def save(self):
        db.session.add(self)
        try:
            db.session.commit()
        except IntegrityError as sql_exception:
            logger.exception(sql_exception)
            db.session.rollback()
            raise APIException(detail='Unable to save to DB.') from sql_exception

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, id, options=None):
        query = cls.query.filter(cls.id == id)
        if options is not None:
            query = query.options(options)
        return query.one()


class User(Model):
    user_uuid = db.Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True)
    name = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean)
    password_hash = db.Column(db.String(120), nullable=True)
    todos = db.relationship('ToDo', back_populates='user', uselist=True)


class ToDo(Model):
    text = db.Column(db.String(150))
    complete = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='todos')


class MagicLink(Model):
    ...
