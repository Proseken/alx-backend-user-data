#!/usr/bin/env python3
"""A simple python flask application module"""

from flask import (
    Flask, jsonify, request,
    abort, make_response, redirect, url_for)
from auth import Auth

app = Flask(__name__)
app.url_map.strict_slashes = False
AUTH = Auth()


@app.route('/', methods=['GET'])
def index_page() -> str:
    """6. Basic Flask app"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def user() -> str:
    """Create new user in database"""
    attrs = ['email', 'password']
    data = {}
    for attr in attrs:
        if attr in request.form:
            data.update({attr: request.form.get(attr)})
        else:
            return jsonify({"message": "Bad request!"}), 400
    try:
        user = AUTH.register_user(**data)
        return jsonify({"email": user.email,
                        "message": "user created"}), 201
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'])
def login():
    """The mines of Moria: Simply Login"""
    attrs = ['email', 'password']
    data = {}
    for attr in attrs:
        if attr in request.form:
            data.update({attr: request.form.get(attr)})
        else:
            return jsonify({"message": "Bad request!"}), 400
    if AUTH.valid_login(**data):
        session_id = AUTH.create_session(data.get('email'))
        resp = make_response(
            jsonify({"email": data.get('email'),
                     "message": "logged in"})
        )
        resp.set_cookie('session_id', session_id)
        return resp
    abort(401)


@app.route('/sessions', methods=['DELETE'])
def logout():
    """The Red Pill: Exit the Matrix"""
    session_id = request.cookies.get('session_id', None)
    if not AUTH.get_user_from_session_id(session_id):
        abort(403)
    AUTH.destroy_session(session_id)
    return redirect(url_for('index_page'))


@app.route('/profile', methods=['GET'])
def profile():
    """Fetch User profile from session_id"""
    session_id = request.cookies.get('session_id', None)
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    return jsonify({"email": user.email})


@app.route('/reset_password', methods=['POST'])
def get_reset_password_token():
    """You want back in to the Matrix?"""
    attrs = ['email']
    data = {}
    for attr in attrs:
        if attr in request.form:
            data.update({attr: request.form.get(attr)})
        else:
            return jsonify({"message": "Bad request!"}), 400
    try:
        reset_token = AUTH.get_reset_password_token(
            email=data.get('email')
        )
        return jsonify({"email": data.get('email'),
                        "reset_token": reset_token})
    except ValueError:
        abort(403)


@app.route('/reset_password', methods=['PUT'])
def update_password():
    """19. Update password end-point"""
    attrs = ['email', 'reset_token', 'new_password']
    data = {}
    for attr in attrs:
        if attr in request.form:
            data.update({attr: request.form.get(attr)})
        else:
            return jsonify({"message": "Bad request!"}), 400
    try:
        AUTH.update_password(reset_token=data.get('reset_token'),
                             password=data.get('new_password'))
        return jsonify({"email": data.get('email'),
                        "message": "Password updated"})
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
