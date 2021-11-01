# from data.db import session
from data.events import Events
from data.goals import Goals
from server import db
from shared.common import is_dirty


def get_goal_by_id(goal_id):
    """ get Room object searched from primary key """
    return db.session.query(Goals).filter(Goals.id == goal_id).first()


def get_goal_by_employee_id(employee_id):
    """ get Room object searched from primary key """
    return db.session.query(Goals).filter(Goals.employee_id == employee_id)


def add_goal(goal):
    db.session.add(goal)
    db.session.commit()

def add_goal_return_id(goal):
    db.session.add(goal)
    db.session.commit()
    db.session.refresh(goal)
    return goal

def update_goal(goal_id, target):
    db.session.query(Goals).update().where(Goals.id == goal_id).values(target=target)
    db.session.commit()
    return True

