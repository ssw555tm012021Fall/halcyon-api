import datetime
import jwt
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from data.db import Base
from server import app, bcrypt, BCRYPT_LOG_ROUNDS
from sqlalchemy.sql.sqltypes import BOOLEAN, CHAR

class Meditation(Base):
    """The Meditation class corresponds to the "meditationß" database table.
    """
    __tablename__ = 'meditation_room'
    id = Column(Integer, primary_key=True, autoincrement=True)
    room_name = Column(String)
    description = Column(String)
    time_interval = Column(Integer)
    start_available_time = Column(DateTime)
    end_available_time = Column(DateTime)


    def __init__(self, room_name: str, description: str, time_interval: int, start_available_time: datetime, end_available_time: datetime):
        self.room_name = room_name
        self.description = description
        self.time_interval = time_interval
        self.start_available_time = start_available_time
        self.end_available_time = end_available_time

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
