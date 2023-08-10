from flask import Blueprint
from flask_restful import Api
from .image_posts import ImagePost
from .likes import Like
from .login import Login, Logout
from .password_reset import ResetPassword
from .profile_details import ProfileDetails
from .profile_image import ProfileImage
from .register import Register
from .search import SearchUser
from .text_posts import Posts
from .user_details import UserDetails
from .report import Report
from .admin import AdminUserList,AdminAuth, AdminUser
from .chat import socketio

api_bp = Blueprint('api', __name__)
api = Api(api_bp)


api.add_resource(Posts, "/api/posts","/api/posts/delete/<string:pid>")
api.add_resource(ResetPassword, "/api/reset")
api.add_resource(Login, "/api/login")
api.add_resource(Register, "/api/register")
api.add_resource(Like, "/api/like")
api.add_resource(UserDetails, "/api/user_details")
api.add_resource(ProfileImage, "/api/image", "/image/<path:path>")
api.add_resource(ImagePost, "/api/post/image", "/post/images/<path:path>")
api.add_resource(ProfileDetails, "/api/name")
api.add_resource(SearchUser, "/api/search")
api.add_resource(Logout, "/api/logout")
api.add_resource(Report, "/api/report")
api.add_resource(AdminUserList, "/api/admin/users")
api.add_resource(AdminAuth, "/api/admin/login")
api.add_resource(AdminUser,"/api/admin/users/disable/<string:uid>","/api/admin/user/<string:username>")
