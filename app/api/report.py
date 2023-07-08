import flask
from flask_restful import Resource
from app.db.report import add_report

from app.api.token_required import token_required


class Report(Resource):
    @token_required
    def post(self, user):
        data = flask.request.get_json()
        print(data)
        pid = data["pid"]
        uid = user.id
        reason = data["reason"]
        if add_report(pid, uid, reason):
            return {"status": "success"}
        else:
            return {"status": "failure"}
