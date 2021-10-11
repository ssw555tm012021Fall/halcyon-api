from datetime import timedelta, datetime, time

from data.db import session
from data.reservation import Reservation
from data.room import Room


def get_room_by_id(room_id):
    return session.query(Room).get(room_id)


def generate_room_times(room, today):
    time_delta = timedelta(minutes=room.time_interval)
    start_date_time = datetime.combine(today, room.start_available_time)
    end_date_time = datetime.combine(today, room.end_available_time)
    time_slots = [[dt, dt + time_delta] for dt in
                  date_time_range_delta(start_date_time, end_date_time, time_delta)]
    return time_slots


def date_time_range_delta(start, end, delta):
    current = start
    while current <= end:
        yield current
        current += delta


def get_room_bookings(room, date_reservation):
    return session.query(Reservation).filter(Reservation.meditation_room_id == room.id).filter(
        Reservation.date_reservation == date_reservation).all()


def get_room_availability_map(room, date_reservation):
    time_slots = generate_room_times(room, datetime.date(datetime.today()))
    current_bookings = get_room_bookings(room, date_reservation)
    room_availability_map_list = []
    for slot in time_slots:
        room_availability_map = {}
        for booking in current_bookings:
            if slot[0].time() == booking.start_time and slot[1].time() == booking.end_time:
                room_availability_map['available'] = False
                break
        if 'available' not in room_availability_map:
            room_availability_map['available'] = True
        room_availability_map['start_time'] = slot[0]
        room_availability_map['end_time'] = slot[1]
        room_availability_map_list.append(room_availability_map)
    return room_availability_map_list
