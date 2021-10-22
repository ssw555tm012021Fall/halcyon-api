import unittest
from flask import app
from app import app
import  json

class AccountTestCases(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_case_1_signup(self):
        """ Fail signup gmail account """
        send_data = json.dumps({
            "email": "felkourdi@gmail.com",
            "password": "Ff@1234567"
        })
        response = self.app.post('http://127.0.0.1:4000/auth/register', headers={"Content-Type": "application/json"}, data=send_data)
        self.assertEqual(202, response.status_code)

    def test_case_2_signup(self):
        """ Fail signup weak password """
        send_data = json.dumps({
            "email": "farahelkourdi95@stevens.edu",
            "password": "1234"
        })
        response = self.app.post('http://127.0.0.1:4000/auth/register', headers={"Content-Type": "application/json"}, data=send_data)
        self.assertEqual(401, response.status_code)
        
    def test_case_3_signup(self):
        """ Fail signup account exists"""
        send_data = json.dumps({
            "email": "farahelkourdi@stevens.edu",
            "password": "Ff1234567891"
        })
        response = self.app.post('http://127.0.0.1:4000/auth/register', headers={"Content-Type": "application/json"}, data=send_data)
        self.assertEqual(202, response.status_code)

    def test_case_1_confirmation_code(self):
        """ Fail confirmation code - account is active """
        send_data = json.dumps({
            "email": "farahelkourdi@stevens.edu",
            "code": "82319"
        })
        response = self.app.post('http://127.0.0.1:4000/auth/Confirmation', headers={"Content-Type": "application/json"}, data=send_data)
        self.assertEqual(401, response.status_code)

    def test_case_2_confirmation_code(self):
        """ Fail confirmation code - wrong code """
        send_data = json.dumps({
            "email": "felkourd@stevens.edu",
            "code": "82319"
        })
        response = self.app.post('http://127.0.0.1:4000/auth/Confirmation', headers={"Content-Type": "application/json"}, data=send_data)
        self.assertEqual(401, response.status_code)

    def test_case_3_confirmation_code(self):
        """ User does not exist """
        send_data = json.dumps({
            "email": "test12345@stevens.edu",
            "code": "82319"
        })
        response = self.app.post('http://127.0.0.1:4000/auth/Confirmation', headers={"Content-Type": "application/json"}, data=send_data)
        self.assertEqual(401, response.status_code)

    def test_case_1_resend_code(self):
        """ Fail - Account is already active """
        send_data = json.dumps({
            "email": "farahelkourdi@stevens.edu"
        })
        response = self.app.post('http://127.0.0.1:4000/auth/resend', headers={"Content-Type": "application/json"}, data=send_data)
        self.assertEqual(401, response.status_code)

    def test_case_2_resend_code(self):
        """ Fail - User does not exists """
        send_data = json.dumps({
            "email": "test123456@stevens.edu"
        })
        response = self.app.post('http://127.0.0.1:4000/auth/resend', headers={"Content-Type": "application/json"}, data=send_data)
        self.assertEqual(401, response.status_code)

