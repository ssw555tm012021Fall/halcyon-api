import enum

from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship

from server import db


class OptionValue(enum.Enum):
    e = 'e'
    i = 'i'
    s = 's'
    n = 'n'
    t = 't'
    f = 'f'
    j = 'j'
    p = 'p'


class PersonalityOptions(db.Model):
    __tablename__ = 'personality_options'
    id = Column(Integer, primary_key=True, autoincrement=True)
    questionId = Column('question_id', Integer)
    content = Column('content', String)
    index = Column('index', Integer)
    value = Column('value', Enum(OptionValue))
    a = relationship('PersonalityQuestions', foreign_keys=[questionId], primaryjoin='PersonalityQuestions.id == '
                                                                                    'PersonalityOptions.questionId')

    def __init__(self, questionId, content, index, value):
        self.questionId = questionId
        self.content = content
        self.index = index
        self.value = value

    def serialize(self):
        return {
            'id': self.id,
            'questionId': self.questionId,
            'content': self.content,
            'index': self.index,
            'value': self.value.name
        }
