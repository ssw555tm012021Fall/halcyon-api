from sqlalchemy_cockroachdb import run_transaction

# from data.db import session, sessionmaker
from data.events import Events
from server import db



def get_event_by_id(id):
    return db.session.query(Events).filter(Events.id == id).first()


def add_event(Events):
    db.session.add(Events)
    db.session.commit()

def add_event_return_id(event):
    db.session.add(event)
    db.session.commit()
    db.session.refresh(event)
    return event

