from flask import request
import app.db as db
from app.api.token_required import token_required
from flask_restful import Resource





class SearchUser(Resource):
    @token_required
    def get(self, _):
        try:
            user = request.args.get("user")
            users = db.search(user)
            return {"status": "success", "data": users}
        except Exception as e:
            print(e)
            return {"status": "failure"}
