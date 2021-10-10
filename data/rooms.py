import datetime
import jwt
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from data.db import Base
from server import app, bcrypt, BCRYPT_LOG_ROUNDS
from sqlalchemy.sql.sqltypes import BOOLEAN, CHAR

class Rooms(Base):
    """The Rooms class corresponds to the "room_reserved" database table.
    """
    __tablename__ = 'room_reserved'
    id = Column(Integer, primary_key=True, autoincrement=True)
    meditation_room_id = Column(Integer)
    reservation_id = Column(Integer)


    def __init__(self, meditation_room_id: int, reservation_id: int):
        self.meditation_room_id = meditation_room_id
        self.reservation_id = reservation_id

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
