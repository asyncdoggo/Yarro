import datetime
import os
import re
import uuid
from functools import wraps

import flask
import jwt
from flask import request, jsonify, url_for, send_from_directory
from jwt import ExpiredSignatureError, DecodeError
from werkzeug.utils import secure_filename
import app.Database as Data
from app.send_mail import send_mail
from flask_restful import Resource

from flask import current_app

active_tokens = {}

email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
username_regex = r"^\w(?:\w|[.-](?=\w)){3,31}$"
password_regex = r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$"


def token_required(f):
    """
    token_required(f) decorator will validate a token f and return the User Class object defined in
    modules/Database. token should be sent through HTTP header 'x-access-tokens'
    """

    @wraps(f)
    def decorator(*args, **kwargs):

        token = request.cookies.get("token")

        if not token:
            return jsonify({'message': 'a valid token is missing'})

        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = Data.User.query.filter_by(id=data['id']).first()

            if not current_user.confirmed:
                return {"status": "email"}
        except ExpiredSignatureError:
            return jsonify({'status': 'expired'})
        except DecodeError:
            return jsonify({"status": "invalid"})

        return f(*args, current_user, **kwargs)

    return decorator


class SearchUser(Resource):
    @token_required
    def get(self, _):
        try:
            user = request.args.get("user")
            users = Data.search(user)
            return {"status": "success", "data": users}
        except Exception as e:
            print(e)
            return {"status": "failure"}


class FullnameBio(Resource):
    @token_required
    def get(self, _):
        try:
            user = request.args.get("user")
            name, bio = Data.get_fullname_bio(user)
            return {"status": "success", "name": name, "bio": bio}
        except Exception as e:
            print(repr(e))
            return {"status": "failure"}


class Image(Resource):
    def get(self, path):
        path = secure_filename(path)
        image_file = os.path.join(flask.current_app.root_path, "static", "userimages", path)
        image_folder = os.path.join(flask.current_app.root_path, "static", "userimages")
        if not os.path.exists(image_file):
            path = "default"
        return send_from_directory(image_folder, path)

    @token_required
    def post(self, user):
        try:
            file = request.files["image"]
            filename = secure_filename(user.username)

            file.save(os.path.join(flask.current_app.root_path, "static", "userimages", filename))
            return {"status": "success"}
        except KeyError as e:
            print(e)
            return {"status": "failure"}


class UserDetails(Resource):
    @token_required
    def get(self, user):
        try:
            ret = Data.getuserdetials(user.id)
            return {"status": "success", "data": ret}
        except Exception as e:
            print(repr(e))
            return jsonify({"subject": "failure"})

    @token_required
    def put(self, user):
        try:
            data = request.get_json()
            name = data["name"]
            gender = data["gender"]
            mob = data["mob"]
            dob = data["dob"]
            bio = data["bio"][0:254]

            if not dob:
                dob = "0000-00-00"
                age = 0
            else:
                age = get_years(dob)

            if not mob:
                mob = 0

            u = Data.update(name=name, age=age, gender=gender, mob=mob,
                            dob=datetime.datetime.strptime(dob, "%Y-%m-%d").date(), uid=user.id, bio=bio)
            if u == mob:
                return {"status": "mob"}
            elif u:
                return {"status": "success"}
            else:
                return {"status": "failure"}
        except KeyError:
            return {"status": "logout"}


class Like(Resource):
    @token_required
    def get(self, user):
        try:
            res = Data.getlikedata(user)
            return {"status": "success", "data": res}
        except Exception:
            return {"status", "success"}

    @token_required
    def post(self, user):
        try:
            data = request.get_json()
            pid = data["pid"]
            islike = data["islike"]
            res = Data.update_like(pid=pid, uid=user.id, islike=islike)
            return {"status": "success", "data": res}
        except Exception as e:
            print(repr(e))
            return jsonify({"status": "failure"})


class Register(Resource):
    @token_required
    def post(self, user):
        try:
            data = request.get_json()
            email = data["email"]
            username = data["uname"]
            password = data["passwd1"]

            if not re.search(email_regex, email):
                return jsonify({"status": "Invalid Email"})

            if not (re.search(username_regex, username)):
                return {"status": "username should be between 4 to 32 characters without spaces"}

            if not (re.search(password_regex, password)):
                return {
                    "status": "password should be between 8 to 32 characters, at least one letter, one number and one "
                              "special character"}

            uid = uuid.uuid4().hex
            guid = uuid.uuid4().hex
            if Data.insert_user(uid=uid, guid=guid, uname=username, passwd=password, email=email):
                token = jwt.encode(
                    {'id': uid, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=45)},
                    current_app.config['SECRET_KEY'], "HS256")

                url = url_for("views.confirm_email", id=guid, uid=uid, _external=True)
                if send_mail(email, username, url, True):
                    response = flask.make_response({'status': 'success', "uname": flask.escape(username)})
                    response.set_cookie("token", token, httponly=True, secure=True, samesite="Strict")
                    return response
                else:
                    return {"status": "error"}
            else:
                return jsonify({'status': 'user or email already exists'})
        except Exception as e:
            print(repr(e))
            return jsonify({"status": "error"})

    def put(self):
        try:
            token = request.cookies.get("token")

            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            user = Data.User.query.filter_by(id=data['id']).first()

            guid = uuid.uuid4().hex
            Data.resend_request(user.id, guid)
            url = url_for("views.confirm_email", id=guid, uid=user.id, _external=True)
            send_mail(user.email, user.username, url, True)

        except Exception as e:
            pass

        return {"status": "success"}


