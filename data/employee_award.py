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
