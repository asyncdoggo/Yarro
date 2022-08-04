import flask
import random
import db
app = flask.Flask(__name__)

keys = {}


@app.route("/", methods=["POST", "GET"])
def root():
    if flask.request.method == "GET":
        return flask.render_template("index.html")
    if flask.request.method == "POST":
        data = flask.request.get_json()

        if data["subject"] == "login":
            return login(data)

        if data["subject"] == "register":
            return register(data)

        if data["subject"] == "login":
            return login(data)


@app.route("/register")
def render_reg():
    return flask.render_template("register.html")


@app.route("/reset")
def render_reset():
    return flask.render_template("reset.html")


def login(data):
    username = data["uname"]
    passwd = data["passwd"]
    # TODO: check password & username from db


    if "passwordmatch":
        key = random.randint(10000000, 99999999)
        keys[username] = key
        resp = {"status": "success", "uname": username, "key": key}
        return resp
    else:
        return {"status", "badpasswd"}


def register(data):
    username = data["username"]
    password = data["passwd1"]

    if (len(username) < 5 or " " in username) and (len(password < 5) or " " in password):
        return {"status": "username and password should be more than 4 characters without spaces"}

    if "Username already exists":
        return {"status": "username already exists"}

    # TODO put data in db
    """db.insert()"""


app.run(host="0.0.0.0", port=5005, debug=True, use_reloader=False)
