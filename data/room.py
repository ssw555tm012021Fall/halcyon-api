from sqlalchemy import Column, Integer, String, DateTime, Time
from sqlalchemy.sql.sqltypes import BOOLEAN, CHAR

from server import db


class Room(db.Model):
    __tablename__ = 'meditation_room'
    id = Column(Integer, primary_key=True, autoincrement=True)
    room_name = Column(String)
    description = Column(String)
    time_interval = Column(Integer)
    start_available_time = Column(Time)
    end_available_time = Column(Time)
    picture = Column(String)

    def __init__(self, room_name, description, time_interval, start_available_time, end_available_time, picture):
        self.room_name = room_name
        self.description = description
        self.time_interval = time_interval
        self.start_available_time = start_available_time
        self.end_available_time = end_available_time
        self.picture = picture

    def serialize(self):
        return {
            'id': self.id,
            'name': self.room_name,
            'description': self.description,
            'timeInterval': self.time_interval,
            'startAvailableTime': self.start_available_time.strftime("%H:%M:%S"),
            'endAvailableTime': self.end_available_time.strftime("%H:%M:%S"),
            'picture': self.picture
        }
