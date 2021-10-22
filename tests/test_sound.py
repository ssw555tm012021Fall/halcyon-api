import unittest
from flask import app
from app import app
import  json
from data.employee import Employee
from service.employee_service import get_employee_by_email
#import request

class SoundsTestCases(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
       

    def test_case_1(self):
        """ Sucessful """
        emp = get_employee_by_email('viyeta@gmail.com')
        access_token = emp.encode_auth_token(emp.id)
        headers = {
            'Authorization': 'Bearer {}'.format(access_token)
        } 
        data_pass = json.dumps(dict(type='sound'))
        response = self.app.get('http://127.0.0.1:4000/sounds', headers=headers, data=data_pass,content_type='application/json')
        self.assertEqual(200, response.status_code)
        data_pass = json.dumps(dict(type='guide'))
        response = self.app.get('http://127.0.0.1:4000/sounds', headers=headers, data=data_pass,content_type='application/json')
        self.assertEqual(200, response.status_code)
 

    
