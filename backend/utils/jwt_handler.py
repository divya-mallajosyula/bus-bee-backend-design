import datetime
from functools import wraps
from flask import request, jsonify, current_app
import jwt


def generate_token(user_id):
    expire_minutes = int(current_app.config.get("JWT_EXPIRE_MINUTES", 60))
    payload = {
        "sub": str(user_id),
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=expire_minutes),
        "iat": datetime.datetime.utcnow(),
    }
    secret = current_app.config.get("JWT_SECRET")
    algorithm = current_app.config.get("JWT_ALGORITHM", "HS256")
    return jwt.encode(payload, secret, algorithm=algorithm)


def decode_token(token):
    secret = current_app.config.get("JWT_SECRET")
    algorithm = current_app.config.get("JWT_ALGORITHM", "HS256")
    return jwt.decode(token, secret, algorithms=[algorithm])


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != "bearer":
            return jsonify({"error": "Authorization header missing or invalid"}), 401
        token = parts[1]
        try:
            data = decode_token(token)
            request.user_id = data.get("sub")
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except Exception:
            return jsonify({"error": "Invalid token"}), 401
        return f(*args, **kwargs)

    return decorated
