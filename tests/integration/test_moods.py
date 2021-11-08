import unittest
import json
from tests.TestBase import TestBase
from tests.integration.test_login import login_user

def get_moods(self, auth_token):
    return self.client.get(
        '/moods/activities',
        data=None,
        headers=dict(
            Authorization='Bearer ' + auth_token
        ),
        content_type='application/json',
    )


class MoodsTestCases(TestBase):
    def test_moods(self):
        """ Sucessful """
        with self.client:
            login_data = json.loads(login_user(self, 'viyetak@stevens.edu', 'Password123').data.decode())
            response = get_moods(self, login_data['auth_token'])
            data = json.loads(response.data.decode())
            self.assertEqual(200, response.status_code)

