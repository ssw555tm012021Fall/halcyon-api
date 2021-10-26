import unittest
from app import app


class TestBase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
