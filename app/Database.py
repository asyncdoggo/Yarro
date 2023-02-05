import datetime
import os

from sqlalchemy import desc
from argon2 import PasswordHasher
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
ph = PasswordHasher()


class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.String(35), primary_key=True, nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    confirmed = db.Column(db.Boolean, nullable=False)


class Details(db.Model):
    __tablename__ = "details"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(35), db.ForeignKey("users.id", ondelete="CASCADE"))
    name = db.Column(db.String(50))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))
    mob = db.Column(db.String(10))
    dob = db.Column(db.Date)
    bio = db.Column(db.String(255))


class Posts(db.Model):
    __tablename__ = "posts"
    post_id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.String(35), db.ForeignKey("users.id", ondelete="CASCADE"))
    content = db.Column(db.String(255), nullable=False)
    content_type = db.Column(db.String(20))
    l_count = db.Column(db.Integer)
    dl_count = db.Column(db.Integer)
    tstamp = db.Column(db.TIMESTAMP)


class Likes(db.Model):
    __tablename__ = "likes"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.String(35), db.ForeignKey("users.id", ondelete="CASCADE"))
    post_id = db.Column(db.Integer, db.ForeignKey("posts.post_id", ondelete="CASCADE"))


class DisLikes(db.Model):
    __tablename__ = "dislikes"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.String(35), db.ForeignKey("users.id", ondelete="CASCADE"))
    post_id = db.Column(db.Integer, db.ForeignKey("posts.post_id", ondelete="CASCADE"))


class Requests(db.Model):
    __tablename__ = "requests"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(35), db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    guid = db.Column(db.String(255), nullable=False)
    tstamp = db.Column(db.TIMESTAMP)


class EmailRequests(db.Model):
    __tablename__ = "emailrequests"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(35), db.ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    guid = db.Column(db.String(255), nullable=False)
    tstamp = db.Column(db.TIMESTAMP)


