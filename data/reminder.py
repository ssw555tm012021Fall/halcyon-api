import enum

from sqlalchemy import Column, Integer, DateTime, Time, Enum

# from data import db
# from data.db import Base
from server import db


class ReminderType(enum.Enum):
    WATER = 'water'
    BREAK = 'break'


class Reminder(db.Model):
    __tablename__ = 'reminder'
    id = Column(Integer, primary_key=True, autoincrement=True)
    employeeId = Column('employeeId', Integer)
    startAt = Column('start_at', Time)
    endAt = Column('end_at', Time)
    type = Column('type', Enum(ReminderType, values_callable=lambda obj: [e.value for e in obj]))
    interval = Column('interval', Integer)

    def __init__(self, employeeId, startAt, endAt, reminder_type, interval):
        self.employeeId = employeeId
        self.startAt = startAt
        self.endAt = endAt
        self.type = reminder_type
        self.interval = interval

    def serialize(self):
        return {
            'id': self.id,
            'employeeId': self.employeeId,
            'startAt': self.startAt.strftime("%H:%M:%S"),
            'endAt': self.endAt.strftime("%H:%M:%S"),
            'type': self.type.value,
            'interval': self.interval
        }
