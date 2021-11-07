from data.reminder import Reminder
from server import db
from shared.common import is_dirty


def get_reminders_for_employee(employeeId):
    """
        Get list of reminders for specified employee id
        """
    return db.session.query(Reminder).filter(Reminder.employeeId == employeeId).all()


def get_reminder_for_employee_and_type(employeeId, type):
    """
        Get reminder for specified employee id and type
        """
    return db.session.query(Reminder).filter(Reminder.employeeId == employeeId).filter(Reminder.type == type.value).first()


def add_reminder_return_id(reminder):
    db.session.add(reminder)
    db.session.commit()
    db.session.refresh(reminder)
    return reminder


def update_reminder(reminder):
    if is_dirty(reminder):
        db.session.commit()
    return reminder
