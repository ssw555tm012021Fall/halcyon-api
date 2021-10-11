import re
import datetime
from shared.common import send_email, generate_code, check_password
from server import bcrypt
from data.employee import Employee
from data.code_confirmation import code_confirmation
from service.employee_service import get_employee_by_email, add_employee, get_employee_by_id, add_employee_return_id
from service.employee_service import activate_account
from service.code_confirmation_service import add_code_confirmation, get_code_confirmation_by_employee_id, update_code
from flask import g, request, make_response, jsonify
from flask.views import MethodView
from datetime import date
from jinja2 import Environment, FileSystemLoader
from sqlalchemy.sql.expression import false
from shared.authorize import authorize
from service.reserve_room_service import get_reservation, get_meditatoin_room_by_id, get_room_reserved_by_id, get_reservation_by_id, add_room_reserved_return_id, add_reservation_return_id



class RegisterAPI(MethodView):
    """
    User Registration Resource 
    Added by: FR7 ~ Farah Elkourdi
    """

    def post(self):
        # get the post data
        post_data = request.get_json()
        # check if user already exists
        employee = get_employee_by_email(post_data.get('email'))
        if not employee:
            try:
                user_email = post_data.get('email')

                # email validation (added by kavish)
                pattern = re.compile(
                    "^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|((stevens\.edu)))$")
                if not pattern.match(user_email):
                    responseObject = {
                        'status': 'fail',
                        'message': 'Invalid email',
                    }
                    return make_response(jsonify(responseObject)), 202
                # end 

                user_pass = post_data.get('password')
                if (user_pass is not None and not check_password(user_pass)):
                    responseObject = {
                        'status': 'fail',
                        'message': 'Password length should be greater or equal to 8, include one capital \
                     letter, one small letter, and one number.'
                    }
                    return make_response(jsonify(responseObject)), 401

                employee = Employee(
                    email=user_email,
                    password=user_pass,
                    is_confirmed=False,
                    first_name='User',
                    last_name='User',
                    birthday="1990-01-01",
                    gender='f'
                )
                # insert the employee
                saved_employee = add_employee_return_id(employee)

                # random verification_code
                code_ints = generate_code()

                code = code_confirmation(
                    employee_id=saved_employee.id,
                    code=code_ints,
                    expiry_date=date.today(),
                    code_confirmation_time=datetime.datetime.now().time()
                )

                # insert the code_confirmation
                add_code_confirmation(code)

                # generate the auth token
                auth_token = employee.encode_auth_token(employee.id)
                responseObject = {
                    'status': 'success',
                    'message': 'Successfully registered.',
                    'auth_token': auth_token
                }

                # send email 
                templateLoader = FileSystemLoader(searchpath="./template/")
                templateEnv = Environment(loader=templateLoader)
                TEMPLATE_FILE = "code_email_template.html"
                template = templateEnv.get_template(TEMPLATE_FILE)
                output = template.render(user_name=saved_employee.first_name, code=code_ints)
                send_email(saved_employee.email, output)

                return make_response(jsonify(responseObject)), 201
            except Exception as e:
                responseObject = {
                    'status': 'fail',
                    'message': 'Some error occurred. Please try again.',
                    'error': repr(e)
                }
                return make_response(jsonify(responseObject)), 401
        else:
            responseObject = {
                'status': 'fail',
                'message': 'User already exists. Please Log in.',
            }
            return make_response(jsonify(responseObject)), 202


class LoginAPI(MethodView):
    """
    User Login Resource
    """

    def post(self):
        # get the post data
        post_data = request.get_json()
        try:
            # fetch the user data
            employee = get_employee_by_email(
                email=post_data.get('email')
            )
            if employee and bcrypt.check_password_hash(
                    employee.password, post_data.get('password')
            ):
                auth_token = employee.encode_auth_token(employee.id)
                if auth_token:
                    responseObject = {
                        'status': 'success',
                        'message': 'Successfully logged in.',
                        'auth_token': auth_token
                    }
                    return make_response(jsonify(responseObject)), 200
            else:
                responseObject = {
                    'status': 'fail',
                    'message': 'User does not exist.'
                }
                return make_response(jsonify(responseObject)), 404
        except Exception as e:
            responseObject = {
                'status': 'fail',
                'message': 'Try again',
                'error': repr(e)
            }
            return make_response(jsonify(responseObject)), 500


class UserAPI(MethodView):
    """
    User Resource
    This demonstrates how the @authorize decorator works
    Just place this decorator in request method to authorize the request

    g.user is Employee object so g.user.id is Employee.id
    """

    @authorize
    def get(self):
        responseObject = {
            'status': 'success',
            'data': {
                'user_id': g.user.id,
                'email': g.user.email
            }
        }
        return make_response(jsonify(responseObject)), 200


