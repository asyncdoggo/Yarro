import flask
from flask_restful import Resource

from app.api.admin import admin_token_required
import app.db as db

from app.api.token_required import token_required


class Report(Resource):
    @token_required
    def post(self, user):
        data = flask.request.get_json()
        print(data)
        pid = data["pid"]
        uid = user.id
        reason = data["reason"]
        if db.add_report(pid, uid, reason):
            return {"status": "success"}
        else:
            return {"status": "failure"}

    @admin_token_required
    def get(self,user):
        reports = db.get_all_reports()
        return {"status":"success","reports":reports}

