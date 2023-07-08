from flask import request
from flask_restful import Resource

import app.db as db
from app.api.token_required import token_required


class Like(Resource):
    @token_required
    def get(self, user):
        try:
            res = db.getlikedata(user)
            return {"status": "success", "data": res}
        except Exception:
            return {"status", "success"}

    @token_required
    def post(self, user):
        try:
            data = request.get_json()
            pid = data["pid"]
            islike = data["islike"]
            res = db.update_like(pid=pid, user=user, islike=islike)
            return {"status": "success", "data": res}
        except Exception as e:
            print(repr(e))
            return {"status": "failure"}
