import uuid

import flask
import random
import Database as db

app = flask.Flask(__name__)

keys = {}

db.initialize("root", "root")


@app.route("/", methods=["POST", "GET"])
def root():
    if flask.request.method == "GET":
        return flask.render_template("index.html")
    if flask.request.method == "POST":
        try:
            sub = flask.request.form["subject"]
            if sub == "gotoreg2":
                return flask.render_template("reg2.html")
        except KeyError:
            pass

        data = flask.request.get_json()

        if data["subject"] == "login":
            return login(data)

        if data["subject"] == "register":
            return register(data)

        if data["subject"] == "login":
            return login(data)

        if data["subject"] == "gotoreg2":
            return flask.render_template("reg2.html")

        if data["subject"] == "reg2_data":
            return update(data)


@app.route("/register")
def render_reg():
    return flask.render_template("register.html")


@app.route("/reset")
def render_reset():
    return flask.render_template("reset.html")


def login(data):
    username = ''
    try:
        username = data["uname"]
        passwd = data["passwd"]

        res = db.check(username, passwd)
        if res:
            key = random.randint(10000000, 99999999)
            keys[username] = key
            resp = {"status": "success", "uname": username, "key": key}
            return resp
        else:
            return {"status": "badpasswd"}

    except KeyError:
        key = data["key"]
        try:
            if str(keys[username]) == key:
                key = random.randint(10000000, 99999999)
                return {"status": "success", "key": key, "uname": username}
            else:
                return {"status": "none"}
        except KeyError:
            return {"status": "none"}


def register(data):
    username = data["uname"]
    password = data["passwd1"]
    email = data["email"]
    if (len(username) < 5 or " " in username) and (len(password) < 5 or " " in password):
        return {"status": "username and password should be between 5 to 20 characters without spaces"}

    res = db.retrieve_users()
    res = [item for t in res for item in t]

    if username in res:
        return {"status": "username already exists"}
    uid = uuid.uuid4().hex
    if db.insert_user(uid=uid, uname=username, passwd=password, email=email):
        data = login({"uname": username, "passwd": password})
        key = data["key"]
        return {"status": "success", "uname": username, "key": key}
    else:
        return {"status": "failure"}


def update(data):
    uname = data["uname"]
    if data["key"] == str(keys[uname]):
        fname = data["fname"]
        lname = data["lname"]
        age = data["age"]
        gender = data["gender"]
        mob = data["mob"]
        dob = data["dob"]
        if db.update(fname=fname, lname=lname, age=age, gender=gender, mob=mob, dob=dob,uname=uname):
            return {"status": "success"}
    else:
        return {"status": "failure"}


app.run(host="0.0.0.0", port=5005, debug=True, use_reloader=False)
