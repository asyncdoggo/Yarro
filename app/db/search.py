
from app.db.classes import Details, Users
from app.db.classes import db

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

