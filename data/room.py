from sqlalchemy import Column, Integer, String, DateTime, Time
from data.db import Base
from sqlalchemy.sql.sqltypes import BOOLEAN, CHAR


class Room(Base):
    __tablename__ = 'meditation_room'
    id = Column(Integer, primary_key=True, autoincrement=True)
    room_name = Column(String)
    description = Column(String)
    time_interval = Column(Integer)
    start_available_time = Column(Time)
    end_available_time = Column(Time)

    def __init__(self, room_name, description, time_interval, start_available_time, end_available_time):
        self.room_name = room_name
        self.description = description
        self.time_interval = time_interval
        self.start_available_time = start_available_time
        self.end_available_time = end_available_time
