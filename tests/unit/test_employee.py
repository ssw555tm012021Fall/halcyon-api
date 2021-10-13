from datetime import datetime

from data.employee import Employee
from server import bcrypt


def test_new_employee():
    """
    GIVEN a Employee model
    WHEN a new Employee is created
    THEN check the email and hashed_password are defined correctly
    """
    today = datetime.today()
    employee = Employee('viyeta@gmail.com', 'FlaskIsAwesome', '', False, '', today, 'f')
    assert employee.email == 'viyeta@gmail.com'
    assert employee.password != 'FlaskIsAwesome'
    assert employee.birthday == today


def test_employee_password():
    employee = Employee('viyeta@gmail.com', 'FlaskIsAwesome', '', False, '', datetime.today(), 'f')
    assert bcrypt.check_password_hash(
        employee.password, 'FlaskIsAwesome')
