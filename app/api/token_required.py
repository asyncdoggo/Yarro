from functools import wraps
import jwt
from flask import request
from jwt import ExpiredSignatureError, DecodeError
import app.db as db
from flask import current_app

def token_required(f):
    """
    token_required(f) decorator will validate a token f and return the User Class object defined in
    modules/Database. token is accessed from cookie with name token
    """

    @wraps(f)
    def decorator(*args, **kwargs):

        token = request.cookies.get("token")

        if not token:
            return {'message': 'a valid token is missing'}

        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = db.Users.query.filter_by(id=data['id']).one_or_none()
            if not current_user:
                admin = db.Admin.query.filter_by(id=data['id']).one_or_none()
                if admin:
                    return {"status":"cannot access user api as admin"}

            if not current_user.confirmed:
                return {"status": "email"}
        except ExpiredSignatureError:
            return {'status': 'expired'}
        except DecodeError:
            return {"status": "invalid"}

        return f(*args, current_user, **kwargs)

    return decorator
