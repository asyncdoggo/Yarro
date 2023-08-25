import uuid

from flask import request, url_for, make_response
from flask_restful import Resource

import app.db as db
from app.util.send_mail import send_mail


class ResetPassword(Resource):
    def post(self):
        data = request.get_json()
        uid = data["uid"]
        pass1 = data["pass1"]
        guid = data["id"]
        if db.resetpasswd(uid, pass1, guid):
            response = make_response({'status': 'success'})
            response.set_cookie("token", "success", httponly=True, secure=True, samesite="Strict")
            return response
        else:
            response = make_response({'status': 'failure'})
            response.set_cookie("token", "expired", httponly=True, secure=True, samesite="Strict")
            return response

    # reset request
    def put(self):
        data = request.get_json()
        email = data["email"]
        user = db.getemail(email)
        if user:
            guid = uuid.uuid4().hex
            url = url_for("reset_password.reset", id=guid, uid=user.id, _external=True)

            if send_mail(email, user.username, url, False):
                db.insert_reset_request(user.id, guid)
                return {"status": "success"}
            
            return {"status": "noconfig"}
        return {"status": "noemail"}
