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

post_api_bp = Blueprint('post_api', __name__)
post_api = Api(post_api_bp)

reset_password_api_bp = Blueprint('reset_password_api', __name__)
reset_password_api = Api(reset_password_api_bp)

login_api_bp = Blueprint('login_api', __name__)
login_api = Api(login_api_bp)

register_api_bp = Blueprint('register_api', __name__)
register_api = Api(register_api_bp)

like_api_bp = Blueprint('like_api', __name__)
like_api = Api(like_api_bp)

user_details_api_bp = Blueprint('user_details_api', __name__)
user_details_api = Api(user_details_api_bp)

profile_image_api_bp = Blueprint('profile_image_api', __name__)
profile_image_api = Api(profile_image_api_bp)

image_post_api_bp = Blueprint('image_post_api', __name__)
image_post_api = Api(image_post_api_bp)

profile_details_api_bp = Blueprint('profile_details_api', __name__)
profile_details_api = Api(profile_details_api_bp)

search_user_api_bp = Blueprint('search_api', __name__)
search_api = Api(post_api_bp)

logout_api_bp = Blueprint('logout_api', __name__)
logout_api = Api(logout_api_bp)

report_api_bp = Blueprint('report_api', __name__)
report_api = Api(report_api_bp)

admin_user_list_api_bp = Blueprint('admin_user_list_api', __name__)
admin_user_list_api = Api(admin_user_list_api_bp)

admin_auth_api_bp = Blueprint('admin_auth_api', __name__)
admin_auth_api = Api(admin_auth_api_bp)


admin_user_api_bp = Blueprint('admin_user_api', __name__)
admin_user_api = Api(admin_user_api_bp)



post_api.add_resource(Posts, "/api/posts","/api/posts/delete/<string:pid>")
reset_password_api.add_resource(ResetPassword, "/api/reset")
login_api.add_resource(Login, "/api/login")
register_api.add_resource(Register, "/api/register")
like_api.add_resource(Like, "/api/like")
user_details_api.add_resource(UserDetails, "/api/user_details")
profile_image_api.add_resource(ProfileImage, "/api/image", "/image/<path:path>")
image_post_api.add_resource(ImagePost, "/api/post/image", "/post/images/<path:path>")
profile_details_api.add_resource(ProfileDetails, "/api/name")
search_api.add_resource(SearchUser, "/api/search")
logout_api.add_resource(Logout, "/api/logout")
report_api.add_resource(Report, "/api/report")
admin_user_list_api.add_resource(AdminUserList, "/api/admin/users")
admin_auth_api.add_resource(AdminAuth, "/api/admin/login")
admin_user_api.add_resource(AdminUser,"/api/admin/users/disable/<string:uid>","/api/admin/user/<string:username>")
