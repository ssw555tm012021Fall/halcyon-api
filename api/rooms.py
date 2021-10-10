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
        for room_map in room_availability_map_list:
            room_map['start_time'] = room_map['start_time'].strftime("%H:%M:%S")
            room_map['end_time'] = room_map['end_time'].strftime("%H:%M:%S")
        responseObject = {
            'status': 'success',
            'available_rooms': room_availability_map_list
        }
        return make_response(jsonify(responseObject)), 200

room_available_time_view = RoomAvailabilityAPI.as_view('room_availability')

class RoomReserved(MethodView):
    """
    User Resource
    """
    from service.reserve_room_service import get_reservation, get_meditatoin_room_by_id, get_room_reserved_by_id, get_reservation_by_id, add_room_reserved_return_id, add_reservation_return_id

    def post(self):
        # get auth token
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''

        if auth_token:
            resp = Reservation.decode_auth_token(auth_token)
            if isinstance(resp, str):
                post_data = request.get_json()

                meditation_room_id = post_data.get('meditation_room_id')
                employee_id = post_data.get('employee_id')
                date = post_data.get('date')
                start_time = post_data.get('start_time')
                end_time = post_data.get('end_time')
                try:
                    reservation = get_reservation(meditation_room_id, date, start_time, end_time)

                    if reservation is None:
                        new_reservation = Reservation(
                            meditation_room_id = meditation_room_id,
                            employee_id=employee_id,
                            date_reservation = date,
                            start_time = start_time,
                            end_time = end_time
                        )
                        new_reservation = add_reservation_return_id(new_reservation)
                        add_room_reserved_return_id(Rooms(meditation_room_id=int(meditation_room_id), reservation_id=int(new_reservation.id)))
                        responseObject = {
                        'status': 'success',
                        'message': 'Reservation created'
                        }
                        return make_response(jsonify(responseObject)), 200
                    else:
                        responseObject = {
                        'status': 'success',
                        'message': 'Room is already reserved'
                        }
                        return make_response(jsonify(responseObject)), 200
                except Exception as e:
                    responseObject = {
                        'status': 'fail',
                        'message': e
                    }
                    return make_response(jsonify(responseObject)), 202
            else:
                responseObject = {
                    'status': 'fail',
                    'message': resp
                }
                return make_response(jsonify(responseObject)), 401
        else:
            responseObject = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return make_response(jsonify(responseObject)), 403