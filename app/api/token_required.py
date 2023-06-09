from functools import wraps
import jwt
from flask import request, jsonify
from jwt import ExpiredSignatureError, DecodeError
import app.db as Data
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
            return jsonify({'message': 'a valid token is missing'})

        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = Data.Users.query.filter_by(id=data['id']).first()

            if not current_user.confirmed:
                return {"status": "email"}
        except ExpiredSignatureError:
            return jsonify({'status': 'expired'})
        except DecodeError:
            return jsonify({"status": "invalid"})

        return f(*args, current_user, **kwargs)

    return decorator
