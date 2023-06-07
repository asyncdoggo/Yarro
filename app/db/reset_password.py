
import datetime
from app.db.classes import EmailRequests, Requests, Users
from app.db.classes import ph, db

def resetpasswd(uid, pass1, guid):
    try:
        req = Requests.query.filter_by(user_id=uid).one()
        if ph.verify(req.guid, guid):
            pwhash = ph.hash(pass1)
            user = Users.query.filter_by(id=uid).one()
            user.password = pwhash
            db.session.delete(req)
            db.session.commit()
            return True
    except Exception as e:
        print(repr(e))




def getemail(email):
    try:
        user = Users.query.filter_by(email=email).one()
        return user
    except Exception as e:
        print(repr(e))


def insert_reset_request(uid, guid):
    try:
        guid_hash = ph.hash(guid)
        req = Requests.query.filter_by(user_id=uid).one_or_none()
        if req:
            db.session.delete(req)
        req = Requests(user_id=uid, guid=guid_hash, tstamp=datetime.datetime.now())
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




def confirm_email(guid, uid):
    try:
        req = EmailRequests.query.filter_by(user_id=uid).one()
        guidhash = req.guid
        if ph.verify(guidhash, guid):
            user = Users.query.filter_by(id=uid).one()
            user.confirmed = True
            db.session.delete(req)
            db.session.commit()
            return True
    except Exception as e:
        print(repr(e))


def resend_request(uid, guid):
    try:
        req = EmailRequests.query.filter_by(user_id=uid).one_or_none()
        if not req:
            req = EmailRequests()
        req.user_id = uid
        req.guid = ph.hash(guid)
        req.tstamp = datetime.datetime.now()
        db.session.add(req)
        db.session.commit()
    except Exception as e:
        print(repr(e))

