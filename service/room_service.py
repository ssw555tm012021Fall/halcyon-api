from datetime import timedelta, datetime, time

from data.db import session
from data.reservation import Reservation
from data.room import Room
from shared.common import is_dirty


def get_room_by_id(room_id):
    """ get Room object searched from primary key """
    return session.query(Room).get(room_id)


def generate_room_times(room, today):
    """
        Generate the time slots for specified room based on
        supplied date and startTime, endTime, interval in minutes from Room object.
        Time slots will have full date-time details
        Parameters:
                room (Room): Room object
                today (datetime.date): Only date part without time
        Returns:
                array of 2d arrays:
                [[startTime, endTime]]
        """
    time_delta = timedelta(minutes=room.time_interval)
    start_date_time = datetime.combine(today, room.start_available_time)
    end_date_time = datetime.combine(today, room.end_available_time)
    time_slots = [[dt, dt + time_delta] for dt in
                  date_time_range_delta(start_date_time, end_date_time, time_delta)]
    return time_slots


def date_time_range_delta(start, end, delta):
    """
        Generator for getting start time for each slot based on start, end and time delta
        """
    current = start
    while current < end:
        yield current
        current += delta


def get_room_bookings(room, date_reservation):
    """
        Get list of reservations based on room and date of the reservation
        """
    return session.query(Reservation).filter(Reservation.meditationRoomId == room.id).filter(
        Reservation.date == date_reservation).all()


def get_room_availability_map(room, date_reservation):
    """
        Generate the list of dictionaries with all the time slots of room on supplied date with availability.
        First we will get all the possible slots for the room and then we will check it against registration.
        Whichever slots are available/bookable will have available: True else False
        Parameters:
                room (Room): Room object
                date_reservation (datetime.date): Only date part without time
        Returns:
                array of dictionary:
                {available: bool, endTime: str, startTime: bool}
        """
    time_slots = generate_room_times(room, date_reservation)
    current_bookings = get_room_bookings(room, date_reservation)
    room_availability_map_list = []
    for slot in time_slots:
        room_availability_map = {}
        for booking in current_bookings:
            if slot[0].time() == booking.startTime and slot[1].time() == booking.endTime:
                room_availability_map['available'] = False
                break
        if 'available' not in room_availability_map:
            room_availability_map['available'] = True
        room_availability_map['startTime'] = slot[0]
        room_availability_map['endTime'] = slot[1]
        room_availability_map_list.append(room_availability_map)
    return room_availability_map_list


def is_time_conflict(room, date, start_time, end_time):
    """
        Check if there is a time conflict for the room on specified interval (startTime - endTime)
        Parameters:
                room (Room): Room object
                date (datetime.date): date on which availability has to be checked
                start_time (datetime.time): start time of the required slot
                end_time (datetime.time): end time of the required slot
        Returns:
                bool: True if the slot can be booked for that room else False
        """
    room_availability_map_list = get_room_availability_map(room, date)
    for room_availability_map in room_availability_map_list:
        if room_availability_map['startTime'].time() == start_time \
                and room_availability_map['endTime'].time() == end_time:
            return False
    return True


def get_reservation_by_id(reservation_id):
    """ get Reservation object searched from primary key """
    return session.query(Reservation).get(reservation_id)


def get_reservation_by_id_and_employee_id(reservation_id, employee_id):
    """ get Reservation object searched from primary key and employeeId """
    return session.query(Reservation).filter(
        Reservation.id == reservation_id).filter(Reservation.employeeId == employee_id).first()


def get_reservation_by_room_id_and_employee_id(room_id, employee_id):
    """ get Reservation object searched from room id, employeeId and today's date"""
    return session.query(Reservation).filter(
        Reservation.meditationRoomId == room_id).filter(Reservation.employeeId == employee_id).filter(
        Reservation.date == datetime.date(datetime.today())).first()


def get_reservation(meditation_room_id, date_reservation, start_time, end_time):
    return session.query(Reservation).filter(Reservation.meditationRoomId == meditation_room_id,
                                             Reservation.date == date_reservation,
                                             Reservation.startTime == start_time,
                                             Reservation.endTime == end_time
                                             ).first()


def get_reservation_all_fields(employee_id, meditation_room_id, date_reservation, start_time, end_time):
    return session.query(Reservation).filter(Reservation.employeeId == employee_id,
                                             Reservation.meditationRoomId == meditation_room_id,
                                             Reservation.date == date_reservation,
                                             Reservation.startTime == start_time,
                                             Reservation.endTime == end_time
                                             ).first()


def update_reservation(reservation):
    if is_dirty(reservation):
        conflicting_reservation = get_reservation(reservation.meditationRoomId, reservation.date,
                                                  reservation.startTime, reservation.endTime)
        if conflicting_reservation:
            raise ValueError("Conflicting reservation error")
        else:
            session.commit()
    return reservation


def get_rooms():
    rooms = session.query(Room).all()
    room_list = []
    for room in rooms:
        room_map = {}
        room_map['id'] = room.id
        room_map['room_name'] = room.room_name
        room_map['description'] = room.description
        room_map['time_interval'] = room.time_interval
        room_map['start_available_time'] = room.start_available_time.strftime("%H:%M")
        room_map['end_available_time'] = room.end_available_time.strftime("%H:%M")
        room_list.append(room_map)
    return room_list


def get_room_details(room_id):
    room = session.query(Room).filter(Room.id == room_id).first()
    return room


def delete_reservation(reservation):
    session.delete(reservation)
    session.commit()
