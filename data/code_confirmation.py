"""
    File name: code_confirmation.py
    Added by: Farah Elkourdi
    Date created: 10/06/2021
    Date last modified: 10/06/2021
    Description:Code confirmation data
"""
import datetime
import jwt
from sqlalchemy import Column, Integer, String, DateTime, Boolean, TIME
from sqlalchemy.types import Date
# from data.db import Base
from server import db


class code_confirmation(db.Model):
    """The code_confirmation class corresponds to the "code_confirmation" database table.
    """
    __tablename__ = 'code_confirmation'
    id = Column(Integer, primary_key=True, autoincrement=True)
    employee_id = Column(Integer)
    code = Column(Integer)
    expiry_date = Column(Date)
    code_confirmation_time = Column(TIME)

    def __init__(self, employee_id, code, expiry_date, code_confirmation_time):
        """
        TODO: add all the fields of code_confirmation
        """
        self.employee_id = employee_id
        self.code = code
        self.expiry_date = expiry_date
        self.code_confirmation_time = code_confirmation_time
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
