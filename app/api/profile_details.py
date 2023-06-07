from flask import request
import app.db as Data
from app.api.token_required import token_required
from flask_restful import Resource



class ProfileDetails(Resource):
    @token_required
    def get(self, _):
        try:
            user = request.args.get("user")
            name, bio = Data.get_fullname_bio(user)
            return {"status": "success", "name": name, "bio": bio}
        except Exception as e:
            print(repr(e))
            return {"status": "failure"}
