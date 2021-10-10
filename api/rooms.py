from datetime import datetime

from flask import make_response, jsonify
from flask.views import MethodView

from service.room_service import get_room_by_id, generate_room_times, get_room_availability_map
from shared.authorize import authorize


class RoomAvailabilityAPI(MethodView):
    """

    """
    @authorize
    def get(self, roomId = 0):
        room = get_room_by_id(roomId)
        if not room:
            responseObject = {
                'status': 'fail',
                'message': 'Room not found!'
            }
            return make_response(jsonify(responseObject)), 401
        room_availability_map_list = get_room_availability_map(room, datetime.date(datetime.today()))
        responseObject = {
            'status': 'success',
            'available_rooms': room_availability_map_list
        }
        return make_response(jsonify(responseObject)), 200


room_available_time_view = RoomAvailabilityAPI.as_view('room_availability')