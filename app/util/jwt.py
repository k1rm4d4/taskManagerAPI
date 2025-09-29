import os
import jwt

from datetime import timedelta, datetime, timezone

SECRET_KEY = os.getenv("SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


def create_token(data: dict, expires_delta: timedelta | None = None)-> str:
    payload = data.copy()
    if expires_delta:
        payload.update({"exp": datetime.now(tz=timezone.utc) + expires_delta})
    else:
        now = datetime.now(tz=timezone.utc)
        payload.update(
            {
                "exp": now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
                "iat": now,
            }
        )
    encoded_jwt = jwt.encode(payload, SECRET_KEY, JWT_ALGORITHM)
    return encoded_jwt



def decode_token(token: str)->dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise
    except jwt.InvalidTokenError:
        raise