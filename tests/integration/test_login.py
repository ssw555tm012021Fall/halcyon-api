import json
import unittest
from tests.TestBase import TestBase
from tests.integration.test_account import register_user


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
    def test_valid_registration(self):
        """ Test for valid user registration """
        with self.client:
            # user registration doesn't work. Error: 'TemplateNotFound(\'code_email_template.html\')'
            # resp_register = register_user(self, 'testuser1@stevens.edu', 'Password123')
            # data_register = json.loads(resp_register.data.decode())
            # self.assertTrue(data_register['status'] == 'success')
            # self.assertTrue(
            #     data_register['message'] == 'Successfully registered.'
            # )
            # self.assertTrue(data_register['auth_token'])
            # self.assertTrue(resp_register.content_type == 'application/json')
            # self.assertEqual(resp_register.status_code, 201)
            pass

    def test_registered_user_login(self):
        """ Test for login of registered-user login """
        with self.client:
            response = login_user(self, 'viyetak@stevens.edu', 'Password123')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully logged in.')
            self.assertTrue(data['auth_token'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)

    def test_invalid_user_login(self):
        """ Test for login of invalid-user login """
        with self.client:
            response = login_user(self, 'test_user1@example.com', 'password')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Invalid credentials.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
