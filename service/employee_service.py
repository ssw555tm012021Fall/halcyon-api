from sqlalchemy_cockroachdb import run_transaction

# from data.db import session, sessionmaker
from data.employee import Employee
from server import db


def get_employee_by_email(email):
    return db.session.query(Employee).filter(Employee.email == email).first()


def get_employee_by_id(id):
    return db.session.query(Employee).filter(Employee.id == id).first()


def get_employee_by_public_id(public_id):
    return db.session.query(Employee).filter(Employee.public_id == public_id).first()


def get_employee_by_public_id_expunged(public_id):
    return db.session.expunge(db.session.query(Employee).filter(Employee.public_id == public_id).first())


def add_employee(employee):
    db.session.add(employee)
    db.session.commit()

def add_employee_return_id(employee):
    db.session.add(employee)
    db.session.commit()
    db.session.refresh(employee)
    return employee

def activate_account(email):
    user = db.session.query(Employee).filter(Employee.email == email).first()
    user.is_confirmed = True
    db.session.commit()

def add_employee_in_txn(employee):
    return run_transaction(db.sessionmaker, lambda sess: sess.add(employee))

