from sqlalchemy_cockroachdb import run_transaction

# from data.db import session, sessionmaker
from data.reservation import Reservation
from data.room import Room
from server import db
from service.room_service import get_room_details
import datetime

def get_meditatoin_room_by_id(id):
    return db.session.query(Room).filter(Room.id == id).first()


def get_reservation_by_id(id):
    return db.session.query(Reservation).filter(Reservation.id == id).first()


def get_room_reserved_by_id(id):
    return db.session.query(Room).filter(Room.id == id).first()


def get_reservation(meditation_room_id, date_reservation, start_time, end_time):
    return db.session.query(Reservation).filter(Reservation.meditationRoomId == meditation_room_id,
                                             Reservation.date == date_reservation,
                                             Reservation.startTime == start_time,
                                             Reservation.endTime == end_time
                                             ).first()


def add_reservation(reservation):
    db.session.add(reservation)
    db.session.commit()


def add_reservation_return_id(reservation):
    db.session.add(reservation)
    db.session.commit()
    db.session.refresh(reservation)
    return reservation


def add_reservation_in_txn(reservation):
    return run_transaction(db.sessionmaker, lambda sess: sess.add(reservation))


def add_room_reserved(room_reserved):
    db.session.add(room_reserved)
    db.session.commit()


def add_room_reserved_return_id(room_reserved):
    db.session.add(room_reserved)
    db.session.commit()
    db.session.refresh(room_reserved)
    return room_reserved


def add_room_reserved_in_txn(room_reserved):
    return run_transaction(db.sessionmaker, lambda sess: sess.add(room_reserved))

def get_room_employee_id(id):
    today = datetime.datetime.now().date()
    now_time = datetime.datetime.now().time()
    employee_reservation = db.session.query(Reservation).filter(Reservation.employeeId == id,
                                                             Reservation.date == today, Reservation.startTime > now_time).first()
    if employee_reservation is not None:
        room = get_room_details(Reservation.meditationRoomId)
        reservation_details = []
        reservation_map = {}
        reservation_map['employeeId'] = employee_reservation.employeeId
        reservation_map['date'] = employee_reservation.date.strftime("%Y-%m-%d")
        reservation_map['startTime'] = employee_reservation.startTime.strftime("%H:%M")
        reservation_map['endTime'] = employee_reservation.endTime.strftime("%H:%M")
        reservation_map['room_name'] = room.room_name
        reservation_map['description'] = room.description
        reservation_details.append(reservation_map)
        return reservation_details
    return None
