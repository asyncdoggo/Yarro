import datetime
import os
import uuid
from sqlalchemy import or_
from sqlalchemy import desc
from argon2 import PasswordHasher
from flask_sqlalchemy import SQLAlchemy
import flask
from app.db.classes import Message
from app.db.classes import db

def new_message(content, sender,reciever):
    gid = uuid.uuid4().hex
    tstamp = datetime.datetime.utcnow()

    msg: Message = Message(message_id=gid,
                            sender_id=sender,
                            reciever_id=reciever,
                            content=content,
                            tstamp=tstamp)
    
    db.session.add(msg)
    db.session.commit()
    return True



def get_message(sender,reciever,skip,limit):
    msg = Message.query.filter(((Message.sender_id==sender) & (Message.reciever_id==reciever)) | ((Message.sender_id==reciever) & (Message.reciever_id==sender))).order_by(Message.tstamp.desc()).limit(limit).offset(skip).all()

    d = []
    for i in msg:
        d.append(
            {
                "msg_id":i.message_id,
                "sender":True if i.sender_id == sender else False,
                "content":i.content
            }
        )

    return d