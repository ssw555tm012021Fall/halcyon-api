from data.db import session
from data.reminder import Reminder
from shared.common import is_dirty


def get_reminders_for_employee(employeeId):
    """
        Get list of reminders for specified employee id
        """
    return session.query(Reminder).filter(Reminder.employeeId == employeeId).all()


def get_reminder_for_employee_and_type(employeeId, type):
    """
        Get reminder for specified employee id and type
        """
    return session.query(Reminder).filter(Reminder.employeeId == employeeId).filter(Reminder.type == type.value).first()


def add_reminder_return_id(reminder):
    session.add(reminder)
    session.commit()
    session.refresh(reminder)
    return reminder


def update_reminder(reminder):
    if is_dirty(reminder):
        session.commit()
    return reminder
