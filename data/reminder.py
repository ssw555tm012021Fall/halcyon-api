import enum

from sqlalchemy import Column, Integer, DateTime, Time, Enum

from data.db import Base


class ReminderType(enum.Enum):
    WATER = 'water'
    BREAK = 'break'


class Reservation(Base):
    __tablename__ = 'reminder'
    id = Column(Integer, primary_key=True, autoincrement=True)
    employee_id = Column(Integer)
    start_at = Column(Time)
    end_at = Column(Time)
    type = Column('type', Enum(ReminderType))
    interval = Column(Integer)

    def __init__(self, employee_id, start_at, end_at, reminder_type, interval):
        self.employee_id = employee_id
        self.start_at = start_at
        self.end_at = end_at
        self.type = reminder_type
        self.interval = interval
