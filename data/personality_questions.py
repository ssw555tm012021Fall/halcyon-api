from sqlalchemy import Column, Integer, String
from server import db


class PersonalityQuestions(db.Model):
    __tablename__ = 'personality_questions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column('content', String)
    index = Column('index', Integer)

    def __init__(self, content, index):
        self.content = content
        self.index = index
