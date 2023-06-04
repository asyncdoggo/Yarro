from flask import Blueprint
from flask_restful import Api
from app.api.routes import *

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

api.add_resource(Posts, "/api/posts")
api.add_resource(ResetPassword, "/api/reset")
api.add_resource(Login, "/api/login")
api.add_resource(Register, "/api/register")
api.add_resource(Like, "/api/like")
api.add_resource(UserDetails, "/api/user_details")
api.add_resource(ProfileImage, "/api/image", "/image/<path:path>")
api.add_resource(ImagePost, "/api/post/image", "/post/images/<path:path>")
api.add_resource(FullnameBio, "/api/name")
api.add_resource(SearchUser, "/api/search")
api.add_resource(Logout, "/api/logout")