class Login(Resource):
    def get(self):
        try:
            token = request.cookies.get("token")
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = Data.User.query.filter_by(id=data['id']).first()
            if current_user.confirmed:
                if token in active_tokens.values():
                    return {"status": "success"}
                else:
                    return {"status": "false"}
            else:
                return {"status": "email"}
        except Exception as e:
            print(repr(e))
            return {"status": "failure"}

    def post(self):
        auth = request.authorization
        if not auth or not auth.username or not auth.password:
            return jsonify({"status": "failure"})

        try:
            user = Data.check_login(auth.username, auth.password)
            if user:
                token = jwt.encode(
                    {'id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=8000)},
                    current_app.config['SECRET_KEY'], "HS256")
                active_tokens[user.username] = token
                response = flask.make_response(
                    {"status": "success" if user.confirmed else "email", "uname": flask.escape(user.username)})
                response.set_cookie("token", token, httponly=True, secure=True, samesite="Strict")
                return response
            else:
                return jsonify({"status": "username or password is incorrect"})

        except Exception:
            return jsonify({"status": "failure"})


class ResetPassword(Resource):
    def post(self):
        data = request.get_json()
        uid = data["uid"]
        pass1 = data["pass1"]
        guid = data["id"]
        if Data.resetpasswd(uid, pass1, guid):
            response = jsonify({'status': 'success'})
            response.set_cookie("token", "success", httponly=True, secure=True, samesite="Strict")
            return response
        else:
            response = jsonify({'status': 'failure'})
            response.set_cookie("token", "expired", httponly=True, secure=True, samesite="Strict")
            return response

    # reset request
    def put(self):
        data = request.get_json()
        email = data["email"]
        user = Data.getemail(email)
        if user:
            guid = uuid.uuid4().hex
            url = url_for("views.reset", id=guid, uid=user.id, _external=True)

            if send_mail(email, user.username, url, False):
                Data.insert_reset_request(user.id, guid)
                return {"status": "success"}
            else:
                return {"status": "noconfig"}
        else:
            return {"status": "noemail"}


class Posts(Resource):
    @token_required
    def get(self, user):
        try:
            page = request.args.get("page")
            res = Data.get_posts(user.id, page)
            return {"status": "success", "data": res}
        except KeyError as e:
            print(repr(e))
            return {"status": "failure"}

    @token_required
    def post(self, user):
        data = request.get_json()
        try:
            content: str = data["content"]
            if content.strip():
                res = Data.insert_post(uid=user.id, cont=content.strip())
                return {"status": "success"} if res else {"status": "failure"}
            else:
                return {"status": "nocontent"}
        except Exception as e:
            print(e)
            return {"status": "logout"}

    @token_required
    def delete(self, user):
        data = request.get_json()
        try:
            pid = data["pid"]
            Data.deletePost(user.id, pid)
            return {"status": "success"}
        except Exception as e:
            print(e)
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


#
# @app.route("/api/add_friend", methods=['POST'])
# @token_required
# def add_friend(user):
#     """
#     api method, requires token validation
#     accepts field "userid", userid to which friend request is sent to
#     """
#     data = request.get_json()
#     try:
#         userid = data["userid"]
#         Data.friend_request(user.id, userid)
#         return {"status": "success"}
#     except KeyError as e:
#         print(repr(e))
#         return {"status": "failure"}
#
#
# @app.route("/api/accept_friend", methods=["POST"])
# @token_required
# def accept_friend(user):
#     try:
#         data = request.get_json()
#         userid = data["userid"]
#         Data.accept_request(userid.id, userid)
#         return {"status": "success"}
#     except Exception as e:
#         print(repr(e))
#         return {"status": "failure"}
#
#
# @app.route("/api/get_friends", methods=["POST"])
# @token_required
# def get_friends(user):
#     try:
#         data = Data.get_friends(user.id)
#         return {"status": "success", "data": data}
#     except Exception as e:
#         print(repr(e))
#         return {"status": "failure"}
#

def get_years(dob: str) -> int:
    _y, _m, _d = dob[:4], dob[5:7], dob[8:]
    cur = str(datetime.date.today())
    c_y, c_m, c_d = cur[:4], cur[5:7], cur[8:]
    dif_y, dif_m, dif_d = int(c_y) - int(_y), int(c_m) - int(_m), int(c_d) - int(_d)
    if dif_m < 0:
        dif_y -= 1
    elif dif_m == 0 and dif_d < 0:
        dif_y -= 1
    return dif_y
