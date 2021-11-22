import datetime
import jwt
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Time
from server import app, db
from sqlalchemy.sql.sqltypes import BOOLEAN, CHAR, TIMESTAMP

class EmployeeAward(db.Model):
    """The Employee class corresponds to the "employee" database table.
    """
    __tablename__ = 'employee_award'
    id = Column(Integer, primary_key=True, autoincrement=True)
    employee_id = Column(Integer)
    award_id = Column(Integer)
    created_at = Column('created_at', Time)

    def __init__(self, employee_id, award_id, created_at):
        self.employee_id = employee_id
        self.award_id = award_id
        self.created_at = created_at

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
