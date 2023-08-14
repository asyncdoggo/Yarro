import datetime
import uuid
from app.db.classes import Message
from app.db.classes import db

def new_message(content, sender,reciever):
    gid = uuid.uuid4().hex
    tstamp = datetime.datetime.utcnow()
    if len(content) >= 255:
        return False
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

    db.session.close()


    d = []
    for i in msg:
        d.append(
            {
                "msg_id":i.message_id,
                "sender":i.sender_id == sender,
                "content":i.content
            }
        )

    return {"messages":d}