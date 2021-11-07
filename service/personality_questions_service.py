from data.personality_questions import PersonalityQuestions
from data.personality_options import PersonalityOptions
from server import db


def get_all_questions():
    """
        Get list of questions
        """
    return db.session.query(PersonalityQuestions).all()


def get_question_by_id(question_id):
    """
        Get list of questions
        """
    return db.session.query(PersonalityQuestions).filter(PersonalityQuestions.id == question_id).first()


def add_question(personality_question):
    db.session.add(personality_question)
    db.session.commit()
    db.session.refresh(personality_question)
    return personality_question


def get_all_options():
    """
        Get list of options
        """
    return db.session.query(PersonalityOptions).all()


def get_options_by_question_id(question_id):
    """
        Get list of options
        """
    return db.session.query(PersonalityOptions).filter(PersonalityOptions.questionId == question_id).all()


def add_options(personality_question_options):
    for option in personality_question_options:
        db.session.add(option)
        db.session.commit()


def get_all_questions_with_options():
    questions = get_all_questions()
    options = get_all_options()
    response_questions = []

    for question in questions:
        question_dict = {}
        question_options = []
        for option in options:
            if option.questionId == question.id:
                question_options.append(option.serialize())

        question_dict['id'] = question.id
        question_dict['content'] = question.content
        question_dict['index'] = question.index
        question_dict['options'] = question_options

        response_questions.append(question_dict)

    return response_questions


def get_question_with_options(question_id):
    question = get_question_by_id(question_id)
    options = get_options_by_question_id(question_id)
    question_dict = {}
    question_options = []
    for option in options:
        question_options.append(option.serialize())
    question_dict['id'] = question.id
    question_dict['content'] = question.content
    question_dict['index'] = question.index
    question_dict['options'] = question_options
    return question_dict
