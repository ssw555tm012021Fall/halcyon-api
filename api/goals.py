from flask import g, make_response, jsonify, request
from flask.views import MethodView
from sqlalchemy.sql.expression import false
import time, datetime


from service.set_goals import update_goal, get_goal_by_id, add_goal, add_goal_return_id, delete_goal
from data.goals import Goals
from data.events import Events, Event_State

from service.events_service import add_event_return_id, add_event, get_event_by_id
from data.goals import Goals

from shared.authorize import authorize


class SetGoalsAPI(MethodView):
    """
    User Reservations
    """
    @authorize
    def post(self):
        # get the post data
        post_data = request.get_json()
        # get employee data
        target = int(post_data.get('target'))
        category = post_data.get('category')
        frequency = post_data.get('frequency')


        if target > 0 or target is not None or category is not None or frequency is not None :
            try:
                if target < 0:
                    responseObject = {
                        'status': 'fail',
                        'message': 'The target should not be less than zero.'
                    }
                    return make_response(jsonify(responseObject)), 401


                new_goal = Goals(
                    target = target,
                    employee_id = g.user.id,
                    frequency = frequency,
                    category = category,
                    created_at = datetime.datetime.now()
                )
                goal = add_goal_return_id(new_goal)
                if goal is None:
                    responseObject = {
                        'status': 'success',
                        'message': 'Goal could not be set'
                    }
                    return make_response(jsonify(responseObject)), 201

                else:
                    responseObject = {
                        'status': 'success',
                        'goal_id': goal.id
                    }
                    return make_response(jsonify(responseObject)), 200

            except Exception as e:
                responseObject = {
                    'status': 'fail',
                    'message': 'Some error occurred. Please try again.',
                    'error': repr(e)
                }
                return make_response(jsonify(responseObject)), 401
        else:
            responseObject = {
                'status': 'fail',
                'message': 'Error, user does not exist.',
            }
            return make_response(jsonify(responseObject)), 401



class CheckGoalsAPI(MethodView):
    """
    User Reservations
    """
    @authorize
    def post(self):
        # get the post data
        post_data = request.get_json()
        # get employee data
        goal_id = int(post_data.get('goal_id'))
        current_progress = int(post_data.get('current_progress'))
        if goal_id is not None:
            try:
                goal = get_goal_by_id(goal_id)
                target = goal.target
                message = "Goal not achieved"
                if current_progress >= target:
                    message = "Goal Achieved"
                    delete_goal(goal_id)
                    event = Events(
                        employee_id=g.user.id,
                        state=Event_State.completed,
                        length=target,
                        category=goal.category,
                        created_at=goal.created_at
                    )
                    add_event(event)

                if goal_id is None:
                    responseObject = {
                        'status': 'error',
                        'message': 'Please provide goal id'
                    }
                    return make_response(jsonify(responseObject)), 201

                else:
                    responseObject = {
                        'status': 'success',
                        'message': message
                    }
                    return make_response(jsonify(responseObject)), 200

            except Exception as e:
                print(e)
                responseObject = {
                    'status': 'fail',
                    'message': 'Some error occurred. Please try again.',
                    'error': repr(e)
                }
                return make_response(jsonify(responseObject)), 401
        else:
            responseObject = {
                'status': 'fail',
                'message': 'Error, user does not exist.',
            }
            return make_response(jsonify(responseObject)), 401


set_goal_view = SetGoalsAPI.as_view('set_goal_api')
check_goal_view = CheckGoalsAPI.as_view('check_goal_api')
