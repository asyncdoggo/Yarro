
from app.db.classes import Details, Users
from app.db.classes import db


def update_details(name, gender, mob, dob, uid, bio):
    detail = Details.query.filter_by(user_id=uid).one()
    detail.name = name
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
    return {"name": details.name,"gender": details.gender,
            "mob": details.mob, "dob": str(details.dob), "bio": details.bio}
