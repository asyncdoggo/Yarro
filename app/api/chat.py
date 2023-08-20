from flask import current_app
from flask_socketio import SocketIO
from flask_socketio import emit
import jwt
import app.db as db
import flask


users = {}

socketio = SocketIO(cors_allowed_origins="*")


@socketio.on('connect')
def test_connect(auth):
    session_id = flask.request.sid
    token = auth["token"]
    user = verify_token(token)

    users[session_id] = user.id



@socketio.on('disconnect')
def test_disconnect():
    session_id = flask.request.sid
    del users[session_id]
    emit("disconnected")

@socketio.on("send_message")
def add_message(data):
    try:
        token = data["token"]
        message = data["message"]
        reciever = data["to_user"]

        if not message.strip():
            return emit("error",{"message":"empty"})

        user = verify_token(token)
        if db.new_message(sender = user.id, content=message,reciever=reciever):
            for i,j in users.items():
                if j == user.id:
                    data = db.get_message(user.id,reciever,0,10, send=True)
                    data["uid"] = j
                    data["rec"] = reciever
                    emit("messages",data,to=i)
                if j == reciever:
                    data = db.get_message(reciever,user.id,0,10, send=True)
                    data["uid"] = reciever
                    data["rec"] = user.id
                    emit("messages",data,to=i)
                    
        else:
            emit("failure",{"message":"message length exceeds 255 characters"})
    except Exception as e:
        print(e)
        emit("disconnect")


@socketio.on("get_messages")
def get_messages(data):
    try:
        token = data["token"]
        reciever = data["to_user"]
        limit = data["limit"]
        skip = data["page"]
        user = verify_token(token)
        data = db.get_message(user.id,reciever,skip,limit)
        data["uid"] = user.id
        data["rec"] = reciever

        return emit("messages",data,sid=flask.request.sid)

    except Exception as e:
        print(e)
        emit("disconnect")


def verify_token(token):
    if not token:
        return emit("disconnect")
    try:
        data = jwt.decode(
            token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
        current_user = db.Users.query.filter_by(id=data['id']).one_or_none()
        if not current_user:
            return emit("disconnect")
        return current_user
    except jwt.ExpiredSignatureError:
        return emit("disconnect")
    except jwt.DecodeError:
        return emit("disconnect")
    
    
@socketio.on("get_unread")
def get_unread_messages(data):
    token = data["token"]
    user = verify_token(token)
    unread = db.get_unread_messages(user.id)
    emit("unread",unread)