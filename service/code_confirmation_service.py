"""
    File name: code_confirmation_service.py
    Added by: Farah Elkourdi
    Date created: 10/06/2021
    Date last modified: 10/06/2021
    Description:Code confirmation services
"""
from sqlalchemy_cockroachdb import run_transaction
from data.db import session, sessionmaker
from data.code_confirmation import code_confirmation

def get_code_confirmation_by_id(id):
    return session.query(code_confirmation).filter(code_confirmation.id == id).first()

def get_code_confirmation_by_public_id(public_id):
    return session.query(code_confirmation).filter(code_confirmation.public_id == public_id).first()

def get_code_confirmation_by_public_id_expunged(public_id):
    return session.expunge(session.query(code_confirmation).filter(code_confirmation.public_id == public_id).first())

def add_code_confirmation(code_confirmation):
    session.add(code_confirmation)
    session.commit()

def add_employee_in_txn(code_confirmation):
    return run_transaction(sessionmaker, lambda sess: sess.add(code_confirmation))