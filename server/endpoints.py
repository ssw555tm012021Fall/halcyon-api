from flask import Blueprint

from api.auth import registration_view, login_view, user_view, logout_view, confirmation_view, resend_view
from api.rooms import room_available_time_view, reserve_room_view, reservation_update_view, reservation_delete_view, \
    show_rooms_view, reservation_view

from api.sounds import sounds_view, play_sounds_view

from api.goals import set_goal_view

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
# Room
blueprints.add_url_rule(
    '/rooms/<roomId>',
    view_func=room_available_time_view,
    methods=['GET']
)
blueprints.add_url_rule(
    '/rooms',
    view_func=show_rooms_view,
    methods=['GET']
)
blueprints.add_url_rule(
    '/rooms/reservation',
    view_func=reservation_view,
    methods=['POST']
)

# Reservations
blueprints.add_url_rule(
    '/reserve-room',
    view_func=reserve_room_view,
    methods=['POST']
)
blueprints.add_url_rule(
    '/reservation/<reservationId>',
    view_func=reservation_update_view,
    methods=['PUT']
)
blueprints.add_url_rule(
    '/reservation/<reservationId>',
    view_func=reservation_delete_view,
    methods=['DELETE']
)

# sounds 
blueprints.add_url_rule(
    '/sounds',
    view_func=sounds_view,
    methods=['GET']
)
blueprints.add_url_rule(
    '/sounds/<soundId>',
    view_func=play_sounds_view,
    methods=['GET']
)

blueprints.add_url_rule(
    '/set-goal',
    view_func=set_goal_view,
    methods=['POST']
)
