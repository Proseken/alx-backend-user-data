#!/usr/bin/env python3
"""Session Auth View"""

from api.v1.views import app_views
from flask import request, jsonify, abort
from models.user import User
import os


SESSION_NAME = os.getenv('SESSION_NAME')


@app_views.route('/auth_session/login', methods=['POST'],
                 strict_slashes=False)
def session_auth_login():
    """POST /api/v1/auth_session/login"""
    attrs = ['email', 'password']
    for attr in attrs:
        if any([request.form.get(attr) is None,
                request.form.get(attr) == '']):
            return jsonify({'error': attr + ' missing'}), 400

    users = User.search({attrs[0]: request.form.get(attrs[0])})
    if len(users) == 0:
        return jsonify({"error": "no user found for this email"}), 404
    for user in users:
        if user.is_valid_password(request.form.get(attrs[1])):
            from api.v1.app import auth
            session_id = auth.create_session(user.id)
            response = jsonify(user.to_json())
            response.set_cookie(SESSION_NAME, session_id)
            return response
    return jsonify({"error": "wrong password"}), 401


@app_views.route('/api/v1/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def session_auth_logout():
    """DELETE /api/v1/auth_session/logout"""
    from api.v1.app import auth
    if not auth.destroy_session(request):
        abort(404)
    return jsonify({}), 200
