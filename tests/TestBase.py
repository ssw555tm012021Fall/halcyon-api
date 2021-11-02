import unittest

from server import app, db
from flask_testing import TestCase

from tests.helper import create_active_user, create_confirmation_code, create_sound1, create_sound2


class TestBase(TestCase):

    def create_app(self):
        app.config.from_object('server.config.TestingConfig')
        return app

    def setUp(self):
        db.create_all()
        db.session.commit()

        # put all helper functions here to add data
        new_active_user = create_active_user()
        create_confirmation_code(new_active_user)
        create_sound1()
        create_sound2()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
