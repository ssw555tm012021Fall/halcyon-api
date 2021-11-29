from data.award import Awards
from server import db
from data.employee_award import EmployeeAward


def get_award_by_id(award_id):
    """ get Room object searched from primary key """
    return db.session.query(Awards).filter(Awards.id == award_id).first()


def add_award(award):
    db.session.add(award)
    db.session.commit()

def add_award_return_id(award):
    db.session.add(award)
    db.session.commit()
    db.session.refresh(award)
    return award



def get_employee_award_by_id(employee_award_id):
    """ get Room object searched from primary key """
    return db.session.query(EmployeeAward).filter(EmployeeAward.id == employee_award_id).first()


def add_employee_award(employee_award):
    db.session.add(employee_award)
    db.session.commit()

def add_employee_award_return_id(employee_award):
    db.session.add(employee_award)
    db.session.commit()
    db.session.refresh(employee_award)
    return employee_award

