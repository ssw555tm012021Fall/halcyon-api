from functools import wraps
from flask import g, request, make_response, jsonify, url_for
from data.employee import Employee
from service.employee_service import get_employee_by_id

def authorize(f):
    @wraps(f)
    def decorated_function(*args, **kws):
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
                g.user = get_employee_by_id(id=resp)
                return f(*args, **kws)
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

    return decorated_function
