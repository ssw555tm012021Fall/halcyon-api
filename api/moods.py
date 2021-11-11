import re
from server import bcrypt
from data.mood_activity import mood_activity
from flask import g, request, make_response, jsonify
from flask.views import MethodView
from jinja2 import Environment, FileSystemLoader
from shared.authorize import authorize
from service.moods_service import get_moods
from service.employee_service import set_isdepressed

class MoodsAPI(MethodView):
    @authorize
    def get(self):
        """ 
            Retrieve Moods list
            return: Moods   {List}
        """

        try:
            mood_activities = get_moods()
            responseObject = {
                'status': 'success',
                'questions': mood_activities
            }
            return make_response(jsonify(responseObject)), 200
                
        except Exception as e:
            responseObject = {
                'status': 'fail',
                'message': 'Some error occurred. Please try again.',
                'error': repr(e)
            }
            return make_response(jsonify(responseObject)), 400

class IsdepressedAPI(MethodView):
    @authorize
    def put(self):
        """
            Set employee is_depressed
        """
        try:
            post_data = request.get_json()
            employee_id = g.user.id
            isDepressed = post_data.get('isDepressed')
            set_isdepressed(employee_id, isDepressed)
            responseObject = {
                'status': 'success'
            }
            return make_response(jsonify(responseObject)), 200

        except Exception as e:
            responseObject = {
                'status': 'fail',
                'message': 'Error in updating isDepressed!',
                'error': str(e)
            }
            return make_response(jsonify(responseObject)), 400

# define the API resources
moods_view = MoodsAPI.as_view('MoodsAPI')
isdepressed_view = IsdepressedAPI.as_view('isdepressedAPI')

