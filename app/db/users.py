import datetime
import os
from sqlalchemy import desc
from argon2 import PasswordHasher
from flask_sqlalchemy import SQLAlchemy

from app.db.classes import Details, EmailRequests, Users
from app.db.classes import db,ph


def check_login(username, password):
    try:
        user: Users = Users.query.filter_by(username=username).one()
        if user:
            pwhash = user.password
            ph.verify(pwhash, password)
            return user
    except Exception as e:
        print(repr(e))


def insert_user(uid, guid, uname, passwd, email):
    try:
        hashpass = ph.hash(passwd)

        user: Users = Users(username=uname, id=uid, password=hashpass, email=email, confirmed=False)
        db.session.add(user)
        db.session.commit()
        detail = Details()
        detail.name = detail.gender = detail.mob = detail.bio = ""
        detail.age = 0
        detail.dob = datetime.datetime(1000, 1, 1)
        detail.user_id = uid
        db.session.add(detail)
        guid_hash = ph.hash(guid)
        request: EmailRequests = EmailRequests(user_id=uid, guid=guid_hash, tstamp=datetime.datetime.now())
        db.session.add(request)
        db.session.commit()
        return True
    except Exception as e:
        print(repr(e))


def get_user(username=None, uid=None):
    try:
        if username:
            user = Users.query.filter_by(username=username).one()
        else:
            user = Users.query.filter_by(id=uid).one()
        return user
    except Exception as e:
        print(repr(e))



