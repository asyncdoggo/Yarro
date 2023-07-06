from flask import request, jsonify
from flask_restful import Resource
from app import db
import app.db as db
from app.api.token_required import token_required

class AdminData(Resource):
    @token_required
    def get(self,user):
        if user.username == "admin" and user.id == "admin":
            pass
    

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
            user = db.admin_login(auth.username, auth.password)
            if user:
                token = jwt.encode(
                    {'id': user.id, 'exp': datetime.datetime.utcnow() +
                     datetime.timedelta(hours=8000)},
                    current_app.config['SECRET_KEY'], "HS256")
                active_tokens[user.username] = token
                response = flask.make_response(
                    {"status": "success", "uname": flask.escape(user.username), "uid": user.id})
                response.set_cookie("token", token, httponly=True, secure=True,
                                    samesite="Strict", expires=datetime.datetime.utcnow() + datetime.timedelta(hours=8000))
                return response
            else:
                return jsonify({"status": "username or password is incorrect"})

        except Exception:
            return jsonify({"status": "failure"})