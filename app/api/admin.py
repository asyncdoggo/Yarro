import datetime
from functools import wraps
from flask import current_app, request, jsonify
import flask
from flask_restful import Resource
import jwt
from app import db
import app.db as db
from app.api.token_required import token_required


def admin_token_required(f):
    """
    token_required(f) decorator will validate a token f and return the User Class object defined in
    modules/Database. token is accessed from cookie with name token
    """

    @wraps(f)
    def decorator(*args, **kwargs):

        token = request.cookies.get("token")

        if not token:
            return jsonify({'message': 'a valid token is missing'})

        try:
            data = jwt.decode(
                token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = db.Admin.query.filter_by(id=data['id']).first()
        except jwt.ExpiredSignatureError:
            return jsonify({'status': 'expired'})
        except jwt.DecodeError:
            return jsonify({"status": "invalid"})

        return f(*args, current_user, **kwargs)

    return decorator


class AdminUsers(Resource):
    @admin_token_required
    def get(self, _):
        user = flask.request.args.get("user", default="")
        sort = flask.request.args.get("sort", default=0)

        db.get_users(user, sort)

    def delete(self, uid):
        if db.delete_user(uid):
            pass


class Admin(Resource):
    # login admin
    def post(self):
        auth = request.authorization
        if not auth or not auth.username or not auth.password:
            return jsonify({"status": "failure"})

        try:
            admin = db.admin_login(auth.username, auth.password)
            if admin:
                token = jwt.encode(
                    {'id': admin.id, 'exp': datetime.datetime.utcnow() +
                     datetime.timedelta(hours=8000)},
                    current_app.config['SECRET_KEY'], "HS256")
                response = flask.make_response(
                    {"status": "success", "uname": flask.escape(admin.username), "uid": admin.id})
                response.set_cookie("token", token, httponly=True, secure=True,
                                    samesite="Strict", expires=datetime.datetime.utcnow() + datetime.timedelta(hours=8000))
                return response
            else:
                return jsonify({"status": "username or password is incorrect"})

        except Exception:
            return jsonify({"status": "failure"})
