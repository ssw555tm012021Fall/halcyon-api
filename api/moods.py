import re
from server import bcrypt
from data.mood_activity import mood_activity
from flask import g, request, make_response, jsonify
from flask.views import MethodView
from jinja2 import Environment, FileSystemLoader
from shared.authorize import authorize
from service.moods_service import get_moods


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

# define the API resources
moods_view = MoodsAPI.as_view('MoodsAPI')


