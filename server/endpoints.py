from flask import Blueprint

from api.auth import registration_view, login_view, user_view, logout_view, confirmation_view, resend_view

blueprints = Blueprint('auth', __name__)

# add Rules for API Endpoints
blueprints.add_url_rule(
    '/auth/register',
    view_func=registration_view,
    methods=['POST']
)
blueprints.add_url_rule(
    '/auth/login',
    view_func=login_view,
    methods=['POST']
)
blueprints.add_url_rule(
    '/auth/status',
    view_func=user_view,
    methods=['GET']
)
blueprints.add_url_rule(
    '/auth/logout',
    view_func=logout_view,
    methods=['POST']
)
blueprints.add_url_rule(
    '/auth/Confirmation',
    view_func=confirmation_view,
    methods=['POST']
)
blueprints.add_url_rule(
    '/auth/resend',
    view_func=resend_view,
    methods=['POST']
)