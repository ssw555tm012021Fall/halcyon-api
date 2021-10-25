from flask import g, make_response, jsonify, request
from flask.views import MethodView
from sqlalchemy.sql.expression import false


from service.set_goals import update_goal, get_goal_by_id, add_goal, add_goal_return_id
from data.goals import Goals
from shared.authorize import authorize


class SetGoalsAPI(MethodView):
    """
    User Reservations
    """
    def post(self):
        # get the post data
        post_data = request.get_json()
        # get employee data
        target = int(post_data.get('target'))

        if target > 0 or target is not None:
            try:
                if target < 0:
                    responseObject = {
                        'status': 'fail',
                        'message': 'The target should not be less than zero.'
                    }
                    return make_response(jsonify(responseObject)), 401

                new_goal = Goals(
                    target = target,
                    employee_id = g.user.id
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


set_goal_view = SetGoalsAPI.as_view('set_goal_api')
