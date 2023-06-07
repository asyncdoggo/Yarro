import os
import flask
from flask import request
import app.db as Data
from app.api.token_required import token_required
from flask_restful import Resource


class Posts(Resource):
    @token_required
    def get(self, user):
        try:
            page = request.args.get("page")
            res = Data.get_posts(user, page)
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
                res = Data.insert_post(user=user, cont=content.strip())
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
            Data.deletePost(user, pid, os.path.join(flask.current_app.root_path, "static", "images"))
            return {"status": "success"}
        except Exception as e:
            print(e)
            return {"status": "failure"}
