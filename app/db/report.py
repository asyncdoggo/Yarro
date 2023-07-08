import datetime
import os
from sqlalchemy import desc
from argon2 import PasswordHasher
from flask_sqlalchemy import SQLAlchemy
import flask
from app.db.classes import Reports, Details, DisLikes, Likes, Posts, Users
from app.db.classes import db


def add_report(pid, uid, reason):
    try:
        report = Reports(post_id=pid, reported_by=uid,
                         reason=reason, created_at=datetime.datetime.utcnow())
        db.session.add(report)
        db.session.commit()
        return True
    except Exception as e:
        print(e)


def get_all_reports(limit=10,page=0):
    try:
        reports = Reports.query.limit(limit).offset(page).all()
        return reports
    except Exception as e:
        print(e)