class LogoutAPI(MethodView):
    """
    Logout Resource
    """

    def post(self):
        # get auth token
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''
        if auth_token:
            resp = Employee.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                # TODO: mark the token as blacklisted
                try:
                    responseObject = {
                        'status': 'success',
                        'message': 'Successfully logged out.'
                    }
                    return make_response(jsonify(responseObject)), 200
                except Exception as e:
                    responseObject = {
                        'status': 'fail',
                        'message': e
                    }
                    return make_response(jsonify(responseObject)), 200
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


class ConfirmationAPI(MethodView):
    """
    Activate account
    Added by : FR7 
    """

    def post(self):
        # get the post data
        post_data = request.get_json()
        # get employee data 
        employee = get_employee_by_email(post_data.get('email'))
        if employee is not None:
            try:
                # get employee code 
                code = get_code_confirmation_by_employee_id(employee.id)

                # account already activated 
                if employee.is_confirmed == True:
                    responseObject = {
                        'status': 'fail',
                        'message': 'The account is already activated.'
                    }
                    return make_response(jsonify(responseObject)), 401

                # compare codes
                if code.code != post_data.get('code'):
                    responseObject = {
                        'status': 'fail',
                        'message': 'Error, code not matched.'
                    }
                    return make_response(jsonify(responseObject)), 401

                    # check if code is still available < 24 hours
                get_code_datetime = str(code.expiry_date) + " " + code.code_confirmation_time.strftime("%H:%M")
                confirmation_datetime = datetime.datetime.strptime(get_code_datetime, "%Y-%m-%d %H:%M")
                now_datetime = datetime.datetime.now()
                difference = now_datetime - confirmation_datetime
                if difference.days != 0:
                    responseObject = {
                        'status': 'fail',
                        'message': 'Error, code is available for 24 hours only.'
                    }
                    return make_response(jsonify(responseObject)), 401

                # activate account
                activate_account(employee.email)

                # generate the auth token
                auth_token = employee.encode_auth_token(employee.id)
                responseObject = {
                    'status': 'success',
                    'message': 'Successfully activated.',
                    'auth_token': auth_token,
                }
                return make_response(jsonify(responseObject)), 201
            except Exception as e:
                responseObject = {
                    'status': 'fail',
                    'message': 'Some error occurred. Please try again.',
                    'error': repr(e)
                }
                return make_response(jsonify(responseObject)), 401
        else:
            responseObject = {
                'status': 'fail',
                'message': 'Error, User does not exist.',
            }
            return make_response(jsonify(responseObject)), 401


class ResendAPI(MethodView):
    """
    Resend verification code
    Added by : FR7 
    """

    def post(self):
        # get the post data
        post_data = request.get_json()
        # get employee data 
        employee = get_employee_by_email(post_data.get('email'))
        if employee is not None:
            try:
                if employee.is_confirmed == True:
                    responseObject = {
                        'status': 'fail',
                        'message': 'The account is already activated.'
                    }
                    return make_response(jsonify(responseObject)), 401

                # get employee code 
                code = get_code_confirmation_by_employee_id(employee.id)
                new_code = generate_code()
                update_code(code.id, new_code)

                # send
                templateLoader = FileSystemLoader(searchpath="./template/")
                templateEnv = Environment(loader=templateLoader)
                TEMPLATE_FILE = "code_email_template.html"
                template = templateEnv.get_template(TEMPLATE_FILE)
                output = template.render(user_name=employee.first_name, code=new_code)
                send_email(employee.email, output)

                # generate the auth token
                auth_token = employee.encode_auth_token(employee.id)
                responseObject = {
                    'status': 'success',
                    'message': 'Successfully resend.',
                    'auth_token': auth_token,
                }
                return make_response(jsonify(responseObject)), 201
            except Exception as e:
                responseObject = {
                    'status': 'fail',
                    'message': 'Some error occurred. Please try again.',
                    'error': repr(e)
                }
                return make_response(jsonify(responseObject)), 401
        else:
            responseObject = {
                'status': 'fail',
                'message': 'Error, user does not exist.',
            }
            return make_response(jsonify(responseObject)), 401


# define the API resources
registration_view = RegisterAPI.as_view('register_api')
login_view = LoginAPI.as_view('login_api')
user_view = UserAPI.as_view('user_api')
logout_view = LogoutAPI.as_view('logout_api')
confirmation_view = ConfirmationAPI.as_view('confirmation_api')
resend_view = ResendAPI.as_view('resend_api')
