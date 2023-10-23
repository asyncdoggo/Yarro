import datetime
import uuid
from app.db.classes import Message
from app.db.classes import db
from markupsafe import escape

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



def get_message(sender,reciever,skip,limit,send=False):
    msg = Message.query.filter(((Message.sender_id==sender) & (Message.reciever_id==reciever)) | ((Message.sender_id==reciever) & (Message.reciever_id==sender))).order_by(Message.tstamp.desc()).limit(limit).offset(skip).all()

    d = []
    for i in msg:
        d.append(
            {
                "msg_id":i.message_id,
                "sender":i.sender_id == sender,
                "content":escape(i.content)
            }
        )
        if i.reciever_id == sender and not send:
            i.unread = False
            # db.session.flush()
        
    db.session.commit()

    return {"messages":d}




def get_unread_messages(rec):
    msg = Message.query.filter_by(reciever_id=rec, unread=True).all()
    unread = []
 
    for i in msg:
        unread.append(i.sender_id)
        
    return unread




### get message count between 2 users
# select sender_id,reciever_id,count(content) from messages group by sender_id, reciever_id having count(content) >= 0;