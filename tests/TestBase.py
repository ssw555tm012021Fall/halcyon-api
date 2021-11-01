import unittest
from datetime import datetime

# from flask_sqlalchemy import SQLAlchemy
# from flask_testing import TestCase

# from app import app
# from data import db
# from data.db import session
# from data.employee import Employee
from server import app, db
from flask_testing import TestCase


class TestBase(TestCase):

    def create_app(self):
        app.config.from_object('server.config.TestingConfig')
        return app

    def setUp(self):
        # app.testing = True
        # self.app = app.test_client()
        # self.app.testing = True
        # Employee.create(db.engine)
        # db.session.create_all()
        db.create_all()
        db.session.commit()
        # Employee.__table__.create(db.engine)

        # today = datetime.today()
        # employee1 = Employee('test_user1@example.com', 'password', '', False, '', today, 'f')
        # db.session.add(employee1)
        # db.session.commit()
        #
        # employee2 = Employee('test_user2@example.com', 'password', '', False, '', today, 'm')
        # db.session.add(employee2)
        # db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