class Friendship(db.Model):
    __tablename__ = 'friendships'
    id = db.Column(db.Integer, primary_key=True)
    user1_id = db.Column(db.String(35), db.ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    user2_id = db.Column(db.String(35), db.ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    initiator_id = db.Column(db.String(35), db.ForeignKey('users.id', ondelete="CASCADE"))


def update(name, age, gender, mob, dob, uid, bio):
    detail = Details.query.filter_by(user_id=uid).one()
    detail.name = name
    detail.age = age
    detail.gender = gender
    detail.mob = mob
    detail.dob = dob
    detail.bio = bio
    db.session.commit()
    return True


def get_fullname_bio(username):
    user = Users.query.filter_by(username=username).one()
    details: Details = Details.query.filter_by(user_id=user.id).one()
    return details.name, details.bio


def getuserdetials(user):
    details: Details = Details.query.filter_by(user_id=user.id).one()
    return {"name": details.name, "age": details.age, "gender": details.gender,
            "mob": details.mob, "dob": str(details.dob), "bio": details.bio}


def update_like(pid, user, islike):
    like: Likes = Likes.query.filter_by(user_id=user.id, post_id=pid).one_or_none()
    dislike: DisLikes = DisLikes.query.filter_by(user_id=user.id, post_id=pid).one_or_none()
    p = {}
    try:
        if islike:
            if like:
                db.session.delete(like)
                post = Posts.query.filter_by(post_id=pid).one()
                post.l_count -= 1
            else:
                like = Likes()
                like.user_id = user.id
                like.post_id = pid
                db.session.add(like)
                post = Posts.query.filter_by(post_id=pid).one()
                if dislike:
                    post.dl_count -= 1
                    db.session.delete(dislike)
                post.l_count += 1
                p["islike"] = 1
            db.session.commit()
            p["lc"] = post.l_count
            p["dlc"] = post.dl_count
            p["isdislike"] = 0
        else:
            if dislike:
                db.session.delete(dislike)
                post = Posts.query.filter_by(post_id=pid).one()
                post.dl_count -= 1
            else:
                dislike = DisLikes()
                dislike.user_id = user.id
                dislike.post_id = pid
                db.session.add(dislike)
                post = Posts.query.filter_by(post_id=pid).one()
                if like:
                    post.l_count -= 1
                    db.session.delete(like)
                post.dl_count += 1
                p["isdislike"] = 1
            db.session.commit()
            p["lc"] = post.l_count
            p["dlc"] = post.dl_count
            p["islike"] = 0

        return p
    except Exception as e:
        print(repr(e))


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


def getlikedata(user):
    try:
        result = db.session.query(Posts).all()
        likes = db.session.query(Likes.user_id, Likes.post_id).filter(Likes.user_id == user.id).all()
        dislikes = db.session.query(DisLikes.user_id, DisLikes.post_id).filter(DisLikes.user_id == user.id).all()

        p = {}
        for each in result:
            p[each.post_id] = {
                "lc": each.l_count,
                "dlc": each.dl_count,
                "islike": 1 if (user.id, each.post_id) in likes else 0,
                "isdislike": 1 if (user.id, each.post_id) in dislikes else 0
            }
        return p
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


def insert_post(user, cont):
    post = Posts(user_id=user.id, content=cont, content_type="text", l_count=0, dl_count=0,
                 tstamp=datetime.datetime.utcnow())
    try:
        db.session.add(post)
        db.session.commit()
        return True
    except Exception as e:
        print(repr(e))


def get_posts(user, page):
    result = db.session.query(Posts, Users, Details).filter(Users.id == Posts.user_id,
                                                            Users.id == Details.user_id).order_by(
        desc(Posts.post_id)).limit(10).offset(page).all()

    likes = db.session.query(Likes.user_id, Likes.post_id).filter(Likes.user_id == user.id).all()
    dislikes = db.session.query(DisLikes.user_id, DisLikes.post_id).filter(DisLikes.user_id == user.id).all()
    p = {}

    for i, j, k in result:
        p[i.post_id] = {
                        "post_id": i.post_id,
                        "content": i.content,
                        "content_type": i.content_type,
                        "lc": i.l_count,
                        "dlc": i.dl_count,
                        "datetime": i.tstamp.strftime("%Y-%m-%d %H:%M:%S"),
                        "uname": j.username,
                        "uid": j.id,
                        "islike": 1 if (user.id, i.post_id) in likes else 0,
                        "isdislike": 1 if (user.id, i.post_id) in dislikes else 0,
                        "fullname": k.name
                        }
    return p


#
# def send_friend_request(user1, user2):
#     friend: Friendship = Friendship(user1_id=user1, user2_id=user2, initiator_id=user1)
#     db.session.add(friend)
#     db.session.commit()
#
#
# def accept_friend_request(user1, user2):
#     friend = Friendship.query.filter_by(user1_id=user1, user2_id=user2).one_or_none()
#     friend.initiator_id = None
#     db.session.commit()
#
#
# def get_friends(user):
#     friends1 = Friendship.query.filter_by(user1_id=user)
#     friends2 = Friendship.query.filter_by(user2_id=user)
#
#     sq = friends1.union(friends2).all()
#     res = []
#
#     for i in sq:
#         user1 = Users.query.filter_by(id=i.user_id1).one()
#         user2 = Users.query.filter_by(id=i.user_id2).one()
#         user3 = Users.query.filter_by(id=i.byuserid).one_or_none()
#
#         res.append({
#             "user1": user1.username,
#             "user2": user2.username,
#             "by": user3.username if user3 else "null"
#         })
#
#     return res


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


def deletePost(user, pid, path):
    try:
        res = Posts.query.filter_by(user_id=user.id, post_id=pid).one_or_none()
        if res and res.content_type == "image":
            file = res.content
            os.remove(path + os.sep + file)
        db.session.delete(res)
        db.session.commit()
    except Exception as e:
        print(e)


def search(user):
    result = db.session.query(Users, Details).filter(
        (Users.id == Details.user_id) & ((Users.username.like(f"%{user}%")) | (Details.name.like(f"%{user}%")))).all()
    res = []
    for i in result:
        res.append({
            "username": i[0].username,
            "name": i[1].name,
            "uid": i[0].id
        })
    return res


def insert_post_image(user, filename):
    try:
        post: Posts = Posts(user_id=user.id, content=filename, content_type="image", l_count=0, dl_count=0,
                            tstamp=datetime.datetime.utcnow())
        db.session.add(post)
        db.session.commit()
        return True
    except Exception as e:
        return False
