from datetime import datetime

from flask import g, make_response, jsonify, request
from flask.views import MethodView

from service.room_service import get_room_by_id, generate_room_times, get_room_availability_map, get_reservation, \
    update_reservation, get_reservation_all_fields, get_reservation_by_id
from shared.authorize import authorize

class RoomAvailabilityAPI(MethodView):
    @authorize
    def get(self, roomId=0):
        """
            Returns the availability of provided room id.
            Needs auth token in request header
            start and end time will be in format: HH:MM:SS (24 hours)
            Parameters:
                    roomId (int): primary key of Room
            Returns:
                    array of dictionary:
                    {available: bool, end_time: str, start_time: bool}
            """
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
            'time_slots': room_availability_map_list
        }
        return make_response(jsonify(responseObject)), 200

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


class ReservationUpdateAPI(MethodView):
    @authorize
    def put(self, reservationId=0):
        """
            Updates the reservation with provided details. First availability should be checked and then update
            Parameters:
                    reservationId (int): primary key of Room
            Returns:
                    updated reservation object
            """
        reservation = get_reservation_by_id(reservationId)
        # room = get_room_by_id(roomId)
        if not reservation:
            responseObject = {
                'status': 'fail',
                'message': 'Reservation not found!'
            }
            return make_response(jsonify(responseObject)), 401

        post_data = request.get_json()

        meditation_room_id = post_data.get('meditation_room_id')
        start_time = datetime.strptime(post_data.get('start_time'), '%H:%M:%S').time()
        end_time = datetime.strptime(post_data.get('end_time'), '%H:%M:%S').time()
        date_reservation = datetime.date(datetime.today())

        try:
            if reservation is None:
                responseObject = {
                    'status': 'fail',
                    'message': 'Reservation not found!'
                }
                return make_response(jsonify(responseObject)), 401
            else:
                reservation.employee_id = g.user.id
                reservation.meditation_room_id = meditation_room_id
                reservation.date_reservation = date_reservation
                reservation.start_time = start_time
                reservation.end_time = end_time

                updated_reservation = update_reservation(reservation)
                responseObject = {
                    'status': 'success',
                    'message': 'Reservation updated'
                    # 'reservation': updated_reservation
                }
                return make_response(jsonify(responseObject)), 200

        except Exception as e:
            responseObject = {
                'status': 'fail',
                'message': 'There is a conflict in booking the room!',
                'error': str(e)
            }
            return make_response(jsonify(responseObject)), 409


room_available_time_view = RoomAvailabilityAPI.as_view('room_availability')
reservation_update_view = ReservationUpdateAPI.as_view('reservation_update')
