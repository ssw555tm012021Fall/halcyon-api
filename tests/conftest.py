from datetime import datetime

import pytest
from server import app
from data.employee import Employee


@pytest.fixture(scope='module')
def new_employee():
    today = datetime.today()
    employee = Employee('viyeta@gmail.com', 'password', '', False, '', today, 'f')
    return employee


@pytest.fixture(scope='module')
def test_client():
    flask_app = app

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        # Establish an application context
        with flask_app.app_context():
            yield testing_client  # this is where the testing happens!


@pytest.fixture(scope='function')
def login_default_user(test_client):
    test_client.post('/login',
                     data=dict(email='viyeta@gmail.com', password='password'),
                     follow_redirects=True)

    yield  # this is where the testing happens!

    test_client.get('/logout', follow_redirects=True)
