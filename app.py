import datetime
import os
import re
import uuid
from functools import wraps
import flask
import jwt
from flask import Flask, request, jsonify, render_template, url_for, send_from_directory, make_response
from jwt import ExpiredSignatureError, DecodeError
from werkzeug.utils import secure_filename
import modules.Database as Data
from modules import send_mail

app = Flask(__name__)
app.config['SECRET_KEY'] = '004f2af45d3a4e161a7dd2d17fdae47f'
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:root@127.0.0.1:3306/data"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
username_regex = r"^\w(?:\w|[.-](?=\w)){3,31}$"
password_regex = r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$"

active_tokens = {}

with app.app_context():
    Data.db.init_app(app)
    Data.db.create_all()


def token_required(f):
    """
    token_required(f) decorator will validate a token f and return the User Class object defined in
    modules/Database. token should be sent through HTTP header 'x-access-tokens'
    """

    @wraps(f)
    def decorator(*args, **kwargs):

        token = request.cookies.get("token")

        if not token:
            return jsonify({'message': 'a valid token is missing'})

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = Data.User.query.filter_by(id=data['id']).first()

            if not current_user.confirmed:
                return {"status": "email"}
        except ExpiredSignatureError:
            return jsonify({'status': 'expired'})
        except DecodeError:
            return jsonify({"status": "invalid"})

        return f(current_user, *args, **kwargs)

    return decorator


@app.route("/", methods=["GET"])
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
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = Data.User.query.filter_by(id=data['id']).first()
            if current_user.confirmed:
                return render_template("main.html")
            else:
                return render_template("confirmemail.html")
        except Exception:
            return render_template("index.html")


@app.route("/register")
def register_render():
    """Renders register.html"""
    token = request.cookies.get("token")
    try:
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        current_user = Data.User.query.filter_by(id=data['id']).first()
        if current_user.confirmed:
            return flask.redirect("/")
        else:
            return render_template("confirmemail.html")
    except Exception:
        return render_template("register.html")


@app.route("/password/reset")
def reset_render():
    """Renders forgotpass.html"""
    return render_template("forgotpass.html")


@app.route("/api/fullname", methods=["POST"])
@token_required
def fullname(_):
    """
    api method, requires token validation
    returns full name of user in the "name" field of response JSON body
    and user bio as field "bio"
    """
    try:
        data = request.get_json()
        name, bio = Data.get_fullname_bio(data["uname"])
        return {"status": "success", "name": name, "bio": bio}
    except Exception as e:
        print(repr(e))
        return {"status": "failure"}


@app.route("/profile/edit")
def edit_profile():
    """
    Render editprofile.html requires token in cookie
    """
    try:
        token = request.cookies.get("token")
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        current_user = Data.User.query.filter_by(id=data['id']).first()
        if current_user.confirmed:
            return render_template("editprofile.html")
        else:
            return render_template("index.html")
    except ExpiredSignatureError:
        return jsonify({'message': 'expired'})
    except DecodeError:
        return jsonify({"message": "invalid"})


@app.route("/u/<uname>", methods=["GET"])
def profile(uname):
    """
    renders userprofile.html
    """
    user = Data.get_user(uname)
    if not user:
        return make_response(render_template("404.html", error=f"User {uname} not found"), 404)
    try:
        token = request.cookies.get("token")
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        current_user = Data.User.query.filter_by(id=data['id']).first()
        if current_user.confirmed:
            if current_user.username == uname:
                return render_template("userprofile.html", visiting=False, login=True)
            else:
                return render_template("userprofile.html", visiting=True, login=True)
        else:
            return render_template("confirmemail.html")
    except Exception as e:
        print(repr(e))

    return render_template("userprofile.html", visiting=True, login=False)


@app.route("/api/sendimage", methods=["POST"])
@token_required
def send_image(user):
    """
    api method, requires token validation
    accepts image as a multipart form body as the field "image".
    The filename of the image should be the username of the user without extension
    """
    try:
        file = request.files["image"]
        filename = secure_filename(user.username)
        file.save(os.path.join('static/userimages/', filename))
        return {"status": "success"}
    except KeyError as e:
        print(e)
        return {"status": "failure"}


@app.route("/api/updatedata", methods=["POST"])
@token_required
def update_details(user):
    """
    api method, requires token validation. Updates user details
    data fields are defined as follows
    "name": name of user
    "gender": gender
    "mob": mobile no
    "dob": date of birth in the format yyyy-mm-dd
    """
    try:
        data = request.get_json()
        name = data["name"]
        gender = data["gender"]
        mob = data["mob"]
        dob = data["dob"]
        bio = data["bio"][0:254]

        if not dob:
            dob = "0000-00-00"
            age = 0
        else:
            age = get_y(dob)

        if not mob:
            mob = 0

        u = Data.update(name=name, age=age, gender=gender, mob=mob,
                        dob=datetime.datetime.strptime(dob, "%Y-%m-%d").date(), uid=user.id, bio=bio)
        if u == mob:
            return {"status": "mob"}
        elif u:
            return {"status": "success"}
        else:
            return {"status": "failure"}
    except KeyError:
        return {"status": "logout"}


