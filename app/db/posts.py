import datetime
import os
import uuid
from markupsafe import escape
import flask
from app.db.classes import Details, DisLikes, Likes, Posts, Users
from app.db.classes import db

def insert_post(user, cont):
    post = Posts(post_id=uuid.uuid4().hex,user_id=user.id, content=cont, content_type="text", l_count=0, dl_count=0,
                 tstamp=datetime.datetime.utcnow())
    try:
        db.session.add(post)
        db.session.commit()
        return True
    except Exception as e:
        print(repr(e))


def get_posts(user, page, limit=10):
    result = db.session.query(Posts, Users, Details).filter(Users.id == Posts.user_id,
                                                            Users.id == Details.user_id).order_by(Posts.tstamp.desc()).offset(page*limit).limit(limit).all()
    
    likes = db.session.query(Likes.user_id, Likes.post_id).filter(Likes.user_id == user.id).all()
    dislikes = db.session.query(DisLikes.user_id, DisLikes.post_id).filter(DisLikes.user_id == user.id).all()
    p = []

    for i, j, k in result:
        p.append({
                        "post_id": i.post_id,
                        "content": escape(i.content),
                        "content_type": i.content_type,
                        "lc": i.l_count,
                        "dlc": i.dl_count,
                        "datetime": i.tstamp.strftime("%Y-%m-%d %H:%M:%S"),
                        "uname": j.username,
                        "uid": j.id,
                        "islike": 1 if (user.id, i.post_id) in likes else 0,
                        "isdislike": 1 if (user.id, i.post_id) in dislikes else 0,
                        "fullname": k.name
                        })
    return p



def deletePost(user, pid, path):
    try:
        res = Posts.query.filter_by(user_id=user.id, post_id=pid).one_or_none()
        if res and res.content_type == "image":
            try:
                file = res.content
                os.remove(path + os.sep + file)
            except:
                pass
        db.session.delete(res)
        db.session.commit()
    except Exception as e:
        print(e)



def insert_post_image(user, filename):
    try:
        post: Posts = Posts(post_id=uuid.uuid4().hex,user_id=user.id, content=filename, content_type="image", l_count=0, dl_count=0,
                            tstamp=datetime.datetime.utcnow())
        db.session.add(post)
        db.session.commit()
        return True
    except Exception as e:
        return False

