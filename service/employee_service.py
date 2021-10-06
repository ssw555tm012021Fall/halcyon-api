from sqlalchemy_cockroachdb import run_transaction
from data.db import session, sessionmaker
from data.employee import Employee

def get_employee_by_email(email):
    return session.query(Employee).filter(Employee.email == email).first()

def get_employee_by_id(id):
    return session.query(Employee).filter(Employee.id == id).first()

def get_employee_by_public_id(public_id):
    return session.query(Employee).filter(Employee.public_id == public_id).first()

def get_employee_by_public_id_expunged(public_id):
    return session.expunge(session.query(Employee).filter(Employee.public_id == public_id).first())

def add_employee(employee):
    session.add(employee)
    session.commit()

def add_employee_return_id(employee):
    session.add(employee)
    session.commit()
    session.refresh(employee)
    return employee

def add_employee_in_txn(employee):
    return run_transaction(sessionmaker, lambda sess: sess.add(employee))