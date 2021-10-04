import datetime

import jwt
from sqlalchemy import Column, Integer, String, DateTime, Boolean

from data.db import Base
from server import app, bcrypt, BCRYPT_LOG_ROUNDS


class Employee(Base):
    """The Employee class corresponds to the "employee" database table.
    """
    __tablename__ = 'employee'
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String)
    password = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    is_confirmed = Column(Boolean)
    birthday = Column(DateTime)
    gender = Column(String)

    def __init__(self, email, password, first_name):
        """
        TODO: add all the fields of Employee
        """
        self.email = email
        self.password = bcrypt.generate_password_hash(
            password, BCRYPT_LOG_ROUNDS
        ).decode()
        self.first_name = first_name
        # self.created = datetime.datetime.now()

    def encode_auth_token(self, user_id):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=5),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Validates the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'), algorithms=['HS256'],
                                 options={"verify_signature": False})
            # TODO: check blacklisted token
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'
