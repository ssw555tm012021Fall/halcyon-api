import re
from server import bcrypt
from data.sound import Sound
from flask import g, request, make_response, jsonify
from flask.views import MethodView
from jinja2 import Environment, FileSystemLoader
from shared.authorize import authorize
from service.sound_service import get_file_by_id, get_files


class SoundsAPI(MethodView):
    """
    Retrieve sound file
    """
    @authorize
    def get(self):
        # get the post data
        post_data = request.get_json()
        # retrieve all {type} files
        try:
            sound_files = get_files(post_data.get('type'))
            if sound_files is not None:
                responseObject = {
                    'status': 'success',
                    'sounds': sound_files
                }
                return make_response(jsonify(responseObject)), 200
            else:
                responseObject = {
                    'status': 'fail',
                    'message': 'No data found.',
                }
                return make_response(jsonify(responseObject)), 202

        except Exception as e:
            responseObject = {
                'status': 'fail',
                'message': 'Some error occurred. Please try again.',
                'error': repr(e)
            }
            return make_response(jsonify(responseObject)), 400



# define the API resources
sounds_view = SoundsAPI.as_view('sound_api')

