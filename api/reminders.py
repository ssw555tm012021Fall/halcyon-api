from datetime import datetime

from flask import g, make_response, jsonify, request
from flask.views import MethodView

from data.reminder import Reminder, ReminderType
from service.reminder_service import get_reminders_for_employee, get_reminder_for_employee_and_type, \
    add_reminder_return_id, update_reminder

from shared.authorize import authorize


class RemindersAPI(MethodView):
    @authorize
    def get(self):
        """
            Get types and specs of reminders for the logged in employee
            Returns:
                    array of reminders:
                    {List[Reminder]}
            """
        try:
            reminders = get_reminders_for_employee(g.user.id)

            if not reminders or len(reminders) == 0:
                responseObject = {
                    'status': 'fail',
                    'message': 'No reminders found!'
                }
                return make_response(jsonify(responseObject)), 404

            responseObject = {
                'status': 'success',
                'reminders': [e.serialize() for e in reminders]
            }
            return make_response(jsonify(responseObject)), 200
        except Exception as e:
            responseObject = {
                'status': 'fail',
                'message': 'Error in fetching reminders!',
                'error': str(e)
            }
            return make_response(jsonify(responseObject)), 400

    @authorize
    def put(self):
        """
            Update reminder for employee
            """
        try:
            post_data = request.get_json()

            employee_id = g.user.id
            type = ReminderType(post_data.get('type'))

            if not isinstance(type, ReminderType):
                responseObject = {
                    'status': 'fail',
                    'message': 'Invalid type supplied!'
                }
                return make_response(jsonify(responseObject)), 400

            startAt = datetime.strptime(post_data.get('startAt'), '%H:%M:%S').time()
            endAt = datetime.strptime(post_data.get('endAt'), '%H:%M:%S').time()
            interval = post_data.get('interval')

            reminder = get_reminder_for_employee_and_type(employee_id, type)

            if not reminder:
                reminder = Reminder(employee_id, startAt, endAt, type, interval)
                reminder = add_reminder_return_id(reminder)
            else:
                reminder.startAt = startAt
                reminder.endAt = endAt
                reminder.interval = interval
                update_reminder(reminder)

            responseObject = {
                'status': 'success',
                'reminder': reminder.serialize()
            }
            return make_response(jsonify(responseObject)), 200
        except Exception as e:
            responseObject = {
                'status': 'fail',
                'message': 'Error in updating reminder!',
                'error': str(e)
            }
            return make_response(jsonify(responseObject)), 400


get_reminders_view = RemindersAPI.as_view('get_reminders')
