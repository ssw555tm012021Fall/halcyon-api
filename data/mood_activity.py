import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from server import db
from sqlalchemy.sql.sqltypes import BOOLEAN, CHAR


class mood_activity(db.Model):
    """The mood_activity class corresponds to the "mood_activity" database table.
    """
    __tablename__ = 'mood_activity'
    id = Column(Integer, primary_key=True, autoincrement=True)
    input_emotion = Column(String)
    activity = Column(String)
    output_emotion = Column(String)


    def __init__(self, input_emotion, activity, output_emotion):
        """
        TODO: add all the fields of moods
        """
        self.input_emotion = input_emotion
        self.activity = activity
        self.output_emotion = output_emotion

