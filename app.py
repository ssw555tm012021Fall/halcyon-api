from flask import Flask, jsonify, request

from data.auth import sign_in, sign_up

app = Flask(__name__)

@app.route("/")
def route_health():
    return jsonify({
        "health": True
    })

@app.route("/signup", methods = ['POST'])
def route_sign_up():
    """In here is the data from the form"""
    content = request.json
    email = content['email']
    password = content['password'];

    return jsonify({
        "success": sign_up(email, password),
        "email": email,
        "password": password
    })

@app.route("/signin", methods = ['POST'])
def route_sign_in():
    """In here is the data from the form"""
    content = request.json
    email = content['email']
    password = content['password'];

    return jsonify({
        "success": sign_in(email, password),
        "email": email,
        "password": password
    })

app.run(debug=True, port=4000)