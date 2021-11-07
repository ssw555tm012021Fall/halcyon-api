from data.personality_questions import PersonalityQuestions
from data.personality_options import PersonalityOptions
from server import db


def get_all_questions():
    """
        Get list of questions
        """
    return db.session.query(PersonalityQuestions).all()


def get_all_options():
    """
        Get list of options
        """
    return db.session.query(PersonalityOptions).all()
