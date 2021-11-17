from flask import g, make_response, jsonify, request
from flask.views import MethodView
from sqlalchemy.sql.expression import false
import time, datetime


from service.award_service import add_award_return_id, add_employee_award_return_id
from data.award import Awards
from data.employee_award import EmployeeAward

from shared.authorize import authorize


class SetAwardsAPI(MethodView):
    """
    User Reservations
    """
    @authorize
    def post(self):
        # get the post data
        post_data = request.get_json()
        # get employee data
        title = post_data.get('title')
        description = post_data.get('description')
        target = int(post_data.get('target'))
        category = post_data.get('category')
        frequency = post_data.get('frequency')
        image = post_data.get('category', "")


        if target > 0 or target is not None or category is not None or frequency is not None :
            try:
                if target < 0:
                    responseObject = {
                        'status': 'fail',
                        'message': 'The target should not be less than zero.'
                    }
                    return make_response(jsonify(responseObject)), 401

                created_at = datetime.datetime.now()
                give_award = Awards(
                    title=title, description=description,
                    target=target,
                    image=image,
                    category=category,
                    frequency=frequency,
                    created_at=created_at)
                award = add_award_return_id(give_award)
                employee_award = add_employee_award_return_id(EmployeeAward(
                    employee_id=g.user.id,
                    award_id=award.id,
                    created_at=created_at
                ))
                if award.id is None or employee_award.id is None:
                    responseObject = {
                        'status': 'success',
                        'message': 'Award could not be given'
                    }
                    return make_response(jsonify(responseObject)), 201

                else:
                    responseObject = {
                        'status': 'success',
                        'award_id': award.id,
                        "employee_award_id": employee_award.id
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




awards_view = SetAwardsAPI.as_view('awards_api')
