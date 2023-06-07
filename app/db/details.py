import datetime
import os
from sqlalchemy import desc
from argon2 import PasswordHasher
from flask_sqlalchemy import SQLAlchemy

from app.db.classes import Details, Users
from app.db.classes import db


def update_details(name, age, gender, mob, dob, uid, bio):
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
