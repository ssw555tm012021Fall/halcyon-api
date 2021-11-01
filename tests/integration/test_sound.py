import unittest
import json
from tests.TestBase import TestBase
from tests.helper import create_sound2
from tests.integration.test_login import login_user


def get_sounds(self, auth_token, sound_type):
    return self.client.get(
        '/sounds',
        data=json.dumps(dict(
            type=sound_type
        )),
        headers=dict(
            Authorization='Bearer ' + auth_token
        ),
        content_type='application/json',
    )


def get_sound(self, auth_token, sound_id):
    return self.client.get(
        ('/sounds' + '/' + sound_id),
        headers=dict(
            Authorization='Bearer ' + auth_token
        ),
        content_type='application/json',
    )


class SoundsTestCases(TestBase):
    def test_case_list_sounds(self):
        """ Sucessful """
        with self.client:
            login_data = json.loads(login_user(self, 'viyetak@stevens.edu', 'Password123').data.decode())
            response = get_sounds(self, login_data['auth_token'], 'sound')
            data = json.loads(response.data.decode())
            self.assertEqual(200, response.status_code)
            response = get_sounds(self, login_data['auth_token'], 'guide')
            data = json.loads(response.data.decode())
            self.assertEqual(200, response.status_code)

    def test_case_sounds_1(self):
        """ Sucessful """
        login_data = json.loads(login_user(self, 'viyetak@stevens.edu', 'Password123').data.decode())
        sound = create_sound2()
        response = get_sound(self, login_data['auth_token'], str(sound.id))
        self.assertEqual(200, response.status_code)

    def test_case_sounds_2(self):
        """ fail sound not found """
        login_data = json.loads(login_user(self, 'viyetak@stevens.edu', 'Password123').data.decode())
        response = get_sound(self, login_data['auth_token'], '222222222222')
        self.assertEqual(404, response.status_code)

