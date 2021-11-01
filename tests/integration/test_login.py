import time
import json
import unittest
from datetime import datetime

from tests.TestBase import TestBase

def register_user(self, email, password):
    return self.client.post(
        '/auth/register',
        data=json.dumps(dict(
            email=email,
            password=password
        )),
        content_type='application/json',
    )

def login_user(self, email, password):
    return self.client.post(
        '/auth/login',
        data=json.dumps(dict(
            email=email,
            password=password
        )),
        content_type='application/json',
    )


class TestAuthBlueprint(TestBase):
    def test_registered_user_login(self):
        """ Test for login of registered-user login """
        with self.client:
            # user registration
            resp_register = register_user(self, 'testuser1@stevens.edu', 'Password@123')
            data_register = json.loads(resp_register.data.decode())
            # self.assertTrue(data_register['status'] == 'success')
            # self.assertTrue(
            #     data_register['message'] == 'Successfully registered.'
            # )
            # self.assertTrue(data_register['auth_token'])
            # self.assertTrue(resp_register.content_type == 'application/json')
            # self.assertEqual(resp_register.status_code, 201)
            # registered user login
            response = login_user(self, 'testuser1@stevens.edu', 'Password@123')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully logged in.')
            self.assertTrue(data['auth_token'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()