from server import bcrypt
from data.employee import Employee
from data.code_confirmation import code_confirmation
from service.employee_service import get_employee_by_email, add_employee, get_employee_by_id, add_employee_return_id
from service.code_confirmation_service import add_code_confirmation
from flask import request, make_response, jsonify
from flask.views import MethodView
import re
import random 
import datetime
from datetime import date
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from smtplib import SMTP 
from jinja2 import Environment, FileSystemLoader

class RegisterAPI(MethodView):
    """
    User Registration Resource
    """
    def send_email(user_email, user_name, user_code):
        sender_email = "ssw555.halcyon@gmail.com"
        password = "SSW555team1"
        receiver_email = user_email
        message = MIMEMultipart("alternative")
        message["Subject"] = "Account activation"
        message["From"] = sender_email
        message["To"] = receiver_email
        templateLoader = FileSystemLoader(searchpath="./template/")
        templateEnv = Environment(loader=templateLoader)
        TEMPLATE_FILE = "email_template.html"
        template = templateEnv.get_template(TEMPLATE_FILE)
        output = template.render(user_name= user_name, code= user_code )
        message.attach(MIMEText(output, "html"))
        msgBody = message.as_string()
        server = SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msgBody)

    def post(self):
        # get the post data
        post_data = request.get_json()

        # email validation constraint - by kavish
        pattern = re.compile("^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|((stevens\.edu)))$")
        if pattern.match(post_data.get('email')):
            responseObject = {
                'status': 'fail',
                'message': 'Invalid email',
            }
            return make_response(jsonify(responseObject)), 202
        # end 
    
        # check if user already exists
        employee = get_employee_by_email(post_data.get('email'))
        if not employee:
            try:
                # check password
                user_pass=post_data.get('password')
                if (user_pass is not None and not RegisterAPI.check_password(user_pass)):
                    responseObject = {
                    'status': 'fail',
                    'message': 'Password length should be greater or equal to 8, at least one capital \
                     letter, one small letter and one number.'
                    }
                    return make_response(jsonify(responseObject)), 401      

                employee = Employee(
                    email=post_data.get('email'),
                    password=user_pass,
                    is_confirmed = False,
                    first_name = 'User',
                    last_name = 'User',
                    birthday = "1990-01-01",
                    gender = 'f'
                )
                # insert the employee
                saved_employee = add_employee_return_id(employee)

                # generate random verification_code
                code_ints = ''.join(random.sample('0123456789', 5))

                code = code_confirmation(
                    employee_id= saved_employee.id,
                    code= code_ints,
                    expiry_date = date.today(),
                    code_confirmation_time = datetime.datetime.now().time()
                )
                # insert the code_confirmation
                add_code_confirmation(code)

                # send email 
                RegisterAPI.send_email(saved_employee.email, saved_employee.first_name, code_ints)

                # generate the auth token
                auth_token = employee.encode_auth_token(employee.id)
                responseObject = {
                    'status': 'success',
                    'message': 'Successfully registered.',
                    'auth_token': auth_token
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
                'message': 'User already exists. Please Log in.',
            }
            return make_response(jsonify(responseObject)), 202

    def check_password (user_pass):
        if (len(user_pass)<8):
            flag = False
        elif not re.search("[a-z]", user_pass):
            flag = False
        elif not re.search("[A-Z]", user_pass):
            flag = False
        elif not re.search("[0-9]", user_pass):
            flag = False
        else:
            flag = True          
        return flag

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
    """

    def get(self):
        # get the auth token
        auth_header = request.headers.get('Authorization')
        if auth_header:
            try:
                auth_token = auth_header.split(" ")[1]
            except IndexError:
                responseObject = {
                    'status': 'fail',
                    'message': 'Bearer token malformed.'
                }
                return make_response(jsonify(responseObject)), 401
        else:
            auth_token = ''
        if auth_token:
            resp = Employee.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                user = get_employee_by_id(id=resp)
                responseObject = {
                    'status': 'success',
                    'data': {
                        'user_id': user.id,
                        'email': user.email
                    }
                }
                return make_response(jsonify(responseObject)), 200
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
            return make_response(jsonify(responseObject)), 401


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


# define the API resources
registration_view = RegisterAPI.as_view('register_api')
login_view = LoginAPI.as_view('login_api')
user_view = UserAPI.as_view('user_api')
logout_view = LogoutAPI.as_view('logout_api')
