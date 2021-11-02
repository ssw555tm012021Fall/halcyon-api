from datetime import datetime

from data.code_confirmation import code_confirmation
from data.employee import Employee
from data.sound import Sound
from server import db

today = datetime.today()


def create_active_user():
    employee = Employee('viyetak@stevens.edu', 'Password123', '', True, '', today, 'f')
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
        url='https://ssw-555-halcyon.s3.amazonaws.com/sound/rain.mp3',
        sound_type='sound'
    )
    db.session.add(sound)
    db.session.commit()


def create_sound2():
    sound = Sound(
        description='Breathing relaxation',
        name='Three minute breathing',
        length=216000,
        credit='Peter Morgan',
        url='https://ssw-555-halcyon.s3.amazonaws.com/meditation/3-min-breathing-p-morgan.mp3',
        sound_type='guide'
    )
    db.session.add(sound)
    db.session.commit()
    db.session.refresh(sound)
    return sound
