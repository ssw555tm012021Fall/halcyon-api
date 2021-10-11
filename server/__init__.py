# server/__init__.py

from flask import Flask, jsonify
from flask_bcrypt import Bcrypt
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = 'your_super_secret_key'

# app_settings = os.getenv(
#     'APP_SETTINGS',
#     'server.config.DevelopmentConfig'
# )
# app.config.from_object(app_settings)

bcrypt = Bcrypt(app)
BCRYPT_LOG_ROUNDS = 12

from server.endpoints import blueprints
app.register_blueprint(blueprints)


@app.route("/")
def route_health():
    return jsonify({
        "health": True
    })


@app.route("/test")
def test():
    return "Works!"
