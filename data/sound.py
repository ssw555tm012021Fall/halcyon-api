import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from server import db
from sqlalchemy.sql.sqltypes import BOOLEAN, CHAR


class Sound(db.Model):
    """The Sound class corresponds to the "Sound" database table.
    """
    __tablename__ = 'sound'
    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String)
    length = Column(Integer)
    name = Column(String)
    credit = Column(String)
    url = Column(String)
    type = Column(String)

    def __init__(self, description, length, name, credit, url, sound_type):
        """
        TODO: add all the fields of Sounds
        """
        self.description = description
        self.length = length
        self.name = name
        self.credit = credit
        self.url = url
        self.type = sound_type
