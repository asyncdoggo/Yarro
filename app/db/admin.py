import datetime
import uuid

from app.db.classes import Details, DisLikes, Likes, Posts, Users, Requests, EmailRequests, Admin, Message
from app.db.classes import db, ph
from app.db.search import search


def get_users(user="", sort=0):
    # user = search string
    # search and sort
    # sort = 0 users sorted by alphabetical order of username in ascending order
    # sort = 1 users sorted by number of posts in descending order
    return search(user, sort)


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
            md = Message.__table__.delete().where(sender_id=uid)
            md2 = Message.__table__.delete().where(reciever_id=uid)
            
            db.session.execute(ld)
            db.session.execute(ud)
            db.session.execute(dld)
            db.session.execute(pd)
            db.session.execute(rd)
            db.session.execute(erd)
            db.session.execute(md)
            db.session.execute(md2)

            db.session.commit()
            return True
    except Exception as e:
        print(e)


def disable_user(uid):
    try:
        user:Users = Users.query.filter_by(id=uid).one_or_none()
        if user:
            user.disabled = int(not user.disabled)
            db.session.commit()
            return True
    except Exception as e:
        print(e)


def admin_login(username, password):
    try:
        admin = Admin.query.filter_by(username=username).one_or_none()
        if admin:
            pwhash = admin.password
            ph.verify(pwhash, password)
            return admin

    except Exception as e:
        print(e)


def create_admin(username,password,email):
    hashpass = ph.hash(password)

    admin = Admin(id=uuid.uuid4().hex,username=username,password=hashpass,email=email,created_at=datetime.datetime.utcnow())
    try:
        db.session.add(admin)
        db.session.commit()
        return True
    except Exception as e:
        print(e)

