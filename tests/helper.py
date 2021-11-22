from datetime import datetime

from data.code_confirmation import code_confirmation
from data.employee import Employee
from data.personality_options import PersonalityOptions
from data.personality_questions import PersonalityQuestions
from data.sound import Sound
from server import db

today = datetime.today()


def create_active_user():
    employee = Employee('viyetak@stevens.edu', 'Password123', '', True, '', today, 'f', False)
    db.session.add(employee)
    db.session.commit()
    db.session.refresh(employee)
    return employee


def create_confirmation_code(employee):
    code = code_confirmation(
        employee_id=employee.id,
        code=12345,
        expiry_date=today,
        code_confirmation_time=datetime.time(today)
    )
    db.session.add(code)
    db.session.commit()


def create_sound1():
    sound = Sound(
        description='Rain sounds',
        name='rain',
        length=1822,
        credit='Me',
        url='https://ssw-555-halcyon.s3.amazonaws.com/sound/audio/rain.mp3',
        sound_type='sound',
        picture='https://ssw-555-halcyon.s3.amazonaws.com/sound/images/rain.jpg'
    )
    db.session.add(sound)
    db.session.commit()


def create_sound2():
    sound = Sound(
        description='Breathing relaxation',
        name='Three minute breathing',
        length=216000,
        credit='Peter Morgan',
        url='https://ssw-555-halcyon.s3.amazonaws.com/meditation/audio/3-min-breathing-p-morgan.mp3',
        sound_type='guide',
        picture='https://ssw-555-halcyon.s3.amazonaws.com/meditation/images/3-min-breathing-p-morgan.jpg'
    )
    db.session.add(sound)
    db.session.commit()
    db.session.refresh(sound)
    return sound


def create_personality_question_and_options():
    question = PersonalityQuestions(
        content='At a party do you',
        index=1
    )
    db.session.add(question)
    db.session.commit()
    db.session.refresh(question)
    option1 = PersonalityOptions(
        questionId=question.id,
        content='Interact with many, including strangers',
        index=1,
        value='e'
    )
    db.session.add(option1)
    db.session.commit()
    option2 = PersonalityOptions(
        questionId=question.id,
        content='Interact with a few, known to you',
        index=2,
        value='i'
    )
    db.session.add(option2)
    db.session.commit()
    return question
