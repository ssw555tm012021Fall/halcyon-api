# server/__init__.py

from flask import Flask, jsonify
from flask_bcrypt import Bcrypt
from flask_cors import CORS
import urllib.request
import shutil

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


@app.before_first_request
def _download_cert():
    url = 'https://cockroachlabs.cloud/clusters/9c750309-b4c4-482e-92ef-8b1521cf223f/cert'
    file_name = 'root.crt'
    with urllib.request.urlopen(url) as response, open(file_name, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)


@app.route("/")
def route_health():
    return jsonify({
        "health": True
    })


@app.route("/test")
def test():
    return "Works!"
