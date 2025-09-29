

from functools import wraps

from flask import g, request
import jwt

from app.util.jwt import decode_token


def _get_token_from_header():
    auth = request.headers.get("Authorization", "")
    if not auth:
        return None
    parts = auth.split()
    if len(parts) == 2 and parts[0] == "Bearer":
        return parts[1]
    else:
        return None
    

def optional_jwt(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth_token = _get_token_from_header()
        if auth_token:
            try:
                decoded = decode_token(auth_token)
            except jwt.ExpiredSignatureError:
                return {"msg": "Token Expired"}, 401
            except jwt.InvalidTokenError:
                return {"msg": "Invalid Token"}, 401

            user_id = decoded.get("sub")
            if user_id:
                g.current_user = {
                    "id": int(user_id),
                }
        else:
            g.current_user = None
        return func(*args, **kwargs)
    return wrapper
    

def required_jwt(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth_token = _get_token_from_header()
        if auth_token:
            try:
                decoded = decode_token(auth_token)
            except jwt.ExpiredSignatureError:
                return {"message": "Token Expired"}, 401
            except jwt.InvalidTokenError:
                return {"message": "Invalid Token"}, 401

            user_id = decoded.get("sub")
            if user_id:
                g.current_user = {
                    "id": int(user_id),
                }
        else:
            return {"message": "Missing access token. Access denied"}, 401
        return func(*args, **kwargs)
    return wrapper
    