from datetime import datetime

from flask import g, make_response, jsonify, request
from flask.views import MethodView

from data.personality_options import PersonalityOptions, OptionValue
from data.personality_questions import PersonalityQuestions
from data.reminder import Reminder, ReminderType
from service.personality_questions_service import get_all_questions, get_all_options, add_question, add_options, \
    get_all_questions_with_options, get_question_with_options
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

            response_questions = get_all_questions_with_options()

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

    @authorize
    def post(self):
        """
        Helper method to add questions and options to database.
        This feature is not needed for front-end integration.
        """
        try:
            post_data = request.get_json()

            personality_question = PersonalityQuestions(post_data.get('content'), post_data.get('index'))
            personality_question = add_question(personality_question)

            request_options = post_data.get('options')
            personality_question_options = []
            for request_option in request_options:
                # if not isinstance(request_option.get('value'), OptionValue):
                #     responseObject = {
                #         'status': 'fail',
                #         'message': 'Invalid option value supplied!'
                #     }
                #     return make_response(jsonify(responseObject)), 400
                option = PersonalityOptions(personality_question.id, request_option.get('content'),
                                            request_option.get('index'), request_option.get('value'))
                personality_question_options.append(option)

            add_options(personality_question_options)

            responseObject = {
                'status': 'success',
                'question': get_question_with_options(personality_question.id)
            }
            return make_response(jsonify(responseObject)), 200

        except Exception as e:
            responseObject = {
                'status': 'fail',
                'message': 'Error in adding question!',
                'error': str(e)
            }
            return make_response(jsonify(responseObject)), 400


get_personality_questions_view = PersonalityTestAPI.as_view('get_personality_test')
