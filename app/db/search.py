
from app.db.classes import Details, Posts, Users
from app.db.classes import db
from sqlalchemy import func, text


def search(user="", sort=0):
    # result = db.session.query(Users, Details).filter(
    #     (Users.id == Details.user_id) & ((Users.username.like(f"%{user}%")) | (Details.name.like(f"%{user}%"))))

    sq = db.session.query(Posts.user_id, func.count(
        Posts.post_id).label("count")).group_by(Posts.user_id).subquery()

    sor = db.session.query(Users.username, Details.name, Users.id, sq.c.count).select_from(Users).join(Details, Users.id == Details.user_id)\
            .join(sq, Details.user_id == sq.c.user_id)
    if sort == 0:
        sor = sor.order_by(Users.username.asc())
    elif sort == 1:
        sor = sor.order_by(sq.c.count.desc())

    sor = sor.filter((Users.id == Details.user_id) & (
        (Users.username.like(f"%{user}%")) | (Details.name.like(f"%{user}%"))))
    res = []
    for i in sor:
        res.append({
            "username": i[0],
            "name": i[1],
            "uid": i[2],
            "post_count": i[3],
        })
    return res
