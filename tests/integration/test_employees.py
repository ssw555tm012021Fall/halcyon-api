import json

from tests.TestBase import TestBase


class EmployeeTest(TestBase):
    def test_successful_login(self):
        email = "viyeta@gmail.com"
        password = "password"
        payload = json.dumps({
            "email": email,
            "password": password
        })
        response = self.app.post('/auth/login', headers={"Content-Type": "application/json"}, data=payload)

        self.assertEqual(str, type(response.json['auth_token']))
        self.assertEqual(200, response.status_code)
