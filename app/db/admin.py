import datetime
import os
from sqlalchemy import desc
from argon2 import PasswordHasher
from flask_sqlalchemy import SQLAlchemy

from app.db.classes import Details, DisLikes, Likes, Posts, Users, Requests, EmailRequests,Admin
from app.db.classes import db
from app.db.search import search


def get_users(user=""):
    return search(user)


def delete_user(uid):
    try:
        user = Users.query.filter_by(id=uid).one_or_none()
        if user:
            ud = Details.__table__.delete().where(user_id=uid)
            ld = Likes.__table__.delete().where(user_id=uid)
            dld = DisLikes.__table__.delete().where(user_id=uid)
            pd = Posts.__table__.delete().where(user_id=uid)
            rd = Requests.__table__.delete().where(user_id=uid)
            erd = EmailRequests.__table__.delete().where(user_id=uid)

            db.session.execute(ld)
            db.session.execute(ud)
            db.session.execute(dld)
            db.session.execute(pd)
            db.session.execute(rd)
            db.session.execute(erd)

            db.session.commit()
            return True
        else:
            return False
    except Exception as e:
        print(e)


def admin_login(username,password):
    try:
        admin = Admin.query.filter_by(username=username).one_or_none()
        if admin:
            pwhash = admin.password
            ph.verify(pwhash, password)
            return admin
        

    except Exception as e:
        print(e)