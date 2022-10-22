import datetime
import os
import re
import uuid
from functools import wraps

import jwt
from flask import Flask, request, jsonify, render_template, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from jwt import ExpiredSignatureError, DecodeError

from modules import Database as mysql_db, send_mail

app = Flask(__name__)

app.config['SECRET_KEY'] = '004f2af45d3a4e161a7dd2d17fdae47f'
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.getcwd()}\\Users.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
mysql_db.initialize("root", "root")
db = SQLAlchemy(app)
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'


class Users(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    username = db.Column(db.String(30))


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):

        token = None

        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not token:
            return jsonify({'message': 'a valid token is missing'})

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = Users.query.filter_by(id=data['id']).first()
        except ExpiredSignatureError:
            return jsonify({'status': 'expired'})
        except DecodeError:
            return jsonify({"status": "invalid"})

        return f(current_user, *args, **kwargs)

    return decorator


@app.route("/", methods=["GET", "POST"])
def main():
    if request.method == "GET":
        return render_template("index.html")
    else:
        try:
            jsondata = request.form
            if jsondata["subject"] == "resetsuccess":
                return render_template("index.html", error="Reset successful")

            data = jwt.decode(jsondata["token"], app.config['SECRET_KEY'], algorithms=["HS256"])
            user = Users.query.filter_by(id=data['id']).first()
        except ExpiredSignatureError:
            return jsonify({'message': 'expired'})
        except DecodeError:
            return jsonify({"message": "invalid"})
        except KeyError:
            return jsonify({"message": "notoken"})

        if jsondata["subject"] == "logout":
            return render_template("index.html")
        elif jsondata["subject"] == "regsuccess":
            return render_template("reg2.html")
        elif jsondata["subject"] == "home":
            return render_template("main.html")


@app.route("/register")
def register_render():
    return render_template("register.html")


@app.route("/password/reset")
def reset_render():
    return render_template("forgotpass.html")


@app.route("/profile", methods=["POST", "GET"])
def profile():
    if request.method == "GET":
        return render_template("userprofile.html")

    try:
        jsondata = request.form
        data = jwt.decode(jsondata["token"], app.config['SECRET_KEY'], algorithms=["HS256"])
        user = Users.query.filter_by(id=data['id']).first()
    except ExpiredSignatureError:
        return jsonify({'message': 'expired'})
    except DecodeError:
        return jsonify({"message": "invalid"})

    return render_template("userprofile.html")


@app.route("/api/sendimage", methods=["POST"])
@token_required
def sendimage(user):
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
def updatedata(user):
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
        res = mysql_db.retrieve_users()
        u = mysql_db.update(fname=fname, lname=lname, age=age, gender=gender, mob=mob, dob=dob, uid=res[user.username])
        if u == mob:
            return {"status": "mob"}
        elif u:
            return {"status": "success"}
        else:
            return {"status": "failure"}

    except Exception as e:
        print(repr(e))
        return {"status": "failure"}


@app.route("/api/userdetails", methods=["POST"])
@token_required
def userdetails(user):
    try:
        ret = mysql_db.getuserdetials(user.username)
        return {"status": "success", "data": ret}
    except Exception as e:
        print(repr(e))
        return jsonify({"subject": "failure"})


@app.route("/images/<path:path>")
def get_image(path):
    if not os.path.exists(f"static/images/{path}"):
        path = "default"
    return send_from_directory("static/images", path)


@app.route("/api/like", methods=["GET", "POST"])
@token_required
def update_lc(user):
    try:
        data = request.get_json()
        pid = data["pid"]
        usr = mysql_db.retrieve_users()
        res = mysql_db.update_post(pid=pid, uid=usr[user.username])
        return {"status": "success" if res else "failure"}
    except Exception as e:
        print(repr(e))
        return jsonify({"status": "success"})


@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data["email"]
    username = data["uname"]
    password = data["passwd1"]

    if not re.search(regex, email):
        return jsonify({"status": "Invalid Email"})

    if (30 > len(username) < 5 or " " in username) or (30 > len(password) < 5 or " " in password):
        return {"status": "username and password should be between 5 to 30 characters without spaces"}

    uid = uuid.uuid4().hex
    if mysql_db.insert_user(uid=uid, uname=username, passwd=password, email=email):
        new_user = Users(id=uid, username=username)
        db.session.add(new_user)
        db.session.commit()
        token = jwt.encode(
            {'id': new_user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=45)},
            app.config['SECRET_KEY'], "HS256")
        return jsonify({'token': token, 'status': 'success'})
    else:
        return jsonify({'status': 'username already exists'})


@app.route('/api/login', methods=['POST'])
def login_user():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return jsonify({"status": "failure"})

    try:
        user = Users.query.filter_by(username=auth.username).first()

        if mysql_db.check(auth.username, auth.password):
            token = jwt.encode(
                {'id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=45)},
                app.config['SECRET_KEY'], "HS256")
            return jsonify({'token': token, "status": "success", "uname": user.username})

        return jsonify({"status": "failure"})
    except:
        return jsonify({"status": "failure"})


@app.route("/api/reset", methods=["POST", "GET"])
def passwdreset():
    data = request.get_json()
    username = data["uname"]
    pass1 = data["pass1"]
    guid = data["id"]
    if mysql_db.resetpasswd(username, pass1, guid):
        return {"status": "success"}
    else:
        return {"status": "Unknown Error"}


@app.route("/reset", methods=["POST", "GET"])
def reset():
    guid = request.args.get("id")
    uname = request.args.get("uname")
    if mysql_db.check_reset(guid, uname):
        return render_template("resetpass.html", uname=uname)
    return render_template("forgotpass.html", error="request expired")


@app.route("/api/resetrequest", methods=['POST'])
def resetrequest():
    data = request.get_json()
    email = data["email"]
    uname = mysql_db.getemail(email)
    if uname:
        guid = uuid.uuid4().hex
        url = url_for("reset", id=guid, uname=uname, _external=True)

        if send_mail.send_mail(email, uname, url):
            mysql_db.insert_reset_request(uname, guid)
            return {"status": "success"}
        else:
            return {"status": "noconfig"}
    else:
        return {"status": "noemail"}


@app.route("/api/newpost", methods=['POST'])
@token_required
def new_post(user):
    data = request.get_json()
    try:
        users = mysql_db.retrieve_users()
        uid = users[user.username]
        res = mysql_db.insert_posts(u_id=uid, cont=data["content"])
        return {"status": "success"} if res else {"status": "failure"}
    except Exception as e:
        print(e)
        return {"status": "logout"}


@app.route("/api/posts", methods=['POST'])
@token_required
def get_posts(user):
    data = request.get_json()
    try:
        selfOnly = data["self"]
        ids = mysql_db.retrieve_users()
        res = mysql_db.retrieve_posts(ids[user.username], selfOnly)
        return {"status": "success", "data": res}
    except KeyError as e:
        print(repr(e))
        return {"status": "logout"}


@app.route('/api/user_details', methods=["POST"])
@token_required
def update_details(user):
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

        res = mysql_db.retrieve_users()
        u = mysql_db.update(fname=fname, lname=lname, age=age, gender=gender, mob=mob, dob=dob, uid=res[user])
        if u == mob:
            return {"status": "mob"}
        elif u:
            return {"status": "success"}
        else:
            return {"status": "failure"}
    except KeyError as e:
        return {"status": "logout"}


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
