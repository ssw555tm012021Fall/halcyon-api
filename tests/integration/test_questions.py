import unittest
import json
from tests.TestBase import TestBase
from tests.helper import create_sound2
from tests.integration.test_login import login_user


def get_questions(self, auth_token):
    return self.client.get(
        '/personality/questions',
        data=None,
        headers=dict(
            Authorization='Bearer ' + auth_token
        ),
        content_type='application/json',
    )


class PersonalityQuestionsTestCases(TestBase):

    def test_list_questions(self):
        """ Sucessful """
        with self.client:
            login_data = json.loads(login_user(self, 'viyetak@stevens.edu', 'Password123').data.decode())
            response = get_questions(self, login_data['auth_token'])
            data = json.loads(response.data.decode())
            self.assertEqual(200, response.status_code)
            self.assertEqual(len(data['questions']), 1)
            self.assertEqual('At a party do you', data['questions'][0]['content'])
            self.assertEqual(len(data['questions'][0]['options']), 2)
            self.assertEqual('Interact with many, including strangers', data['questions'][0]['options'][0]['content'])
