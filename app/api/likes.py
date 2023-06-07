from flask import request, jsonify
import app.db as Data
from app.api.token_required import token_required
from flask_restful import Resource

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
            res = Data.update_like(pid=pid, user=user, islike=islike)
            return {"status": "success", "data": res}
        except Exception as e:
            print(repr(e))
            return jsonify({"status": "failure"})

