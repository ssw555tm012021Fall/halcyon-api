from sqlalchemy import Column, Integer, DateTime, Time

from data.db import Base


class Reservation(Base):
    __tablename__ = 'reservation'
    id = Column(Integer, primary_key=True, autoincrement=True)
    employee_id = Column(Integer)
    meditation_room_id = Column(Integer)
    date_reservation = Column(DateTime)
    start_time = Column(Time)
    end_time = Column(Time)

    def __init__(self, employee_id, meditation_room_id, date_reservation, start_time, end_time):
        self.employee_id = employee_id
        self.meditation_room_id = meditation_room_id
        self.date_reservation = date_reservation
        self.start_time = start_time
        self.end_time = end_time
