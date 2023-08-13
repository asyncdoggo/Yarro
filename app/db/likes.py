
from app.db.classes import DisLikes, Likes, Posts
from app.db.classes import db


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