@app.route("/api/userdetails", methods=["POST"])
@token_required
def user_details(user):
    """
    api method, requires token validation
    returns user details in the "data" field
    the data is a key value pair of following:
    "name": name of user
    "gender": gender
    "mob": mobile no
    "age": age
    "dob": date of birth in the format yyyy-mm-dd
    """
    try:
        ret = Data.getuserdetials(user.id)
        return {"status": "success", "data": ret}
    except Exception as e:
        print(repr(e))
        return jsonify({"subject": "failure"})


@app.route("/images/<path:path>")
def get_image(path):
    """
    method used to fetch user profile image.
    request path should be /images/username where username is the username of user
    returns the user profile image associated with username
    if the image is not found returns the default image
    """
    path = secure_filename(path)
    if not os.path.exists(f"static/userimages/{path}"):
        path = "default"
    return send_from_directory("static/userimages", path)


@app.route("/api/like", methods=["POST"])
@token_required
def update_lc(user):
    """
    api method, requires token validation
    accepts data fields "pid" indicating the post id to like/dislike
    "islike" 0 or 1 value
    "islike" = 0 indicated the post is to be disliked
    "islike" = 1 indicated the post is to be liked
    returns "data" field in response body
    data field contains following:
    "islike" = indicates if the post is liked by the user
    "isdislike" = indicates if the post is disliked by the user
    "lc" = indicates the like count of the post
    "dlc" = indicates the dislike count of the post
    """
    try:
        data = request.get_json()
        pid = data["pid"]
        islike = data["islike"]
        res = Data.update_like(pid=pid, uid=user.id, islike=islike)
        return {"status": "success", "data": res}
    except Exception as e:
        print(repr(e))
        return jsonify({"status": "failure"})


@app.route('/api/register', methods=['POST'])
def register():
    """
    api method
    register new user, accept data fields "email", "uname" and "passwd1" for email, username and password
    passwords are stored as a hash using argon2 hashing algorithm
    returns a token and username in the fields "token" and "uname"
    """
    try:
        data = request.get_json()
        email = data["email"]
        username = data["uname"]
        password = data["passwd1"]

        if not re.search(email_regex, email):
            return jsonify({"status": "Invalid Email"})

        if not (re.search(username_regex, username)):
            return {"status": "username should be between 4 to 32 characters without spaces"}

        if not (re.search(password_regex, password)):
            return {"status": "password should be between 8 to 32 characters, at least one letter, one number and one "
                              "special character"}

        uid = uuid.uuid4().hex
        guid = uuid.uuid4().hex
        if Data.insert_user(uid=uid, guid=guid, uname=username, passwd=password, email=email):
            token = jwt.encode(
                {'id': uid, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=45)},
                app.config['SECRET_KEY'], "HS256")

            url = url_for("confirm_email", id=guid, uid=uid, _external=True)
            if send_mail.send_mail(email, username, url, True):
                response = flask.make_response({'status': 'success', "uname": flask.escape(username)})
                response.set_cookie("token", token, httponly=True, secure=True, samesite="Strict")
                return response
            else:
                return {"status": "error"}
        else:
            return jsonify({'status': 'user or email already exists'})
    except Exception as e:
        print(repr(e))
        return jsonify({"status": "error"})


