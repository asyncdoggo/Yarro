from argon2 import PasswordHasher
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()
ph = PasswordHasher()


class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.String(35), primary_key=True, nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    confirmed = db.Column(db.Boolean,default=False, nullable=False)
    created_at = db.Column(db.TIMESTAMP, nullable=False)
    disabled = db.Column(db.Boolean,default=False, nullable=False)


class Details(db.Model):
    __tablename__ = "details"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(35))
    name = db.Column(db.String(50))
    gender = db.Column(db.String(10))
    mob = db.Column(db.String(10))
    dob = db.Column(db.Date)
    bio = db.Column(db.String(255))


class Posts(db.Model):
    __tablename__ = "posts"
    post_id = db.Column(db.String(35), primary_key=True,nullable=False)
    user_id = db.Column(db.String(35))
    content = db.Column(db.String(255), nullable=False)
    content_type = db.Column(db.String(20))
    l_count = db.Column(db.Integer)
    dl_count = db.Column(db.Integer)
    tstamp = db.Column(db.TIMESTAMP)


class Likes(db.Model):
    __tablename__ = "likes"
    id = db.Column(db.Integer, primary_key=True,
                   nullable=False, autoincrement=True)
    user_id = db.Column(db.String(35))
    post_id = db.Column(db.String(35))


class DisLikes(db.Model):
    __tablename__ = "dislikes"
    id = db.Column(db.Integer, primary_key=True,
                   nullable=False, autoincrement=True)
    user_id = db.Column(db.String(35))
    post_id = db.Column(db.String(35))


class Requests(db.Model):
    __tablename__ = "requests"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(35), nullable=False)
    guid = db.Column(db.String(255), nullable=False)
    tstamp = db.Column(db.TIMESTAMP)


class EmailRequests(db.Model):
    __tablename__ = "emailrequests"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(35), unique=True, nullable=False)
    guid = db.Column(db.String(255), nullable=False)
    tstamp = db.Column(db.TIMESTAMP)


class Friendship(db.Model):
    __tablename__ = 'friendships'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user1_id = db.Column(db.String(35), nullable=False)
    user2_id = db.Column(db.String(35), nullable=False)
    initiator_id = db.Column(db.String(35))


class Admin(db.Model):
    __tablename__ = "admin"
    id = db.Column(db.String(35), primary_key=True,
                   nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(
        db.TIMESTAMP, nullable=False)


class Reports(db.Model):
    __tablename__ = "reports"
    id = db.Column(db.Integer, primary_key=True,
                   nullable=False, autoincrement=True)
    post_id = db.Column(db.String(35),nullable=False)
    reported_by = db.Column(db.String(35), nullable=False, unique=True)
    reason = db.Column(db.String(255), nullable=False)
    created_at = db.Column(
        db.TIMESTAMP, nullable=False)
    resolved = db.Column(db.Boolean,default=False)
    resolution_message = db.Column(db.String(255))
    resolved_by = db.Column(db.String(35))



class Message(db.Model):
    __tablename__ = "messages"
    message_id = db.Column(db.String(35), primary_key=True,nullable=False)
    sender_id = db.Column(db.String(35))
    reciever_id = db.Column(db.String(35))
    content = db.Column(db.String(255), nullable=False)
    tstamp = db.Column(db.TIMESTAMP)
    unread = db.Column(db.Boolean,default=True)
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
