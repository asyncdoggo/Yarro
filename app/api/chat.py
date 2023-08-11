from flask import current_app
from flask_socketio import SocketIO
from flask_socketio import emit, rooms,join_room,close_room,leave_room
import jwt
import app.db as db
import uuid
import flask


users = {}

socketio = SocketIO(cors_allowed_origins="*")


@socketio.on('connect')
def test_connect():
    session_id = flask.request.sid
    user_id = 1
    users[session_id] = user_id



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
            return emit("success",{"status":"message"})
        emit("failure",{"message":"failed to create message"})
    except:
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
        return emit("messages",data)

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