import json

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


def confirm_user(self, email, code):
    return self.client.post(
        '/auth/Confirmation',
        data=json.dumps(dict(
            email=email,
            code=code
        )),
        content_type='application/json',
    )


def resend_code(self, email):
    return self.client.post(
        '/auth/resend',
        data=json.dumps(dict(
            email=email
        )),
        content_type='application/json',
    )


class AccountTestCases(TestBase):

    def test_case_1_signup(self):
        """ Fail signup gmail account """
        response = register_user(self, 'felkourdi@gmail.com', 'Ff@1234567')
        self.assertEqual(202, response.status_code)

    def test_case_2_signup(self):
        """ Fail signup weak password """
        response = register_user(self, 'farahelkourdi95@stevens.edu', '1234')
        self.assertEqual(401, response.status_code)
        
    def test_case_3_signup(self):
        """ Fail signup account exists"""
        response = register_user(self, 'viyetak@stevens.edu', 'Ff1234567891')
        self.assertEqual(202, response.status_code)

    def test_case_1_confirmation_code(self):
        """ Fail confirmation code - account is active """
        response = confirm_user(self, 'viyetak@stevens.edu', '82319')
        self.assertEqual(401, response.status_code)

    def test_case_2_confirmation_code(self):
        """ Fail confirmation code - wrong code """
        response = confirm_user(self, 'viyetak@stevens.edu', '82319')
        self.assertEqual(401, response.status_code)

    def test_case_3_confirmation_code(self):
        """ User does not exist """
        response = confirm_user(self, 'test12345@stevens.edu', '82319')
        self.assertEqual(401, response.status_code)

    def test_case_1_resend_code(self):
        """ Fail - Account is already active """
        response = resend_code(self, 'viyetak@stevens.edu')
        self.assertEqual(401, response.status_code)

    def test_case_2_resend_code(self):
        """ Fail - User does not exists """
        response = resend_code(self, 'test123456@stevens.edu')
        self.assertEqual(401, response.status_code)

