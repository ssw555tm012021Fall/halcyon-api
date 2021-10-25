from sqlalchemy import Column, Integer, DateTime, Time

from data.db import Base


class Reservation(Base):
    __tablename__ = 'reservation'
    id = Column(Integer, primary_key=True, autoincrement=True)
    employeeId = Column('employee_id', Integer)
    meditationRoomId = Column('meditation_room_id', Integer)
    date = Column('date_reservation', DateTime)
    startTime = Column('start_time', Time)
    endTime = Column('end_time', Time)

    def __init__(self, employee_id, meditation_room_id, date_reservation, start_time, end_time):
        self.employeeId = employee_id
        self.meditationRoomId = meditation_room_id
        self.date = date_reservation
        self.startTime = start_time
        self.endTime = end_time
