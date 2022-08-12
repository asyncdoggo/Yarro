import uuid
from datetime import date
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

        if data["subject"] == "reg2_data":
            return update(data)

        if data["subject"] == "resetpass":
            return reset(data)


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

    res1 = db.retrieve_users()
    res = res1.keys()

    if username in res:
        return {"status": "alreadyuser"}
    uid = uuid.uuid4().hex
    if db.insert_user(uid=uid, uname=username, passwd=password, email=email):
        data = login({"uname": username, "passwd": password})
        key = data["key"]
        return {"status": "success", "uname": username, "key": key}
    else:
        return {"status": "alreadyemail"}


def reset(data):
    username = data["uname"]
    oldpass = data["oldpass"]
    newpass = data["newpass"]

    res = db.check(username, oldpass)
    if res:
        if db.resetpasswd(username, newpass):
            return {"status": "success"}
        else:
            return {"status": "nouser"}
    else:
        return {"status": "badpass"}


def update(data):
    uname = data["uname"]
    if data["key"] == str(keys[uname]):
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

        if db.update(fname=fname, lname=lname, age=age, gender=gender, mob=mob, dob=dob, uname=uname):
            return {"status": "success"}
        else:
            return {"status": "failure"}
    else:
        return {"status": "failure"}



def get_y(dob:str) -> int:
    _y, _m, _d = dob[:4], dob[5:7], dob[8:]

    cur = str(date.today())
    c_y, c_m, c_d = cur[:4], cur[5:7], cur[8:]

    dif_y, dif_m, dif_d = int(c_y) - int(_y), int(c_m) - int(_m), int(c_d) - int(_d)
    
    if dif_m < 0:
        dif_y -= 1
    elif dif_m == 0 and dif_d < 0:
        dif_y -=1

    return dif_y


app.run(host="0.0.0.0", port=5005, debug=True, use_reloader=False)
