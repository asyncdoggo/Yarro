import datetime
import re
import uuid
import flask
import jwt
from flask import request, url_for
import app.db as db
from app.util.send_mail import send_mail
from flask_restful import Resource
from flask import current_app
from markupsafe import escape

email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
username_regex = r"^\w(?:\w|[.-](?=\w)){3,31}$"
password_regex = r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$"


class Register(Resource):
    def post(self):
        try:
            data = request.get_json()
            email = data["email"]
            username = data["uname"]
            password = data["passwd1"]

            if not re.search(email_regex, email):
                return {"status": "Invalid Email"}

            if not (re.search(username_regex, username)):
                return {"status": "username should be between 4 to 32 characters without spaces"}

            if not (re.search(password_regex, password)):
                return {
                    "status": "password should be between 8 to 32 characters, at least one letter, one number and one "
                              "special character"}

            uid = uuid.uuid4().hex
            guid = uuid.uuid4().hex
            if db.insert_user(uid=uid, guid=guid, uname=username, passwd=password, email=email):
                token = jwt.encode(
                    {'id': uid, 'exp': datetime.datetime.utcnow(
                    ) + datetime.timedelta(days=30)},
                    current_app.config['SECRET_KEY'], "HS256")

                url = url_for("confirm_email.confirm_email", id=guid,
                              uid=uid, _external=True)
                if send_mail(email, username, url, True):
                    response = flask.make_response(
                        {'status': 'success', "uname": escape(username), "uid": uid})
                    response.set_cookie("token", token, httponly=False, secure=True,
                                        samesite="None", expires=datetime.datetime.utcnow(
                    ) + datetime.timedelta(days=30))
                    return response
                else:
                    return {"status": "error"}
            else:
                return {'status': 'user or email already exists'}
        except Exception as e:
            print(repr(e))
            return {"status": "error"}

    def put(self):
        try:
            token = request.cookies.get("token")

            data = jwt.decode(
                token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            user = db.Users.query.filter_by(id=data['id']).first()

            guid = uuid.uuid4().hex
            db.resend_request(user.id, guid)
            url = url_for("views.confirm_email", id=guid,
                          uid=user.id, _external=True)
            send_mail(user.email, user.username, url, True)

        except Exception as e:
            pass

        return {"status": "success"}
