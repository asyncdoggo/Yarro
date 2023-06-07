import uuid
from flask import request, jsonify, url_for
import app.db as Data
from app.util.send_mail import send_mail
from flask_restful import Resource


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
