import re
from server import bcrypt
from data.sound import Sound
from flask import g, request, make_response, jsonify
from flask.views import MethodView
from jinja2 import Environment, FileSystemLoader
from shared.authorize import authorize
from service.sound_service import get_file_by_id, get_files



class SoundsAPI(MethodView):
    @authorize
    def get(self):
        """ 
            Retrieve sounds list
            parameters: sound type {string}
            return: sounds   {List}
        """
        post_data = request.get_json()
        # retrieve all {type} files
        try:
            sound_files = get_files(post_data.get('type'))
            responseObject = {
                'status': 'success',
                'sounds': sound_files
            }
            return make_response(jsonify(responseObject)), 200
                
        except Exception as e:
            responseObject = {
                'status': 'fail',
                'message': 'Some error occurred. Please try again.',
                'error': repr(e)
            }
            return make_response(jsonify(responseObject)), 400

class PlaysoundAPI(MethodView):
    @authorize
    def get(self, soundId=0):
        """ 
            Fetch sound 
            parameters: Sound ID {INT}
            return: Sound details   {List}
        """
        try:
            sound = get_file_by_id(soundId)
            responseObject = {
                'status': 'success',
                'sound': sound
            }
            return make_response(jsonify(responseObject)), 200

        except (TypeError, AttributeError):
                responseObject = {
                    'status': 'fail',
                    'message': 'sound not found!'
                }
                return make_response(jsonify(responseObject)), 404

        except Exception as e:
            responseObject = {
                'status': 'fail',
                'message': 'Some error occurred. Please try again.',
                'error': repr(e)
            }
            return make_response(jsonify(responseObject)), 400

# define the API resources
sounds_view = SoundsAPI.as_view('sound_api')
play_sounds_view = PlaysoundAPI.as_view('play_sound_api')


