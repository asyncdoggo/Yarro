import datetime

import flask
import jwt
from flask import current_app
from flask import request
from flask_restful import Resource
from markupsafe import escape

import app.db as db
from app.api.token_required import token_required

active_tokens = {}


class Login(Resource):
    def get(self):
        try:
            token = request.cookies.get("token")
            data = jwt.decode(
                token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = db.Users.query.filter_by(
                id=data['id']).one_or_none()

            if current_user.disabled:
                return {"status": "disabled"}

            if not current_user.confirmed:
                return {"status": "email"}
            if active_tokens[current_user.username] == token:
                return {"status": "success","uname": current_user.username,"uid": current_user.id}

            return {"status": "false"}

        except Exception as e:
            print(repr(e))
            return {"status": "failure"}

    def post(self):
        auth = request.authorization
        if not auth or not auth.username or not auth.password:
            return {"status": "failure"}

        try:
            user = db.check_login(auth.username, auth.password)
            if user:
                token = jwt.encode(
                    {'id': user.id, 'exp': datetime.datetime.utcnow() +
                     datetime.timedelta(hours=8000)},
                    current_app.config['SECRET_KEY'], "HS256")
                active_tokens[user.username] = token
                response = flask.make_response(
                    {"status": "success", "uname": escape(user.username), "uid": user.id})
                response.set_cookie("token", token, httponly=False, secure=True,
                                    samesite="None", expires=datetime.datetime.utcnow() + datetime.timedelta(hours=8000))
                return response

            return {"status": "username or password is incorrect"}

        except Exception as e:
            print(repr(e))
            return {"status": "failure"}


class Logout(Resource):
    @token_required
    def post(self, user):
        try:
            active_tokens.pop(user.username)
        except KeyError:
            pass
        response = flask.make_response({"status": "success"})
        response.delete_cookie("token")
        return response
