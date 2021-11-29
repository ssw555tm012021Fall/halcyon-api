import datetime
import jwt
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Time
from server import app, db
from sqlalchemy.sql.sqltypes import BOOLEAN, CHAR, TIMESTAMP
import Enum

class Event_State(enum.Enum):
    completed = 'completed'
    cancel = 'cancel'

class Event_Category(enum.Enum):
    guided_meditation = 'guided_meditation'
    meditation = 'meditation'
    water = 'water'
    break_category = 'break'



class Awards(db.Model):
    """The Employee class corresponds to the "employee" database table.
    """
    __tablename__ = 'award'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(Integer)
    description = Column(String)
    target = Column(Integer)
    image = Column(String)
    category = Column('category', Enum(Event_Category))
    frequency = Column(String)
    created_at = Column('created_at', Time)

    def __init__(self, title, description, target, image, category, frequency, created_at):
        self.title = title
        self.description = description
        self.target = target
        self.image = image
        self.category = category
        self.frequency = frequency
        self.created_at = created_at
