import flask
import jwt
from flask import Blueprint
from flask import current_app
from flask import request, jsonify, render_template, make_response
from jwt import ExpiredSignatureError, DecodeError
from app.api.admin import admin_token_required
from app.api.token_required import token_required
import app.db as db
import os

root_bp = Blueprint("root", __name__)
register_bp = Blueprint("register", __name__)
edit_profile_bp = Blueprint("edit_profile", __name__)
visit_user_bp = Blueprint("visit_user", __name__)
reset_password_bp = Blueprint("reset_password", __name__)
confirm_email_bp = Blueprint("confirm_email", __name__)
search_bp = Blueprint("search", __name__)
admin_login_bp = Blueprint("admin_login", __name__)
log_bp = Blueprint("log", __name__)
chat_bp = Blueprint("chat", __name__)



nav = [{"name": "Home", "icon": "home", "link": "/"},
       {"name": "Search", "icon": "search", "link": "/search"},
       {"name": "chat", "icon": "chat", "link": "/chat"}]


@root_bp.route("/", methods=["GET"])
def main():
    """
    The root route of the app. will handle rendering of index.html and forgotpass.html
    """
    token = request.cookies.get("token")
    if not token:
        return render_template("index.html")
    elif token == "success":
        response = flask.make_response(render_template("index.html"))
        response.delete_cookie("token")
        return response
    elif token == "expired":
        response = flask.make_response(render_template("forgotpass.html"))
        response.delete_cookie("token")
        return response
    else:
        try:
            data = jwt.decode(
                token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = db.Users.query.filter_by(id=data['id']).one_or_none()
            if not current_user:
                admin = db.Admin.query.filter_by(id=data['id']).one_or_none()
                if admin:
                    return flask.redirect("/admin")

            if current_user.disabled:
                return render_template("disabled.html")
            if not current_user.confirmed:
                return render_template("confirmemail.html")
            return render_template("main.html", nav=nav)

        except Exception:
            return render_template("index.html")


@register_bp.route("/register")
def register_render():
    """Renders register.html"""
    token = request.cookies.get("token")
    try:
        data = jwt.decode(
            token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
        current_user = db.Users.query.filter_by(id=data['id']).one_or_none()
        if not current_user:
            admin = db.Admin.query.filter_by(id=data['id']).one_or_none()
            if admin:
                return flask.redirect("/admin")
        if current_user.disabled:
            return render_template("disabled.html")
        if not current_user.confirmed:
            return render_template("confirmemail.html")

        return flask.redirect("/")
    except Exception:
        return render_template("register.html")


@edit_profile_bp.route("/profile/edit")
def edit_profile():
    """
    Render editprofile.html requires token in cookie
    """
    try:
        token = request.cookies.get("token")
        data = jwt.decode(
            token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
        current_user = db.Users.query.filter_by(id=data['id']).one_or_none()
        if not current_user:
            admin = db.Admin.query.filter_by(id=data['id']).one_or_none()
            if admin:
                return flask.redirect("/admin")
        if current_user.disabled:
            return render_template("disabled.html")
        if current_user.confirmed:
            return render_template("editprofile.html", nav=nav)

        return render_template("index.html")
    except ExpiredSignatureError:
        return jsonify({'message': 'expired'})
    except DecodeError:
        return jsonify({"message": "invalid"})


@visit_user_bp.route("/u/<uname>", methods=["GET"])
def profile(uname):
    """
    renders userprofile.html
    """
    user = db.get_user(uname)
    if not user:
        return make_response(render_template("404.html", error=f"User {uname} not found"), 404)
    try:
        token = request.cookies.get("token")
        data = jwt.decode(
            token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
        current_user = db.Users.query.filter_by(id=data['id']).one_or_none()
        if not current_user:
            admin = db.Admin.query.filter_by(id=data['id']).one_or_none()
            if admin:
                return flask.redirect("/admin")
        if current_user.disabled:
            return render_template("disabled.html")
        if current_user.confirmed:
            if current_user.username == uname:
                return render_template("userprofile.html", uid=user.id, visiting=False, login=True, nav=nav)
            return render_template("userprofile.html", uid=user.id, visiting=True, login=True, nav=nav)
        return render_template("confirmemail.html")
    except Exception as e:
        print(repr(e))

    return render_template("userprofile.html", uid=user.id, visiting=True, login=False)


@reset_password_bp.route("/password/reset")
def reset_render():
    """Renders forgotpass.html"""
    return render_template("forgotpass.html")


@reset_password_bp.route("/reset", methods=["GET"])
def reset():
    """
    renders the password reset page by checking the GET method args "id" and "uid" for guid and user id
    """

    guid = request.args.get("id")
    uid = request.args.get("uid")
    if db.check_reset(guid, uid):
        user = db.get_user(uid=uid)
        return render_template("resetpass.html", uname=user.username)
    return render_template("forgotpass.html")


@confirm_email_bp.route("/confirm", methods=["GET"])
def confirm_email():
    """
    """
    guid = request.args.get("id")
    uid = request.args.get("uid")
    db.confirm_email(guid, uid)
    return flask.redirect("/")


@search_bp.route("/search", methods=["GET"])
@token_required
def search(user):
    try:
        if user.disabled:
            return render_template("disabled.html")
        search_uname = request.args.get("user")
        users = db.search(search_uname)
        return render_template("search.html", users=users, uname=user.username, nav=nav)
    except Exception as e:
        print(repr(e))
        return render_template("404.html")




@log_bp.route("/log")
def log():
    try:
        token = request.args.get('token')

        if token != current_app.config['SECRET_KEY']:
            return render_template("log.html",log="token invalid")

        with open(os.path.join(current_app.root_path, "record.log"), 'r') as f:
            return render_template("log.html", log=f.read())

    except Exception as e:
        print(e)
        return render_template("log.html",log=str(e))
    

@chat_bp.route("/chat")
@token_required
def chat(user):
    try:
        if user.disabled:
            return render_template("disabled.html")
        return render_template("chat.html", nav=nav)
    except Exception as e:
        print(repr(e))
        return render_template("404.html")
    
    
    
@admin_login_bp.route("/admin")
def admin_page():
    token = request.cookies.get("token")

    if not token:
        return render_template("admin/index.html")

    try:
        data = jwt.decode(
            token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
        current_user = db.Admin.query.filter_by(id=data['id']).one_or_none()
        if not current_user:
            return "unauthorized",403
    except jwt.ExpiredSignatureError:
        return {'status': 'expired'},403
    except jwt.DecodeError:
        return {"status": "invalid"},403
    
    return render_template("admin/admin.html")

