import datetime
from functools import wraps
from flask import current_app, request
import flask
from flask_restful import Resource
import jwt
from app import db
from markupsafe import escape

def admin_token_required(f):
    """
    token_required(f) decorator will validate a token f and return the Admin Class object defined in
    modules/Database. token is accessed from cookie with name token
    """

    @wraps(f)
    def decorator(*args, **kwargs):

        token = request.cookies.get("token")

        if not token:
            return {'message': 'a valid token is missing'},403

        try:
            data = jwt.decode(
                token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = db.Admin.query.filter_by(id=data['id']).one_or_none()
            if not current_user:
                return "unauthorized",403
        except jwt.ExpiredSignatureError:
            return {'status': 'expired'},403
        except jwt.DecodeError:
            return {"status": "invalid"},403

        return f(*args, current_user, **kwargs)

    return decorator


class AdminUserList(Resource):
    @admin_token_required
    def get(self, _):
        user = flask.request.args.get("user", default="")
        sort = flask.request.args.get("sort", default=0)

        users = db.get_users(user, sort)

        return {"status":"success","users":users}




class AdminAuth(Resource):
    def post(self):
        auth = request.authorization
        if not auth or not auth.username or not auth.password:
            return {"status": "failure"}

        try:
            admin = db.admin_login(auth.username, auth.password)
            if admin:
                token = jwt.encode(
                    {'id': admin.id, 'exp': datetime.datetime.utcnow() +
                     datetime.timedelta(hours=8000)},
                    current_app.config['SECRET_KEY'], "HS256")
                response = flask.make_response(
                    {"status": "success", "uname": escape(admin.username), "uid": admin.id})
                response.set_cookie("token", token, httponly=True, secure=True,
                                    samesite="Strict", expires=datetime.datetime.utcnow() + datetime.timedelta(hours=8000))
                return response
            else:
                return {"status": "username or password is incorrect"}

        except Exception:
            return {"status": "failure"}



class AdminUser(Resource):
    @admin_token_required
    def get(self,_,username):
        user = db.get_user(username=username)
        if user:
            return {"status":"success","username":user.username,"email":user.email,"confirmed":user.confirmed,"created_at":user.created_at,"id":user.id,"disabled":user.disabled}
        return {"status": "user not found"}
    
    
    @admin_token_required
    def delete(self,_, uid):
        if db.disable_user(uid):
            return {"status": "success"}
        return {"status": "failure"}
