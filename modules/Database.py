import datetime

from argon2 import PasswordHasher
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

ph = PasswordHasher()


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.String(35), primary_key=True, nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)


class Details(db.Model):
    __tablename__ = "details"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(35), db.ForeignKey("users.id"))
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))
    mob = db.Column(db.String(10))
    dob = db.Column(db.Date)


class Posts(db.Model):
    __tablename__ = "posts"
    post_id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.String(35), db.ForeignKey("users.id"))
    content = db.Column(db.String(255), nullable=False)
    l_count = db.Column(db.Integer)
    tstamp = db.Column(db.TIMESTAMP)


class Likes(db.Model):
    __tablename__ = "likes"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.String(35))
    post_id = db.Column(db.Integer)


class Requests(db.Model):
    __tablename__ = "requests"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(35), db.ForeignKey("users.id"), nullable=False)
    guid = db.Column(db.String(255), nullable=False)
    tstamp = db.Column(db.TIMESTAMP)


def update(fname, lname, age, gender, mob, dob, uid):
    detail = Details.query.filter_by(user_id=uid).one()
    detail.first_name = fname
    detail.last_name = lname
    detail.age = age
    detail.gender = gender
    detail.mob = mob
    detail.dob = dob
    db.session.commit()
    return True


def getuserdetials(id):
    details = Details.query.filter_by(user_id=id).one()
    return {"fname": details.first_name, "lname": details.last_name, "age": details.last_name, "gender": details.gender,
            "mob": details.mob, "dob": str(details.dob)}


def update_like(pid, uid):
    try:
        like = Likes.query.filter_by(user_id=uid, post_id=pid).one_or_none()
        if like:
            db.session.delete(like)
            post = Posts.query.filter_by(post_id=pid).one()
            post.l_count -= 1
        else:
            like = Likes()
            like.user_id = uid
            like.post_id = pid
            db.session.add(like)
            post = Posts.query.filter_by(post_id=pid).one()
            post.l_count += 1
        db.session.commit()
        return True
    except Exception as e:
        print(repr(e))


def check_login(username, password):
    try:
        user = User.query.filter_by(username=username).one()
        if user:
            pwhash = user.password
            ph.verify(pwhash, password)
            return user.username
    except Exception as e:
        print(repr(e))


def insert_user(uid, uname, passwd, email):
    try:
        hashpass = ph.hash(passwd)

        user = User()
        user.username = uname
        user.id = uid
        user.password = hashpass
        user.email = email

        detail = Details()
        detail.user_id = uid
        db.session.add(user)
        db.session.add(detail)
        db.session.commit()
        return True
    except Exception as e:
        print(repr(e))


def get_user(username=None, uid=None):
    try:
        if username:
            user = User.query.filter_by(username=username).one()
        else:
            user = User.query.filter_by(id=uid).one()
        return user
    except Exception as e:
        print(repr(e))


def resetpasswd(uid, pass1, guid):
    try:
        req = Requests.query.filter_by(user_id=uid).one()
        if ph.verify(req.guid,guid):
            pwhash = ph.hash(pass1)
            user = User.query.filter_by(id=uid).one()
            user.password = pwhash
            db.session.delete(req)
            db.session.commit()
            return True
    except Exception as e:
        print(repr(e))
def getemail(email):
    try:
        user = User.query.filter_by(email=email).one()
        return user
    except Exception as e:
        print(repr(e))


def insert_reset_request(uid, guid):
    try:
        guid_hash = ph.hash(guid)
        req = Requests.query.filter_by(user_id=uid).one_or_none()
        if req:
            db.session.delete(req)
        req = Requests()
        req.user_id = uid
        req.guid = guid_hash
        req.tstamp = datetime.datetime.now()
        db.session.add(req)
        db.session.commit()
    except Exception as e:
        print(repr(e))


def check_reset(guid, uid):
    try:
        req = Requests.query.filter_by(user_id=uid).one()
        guidhash = req.guid
        if ph.verify(guidhash, guid):
            return True
    except Exception as e:
        print(repr(e))


def insert_posts(uid, cont):
    post = Posts()
    try:
        post.user_id = uid
        post.content = cont
        post.l_count = 0
        post.tstamp = datetime.datetime.now()
        db.session.add(post)
        db.session.commit()
        return True
    except Exception as e:
        print(repr(e))


def get_posts(uid, selfOnly):
    if selfOnly == "false":
        result = db.session.query(Posts, User).filter(User.id == Posts.user_id).all()
    else:
        result = db.session.query(Posts, User).filter(User.id == Posts.user_id, User.id == uid).all()

    likes = db.session.query(Likes.user_id, Likes.post_id).filter(Likes.user_id == uid).all()
    p = {}
    for i, j in result:
        p[i.post_id] = {"uid": j.id, "content": i.content, "lc": i.l_count, "datetime": str(i.tstamp),
                        "uname": j.username, "islike": 1 if (j.id, i.post_id) in likes else 0}
    return p
