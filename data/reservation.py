import datetime
import jwt
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from data.db import Base
from server import app, bcrypt, BCRYPT_LOG_ROUNDS
from sqlalchemy.sql.sqltypes import BOOLEAN, CHAR

class Reservation(Base):
    """The Reservation class corresponds to the "reservation" database table.
    """
    __tablename__ = 'reservation'
    id = Column(Integer, primary_key=True, autoincrement=True)
    meditation_room_id = Column(Integer)
    employee_id = Column(Integer)
    date_reservation = Column(DateTime)
    start_time = Column(DateTime)
    end_time = Column(DateTime)



    def __init__(self, employee_id: int, meditation_room_id:int, date_reservation: datetime, start_time: datetime, end_time: datetime):
        self.employee_id = employee_id
        self.meditation_room_id = meditation_room_id
        self.date_reservation = date_reservation
        self.start_time = start_time
        self.end_time = end_time

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
