import datetime
import os
import re
import uuid
from functools import wraps

import jwt
from flask import Flask, request, jsonify, render_template, url_for, send_from_directory
from jwt import ExpiredSignatureError, DecodeError

import modules.Database as Data
from modules import send_mail

app = Flask(__name__)
app.config['SECRET_KEY'] = '004f2af45d3a4e161a7dd2d17fdae47f'
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql://root:root@127.0.0.1:3306/data"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

active_tokens = []

with app.app_context():
    Data.db.init_app(app)
    Data.db.create_all()


def token_required(f):
    """
    token_required(f) decorator will validate a JWT created token f and return the User Class object defined in
    modules/Database. token should be sent through HTTP header 'x-access-tokens'
    """

    @wraps(f)
    def decorator(*args, **kwargs):

        token = None

        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not token:
            return jsonify({'message': 'a valid token is missing'})

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = Data.User.query.filter_by(id=data['id']).first()
        except ExpiredSignatureError:
            return jsonify({'status': 'expired'})
        except DecodeError:
            return jsonify({"status": "invalid"})

        return f(current_user, *args, **kwargs)

    return decorator


@app.route("/", methods=["GET", "POST"])
def main():
    """
    The root route of the app. will handle rendering of index.html,forgotpass.html,logout.html,home.html
    """
    if request.method == "GET":
        return render_template("index.html")
    else:
        try:
            jsondata = request.form
            if jsondata["subject"] == "resetsuccess":
                return render_template("index.html", error="Reset successful")
            elif jsondata["subject"] == "expired":
                return render_template("forgotpass.html", error="Request expired")

            jwt.decode(jsondata["token"], app.config['SECRET_KEY'], algorithms=["HS256"])
            # Data.User.query.filter_by(id=data['id']).first()
        except ExpiredSignatureError:
            return jsonify({'message': 'token_expired'})
        except DecodeError:
            return jsonify({"message": "invalid"})
        except KeyError:
            return jsonify({"message": "notoken"})

        if jsondata["subject"] == "logout":
            return render_template("index.html")
        elif jsondata["subject"] == "home":
            return render_template("main.html")


@app.route("/register")
def register_render():
    """Renders register.html"""
    return render_template("register.html")


@app.route("/password/reset")
def reset_render():
    """Renders forgotpass.html"""
    return render_template("forgotpass.html")


@app.route("/api/fullname", methods=["POST"])
@token_required
def fullname(user):
    """
    api method, requires token validation
    returns full name of user in the "name" field of response JSON body
    """
    try:
        name = Data.get_fullname(user.username)
        return {"status": "success", "name": name}
    except Exception as e:
        print(repr(e))
        return {"status": "failure"}


@app.route("/editprofile", methods=["POST"])
def edit_profile():
    """
    form redirect method, requires token to be sent in the form data as "token" field
    renders editprofile.html
    """
    try:
        jsondata = request.form
        jwt.decode(jsondata["token"], app.config['SECRET_KEY'], algorithms=["HS256"])
        # user = Data.User.query.filter_by(id=data['id']).first()
        return render_template("editprofile.html")
    except ExpiredSignatureError:
        return jsonify({'message': 'expired'})
    except DecodeError:
        return jsonify({"message": "invalid"})


@app.route("/profile", methods=["POST", "GET"])
def profile():
    """
    renders userprofile.html
    """
    return render_template("userprofile.html")


@app.route("/api/sendimage", methods=["POST"])
@token_required
def sendimage(user):
    """
    api method, requires token validation
    accepts image as a multipart form body as the field "image".
    The filename of the image should be the username of the user without extension
    """
    try:
        file = request.files["image"]
        filename = file.filename
        file.save(os.path.join('static/images/', filename))
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
    "fname": first name
    "lname": last name
    "gender": gender
    "mob": mobile no
    "dob": date of birth in the format yyyy-mm-dd
    """
    try:
        data = request.get_json()
        fname = data["fname"]
        lname = data["lname"]
        gender = data["gender"]
        mob = data["mob"]
        dob = data["dob"]

        if not dob:
            dob = "0000-00-00"
            age = 0
        else:
            age = get_y(dob)

        if not mob:
            mob = 0

        u = Data.update(fname=fname, lname=lname, age=age, gender=gender, mob=mob,
                        dob=datetime.datetime.strptime(dob, "%Y-%m-%d").date(), uid=user.id)
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
def userdetails(user):
    """
    api method, requires token validation
    returns user details in the "data" field
    the data is a key value pair of following:
    "fname": first name
    "lname": last name
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
    if not os.path.exists(f"static/images/{path}"):
        path = "default"
    return send_from_directory("static/images", path)


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
    "islike" = determines if the post is liked by the user
    "isdislike" = determines of the post is disliked by the user
    "lc" = determines the like count of the post
    "dlc" = determines the dislike count of the post
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

        if not re.search(regex, email):
            return jsonify({"status": "Invalid Email"})

        if (30 > len(username) < 5 or " " in username) or (30 > len(password) < 5 or " " in password):
            return {"status": "username and password should be between 5 to 30 characters without spaces"}

        uid = uuid.uuid4().hex
        if Data.insert_user(uid=uid, uname=username, passwd=password, email=email):
            token = jwt.encode(
                {'id': uid, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=45)},
                app.config['SECRET_KEY'], "HS256")
            return jsonify({'token': token, 'status': 'success', "uname": username})
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
        user = Data.get_user(username=auth.username)

        if Data.check_login(auth.username, auth.password):
            token = jwt.encode(
                {'id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=8000)},
                app.config['SECRET_KEY'], "HS256")
            active_tokens.append(token)
            return jsonify({'token': token, "status": "success", "uname": user.username})

            # if token in active_tokens:
            #     return {"status": "tokenexists"}
            # else:
            #     active_tokens.append(token)
            #     return jsonify({'token': token, "status": "success", "uname": user.username})

        return jsonify({"status": "username or password is incorrect"})
    except:
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
        return {"status": "success"}
    else:
        return {"status": "expired"}


@app.route("/reset", methods=["POST", "GET"])
def reset():
    """
    renders the password reset page by checking the GET method args "id" and "uid" for guid and user id
    """
    guid = request.args.get("id")
    uid = request.args.get("uid")
    if Data.check_reset(guid, uid):
        user = Data.get_user(uid=uid)
        return render_template("resetpass.html", uname=user.username)
    return render_template("forgotpass.html", error="request expired")


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

        if send_mail.send_mail(email, user.username, url):
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
        data = request.get_json()
        if data["token"] in active_tokens:
            return {"status": "success"}
        else:
            return {"status": "false"}

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
        res = Data.insert_post(uid=user.id, cont=data["content"])
        return {"status": "success"} if res else {"status": "failure"}
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
        return res
    except Exception as e:
        return {"status", "success"}


@app.route("/api/posts", methods=['POST'])
@token_required
def get_posts(user):
    """
    api method, requires token validation
    accepts field "latest", an integer that identifies how many posts does client already have
    """
    data = request.get_json()
    try:
        latest = data["latest"]
        res = Data.get_posts(user.id, latest)
        return {"status": "success", "data": res}
    except KeyError as e:
        print(repr(e))
        return {"status": "logout"}


@app.route("/api/logout", methods=['POST'])
def logout():
    """
    api method, requires token validation
    method logout, removes the user token from active tokens
    """
    try:
        data = request.get_json()
        active_tokens.remove(data["token"])
        return {"status": "success"}

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
