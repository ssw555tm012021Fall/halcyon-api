from datetime import datetime

from flask import g, make_response, jsonify, request
from flask.views import MethodView

from data.reminder import Reminder, ReminderType
from service.personality_questions_service import get_all_questions, get_all_options
from service.reminder_service import get_reminders_for_employee, get_reminder_for_employee_and_type, \
    add_reminder_return_id, update_reminder

from shared.authorize import authorize


class PersonalityTestAPI(MethodView):
    @authorize
    def get(self):
        """
            Get questions and options with values associated with each option
            Returns:
                    array of questions with array of options with values:
                    {List[PersonalityQuestions]}
            """
        try:
            questions = get_all_questions()
            options = get_all_options()

            if not questions or len(questions) == 0:
                responseObject = {
                    'status': 'fail',
                    'message': 'No questions found!'
                }
                return make_response(jsonify(responseObject)), 404

            response_questions = []
            for question in questions:
                question_dict = {}
                question_options = []
                for option in options:
                    if option.questionId == question.id:
                        question_options.append(option.serialize())

                question_dict['id'] = question.id
                question_dict['content'] = question.content
                question_dict['index'] = question.index
                question_dict['options'] = question_options

                response_questions.append(question_dict)

            responseObject = {
                'status': 'success',
                'questions': response_questions
            }
            return make_response(jsonify(responseObject)), 200
        except Exception as e:
            responseObject = {
                'status': 'fail',
                'message': 'Error in fetching questions!',
                'error': str(e)
            }
            return make_response(jsonify(responseObject)), 400


get_personality_questions_view = PersonalityTestAPI.as_view('get_personality_test')