@app.route('/api/login', methods=['POST'])
def login_user():
    """
    api method
    login method validates username and password,
    The username and password for login should be sent through the Authorization header
    returns a token and username in the fields "token" and "uname"
    """
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return jsonify({"status": "failure"})

    try:
        user = Data.check_login(auth.username, auth.password)
        if user:
            token = jwt.encode(
                {'id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=8000)},
                app.config['SECRET_KEY'], "HS256")
            active_tokens[user.username] = token
            response = flask.make_response(
                {"status": "success" if user.confirmed else "email", "uname": flask.escape(user.username)})
            response.set_cookie("token", token, httponly=True, secure=True, samesite="Strict")
            return response
        else:
            return jsonify({"status": "username or password is incorrect"})

    except Exception:
        return jsonify({"status": "failure"})


@app.route("/api/reset", methods=["POST", "GET"])
def password_reset():
    """
    api method
    reset password for the given user
    accepts data fields "uid", "pass1" and "id" as user id. new password and reset guid
    """
    data = request.get_json()
    uid = data["uid"]
    pass1 = data["pass1"]
    guid = data["id"]
    if Data.resetpasswd(uid, pass1, guid):
        response = flask.make_response()
        response.set_cookie("token", "success", httponly=True, secure=True, samesite="Strict")
        return response
    else:
        response = flask.make_response()
        response.set_cookie("token", "expired", httponly=True, secure=True, samesite="Strict")
        return response


@app.route("/reset", methods=["POST", "GET"])
def reset():
    """
    renders the password reset page by checking the GET method args "id" and "uid" for guid and user id
    """
    guid = request.args.get("id")
    uid = request.args.get("uid")
    if Data.check_reset(guid, uid):
        user = Data.get_user(uid=uid)
        return render_template("resetpass.html")
    return render_template("forgotpass.html")


@app.route("/api/resetrequest", methods=['POST'])
def reset_request():
    """
    api method to create a reset password request
    accepts user email as "email"
    a mail will be sent to the given email address with the reset link
    """
    data = request.get_json()
    email = data["email"]
    user = Data.getemail(email)
    if user:
        guid = uuid.uuid4().hex
        url = url_for("reset", id=guid, uid=user.id, _external=True)

        if send_mail.send_mail(email, user.username, url, False):
            Data.insert_reset_request(user.id, guid)
            return {"status": "success"}
        else:
            return {"status": "noconfig"}
    else:
        return {"status": "noemail"}


@app.route("/api/checklogin", methods=["POST"])
def check_login():
    """
    api method to check if a user is already logged in
    """

    try:
        token = request.cookies.get("token")
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        current_user = Data.User.query.filter_by(id=data['id']).first()
        if current_user.confirmed:
            if token in active_tokens.values():
                return {"status": "success"}
            else:
                return {"status": "false"}
        else:
            return {"status": "email"}
    except Exception as e:
        print(repr(e))
        return {"status": "failure"}


@app.route("/api/newpost", methods=['POST'])
@token_required
def new_post(user):
    """
    api method, requires token validation
    accepts data field "content" to get the post content
    """
    data = request.get_json()
    try:
        content: str = data["content"]
        if content.strip():
            res = Data.insert_post(uid=user.id, cont=content.strip())
            return {"status": "success"} if res else {"status": "failure"}
        else:
            return {"status": "nocontent"}
    except Exception as e:
        print(e)
        return {"status": "logout"}


@app.route("/api/likedata", methods=["POST"])
@token_required
def like_data(user):
    """
    api method, requires token validation
    returns like and dislike data for all posts
    """
    try:
        res = Data.getlikedata(user)
        return {"status": "success", "data": res}
    except Exception:
        return {"status", "success"}


@app.route("/api/posts", methods=['POST'])
@token_required
def get_posts(user):
    """
    api method, requires token validation
    accepts field "page", an integer that identifies next page
    """
    data = request.get_json()
    try:
        page = data["page"]
        res = Data.get_posts(user.id, page)
        return {"status": "success", "data": res}
    except KeyError as e:
        print(repr(e))
        return {"status": "failure"}


@app.route("/api/deletepost", methods=["POST"])
@token_required
def delete_post(user):
    data = request.get_json()
    try:
        pid = data["pid"]
        Data.deletePost(user.id,pid)
        return {"status": "success"}
    except Exception as e:
        print(e)
        return {"status": "failure"}


@app.route("/api/logout", methods=['POST'])
@token_required
def logout(user):
    """
    api method, requires token validation
    method logout, removes the user token from active tokens
    """
    try:
        active_tokens.pop(user.username)
    except KeyError:
        pass
    response = flask.make_response({"status": "success"})
    response.delete_cookie("token")
    return response


@app.route("/confirm", methods=["GET"])
def confirm_email():
    """
    renders the password reset page by checking the GET method args "id" and "uid" for guid and user id
    """
    guid = request.args.get("id")
    uid = request.args.get("uid")
    Data.confirm_email(guid, uid)
    return flask.redirect("/")


@app.route("/api/resend_confirm", methods=["POST"])
def resend_confirm():
    try:
        token = request.cookies.get("token")

        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        user = Data.User.query.filter_by(id=data['id']).first()

        guid = uuid.uuid4().hex
        Data.resend_request(user.id, guid)
        url = url_for("confirm_email", id=guid, uid=user.id, _external=True)
        send_mail.send_mail(user.email, user.username, url, True)

    except Exception as e:
        pass

    return {"status": "success"}


@app.route("/api/add_friend", methods=['POST'])
@token_required
def add_friend(user):
    """
    api method, requires token validation
    accepts field "userid", userid to which friend request is sent to
    """
    data = request.get_json()
    try:
        userid = data["userid"]
        Data.friend_request(user.id, userid)
        return {"status": "success"}
    except KeyError as e:
        print(repr(e))
        return {"status": "failure"}


@app.route("/api/accept_friend", methods=["POST"])
@token_required
def accept_friend(user):
    try:
        data = request.get_json()
        userid = data["userid"]
        Data.accept_request(userid.id, userid)
        return {"status": "success"}
    except Exception as e:
        print(repr(e))
        return {"status": "failure"}


@app.route("/api/get_friends", methods=["POST"])
@token_required
def get_friends(user):
    try:
        data = Data.get_friends(user.id)
        return {"status": "success", "data": data}
    except Exception as e:
        print(repr(e))
        return {"status": "failure"}


def get_y(dob: str) -> int:
    _y, _m, _d = dob[:4], dob[5:7], dob[8:]
    cur = str(datetime.date.today())
    c_y, c_m, c_d = cur[:4], cur[5:7], cur[8:]
    dif_y, dif_m, dif_d = int(c_y) - int(_y), int(c_m) - int(_m), int(c_d) - int(_d)
    if dif_m < 0:
        dif_y -= 1
    elif dif_m == 0 and dif_d < 0:
        dif_y -= 1
    return dif_y


if __name__ == '__main__':
    app.run("0.0.0.0", 5005, debug=True)
