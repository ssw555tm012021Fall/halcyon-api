from sqlalchemy_cockroachdb import run_transaction

from data.db import session, sessionmaker
from data.reservation import Reservation
from data.room import Room


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
