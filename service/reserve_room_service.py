from sqlalchemy_cockroachdb import run_transaction

from data.db import session, sessionmaker
from data.reservation import Reservation
from data.room import Room
from service.room_service import get_room_details
import datetime

def get_meditatoin_room_by_id(id):
    return session.query(Room).filter(Room.id == id).first()


def get_reservation_by_id(id):
    return session.query(Reservation).filter(Reservation.id == id).first()


def get_room_reserved_by_id(id):
    return session.query(Room).filter(Room.id == id).first()


def get_reservation(meditation_room_id, date_reservation, start_time, end_time):
    return session.query(Reservation).filter(Reservation.meditation_room_id == meditation_room_id,
                                             Reservation.date_reservation == date_reservation,
                                             Reservation.start_time == start_time,
                                             Reservation.end_time == end_time
                                             ).first()


def add_reservation(reservation):
    session.add(reservation)
    session.commit()


def add_reservation_return_id(reservation):
    session.add(reservation)
    session.commit()
    session.refresh(reservation)
    return reservation


def add_reservation_in_txn(reservation):
    return run_transaction(sessionmaker, lambda sess: sess.add(reservation))


def add_room_reserved(room_reserved):
    session.add(room_reserved)
    session.commit()


def add_room_reserved_return_id(room_reserved):
    session.add(room_reserved)
    session.commit()
    session.refresh(room_reserved)
    return room_reserved


def add_room_reserved_in_txn(room_reserved):
    return run_transaction(sessionmaker, lambda sess: sess.add(room_reserved))

def get_room_employee_id(id):
    today = datetime.datetime.now().date()
    now_time = datetime.datetime.now().time()
    employee_reservation = session.query(Reservation).filter(Reservation.employee_id == id,
    Reservation.date_reservation == today, Reservation.start_time > now_time).first()
    if employee_reservation is not None:
        room = get_room_details(Reservation.meditation_room_id)
        reservation_details = []
        reservation_map = {}
        reservation_map['employee_id'] = employee_reservation.employee_id
        reservation_map['date_reservation'] = employee_reservation.date_reservation.strftime("%Y-%m-%d")
        reservation_map['start_time'] = employee_reservation.start_time.strftime("%H:%M")
        reservation_map['end_time'] = employee_reservation.end_time.strftime("%H:%M")
        reservation_map['room_name'] = room.room_name
        reservation_map['description'] = room.description
        reservation_details.append(reservation_map)
        return reservation_details
    return None
