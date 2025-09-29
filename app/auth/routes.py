from flask_smorest import Blueprint, abort
from flask.views import MethodView
from flask import request
from werkzeug.security import check_password_hash, generate_password_hash


from app.crud import add_user, get_user_by_username
from app.db import SessionLocal
from app.schemas import LoginSchema, RegisterSchema, TokenSchema, UserOutSchema
from app.util.jwt import create_token
from sqlalchemy.exc import SQLAlchemyError

blp = Blueprint("auth", __name__, url_prefix="/auth", description="Authentication")


@blp.route("/register")
class Register(MethodView):
    @blp.arguments(RegisterSchema)
    @blp.response(201, UserOutSchema)
    def post(self, new_user):
        username = new_user.get("username")
        password = new_user.get("password")

        try:
            with SessionLocal() as db:
                existing_user = get_user_by_username(db, username)
                if existing_user:
                    abort(400, message=f"User with {username} already exists!")

                hashed_password = generate_password_hash(password)
                user_added = add_user(
                    db, {"username": username, "hash_password": hashed_password}
                )

                return {"username": f"{user_added.username}"}
        except SQLAlchemyError:
            abort(500, message="Internal Server Error")


@blp.route("/login")
class Login(MethodView):
    @blp.arguments(LoginSchema)
    @blp.response(200, TokenSchema)
    def post(self, user_login):
        username = user_login.get("username")
        password = user_login.get("password")

        try:
            with SessionLocal() as db:
                # check if username already present in DB
                existing_user = get_user_by_username(db, username)
                if not existing_user:
                    abort(400, message=f"User with {username} does not exist!")

                # check password hash
                if not check_password_hash(existing_user.hash_password, password):
                    abort(400, message="Invalid credentials.")

                # generate JWT AT token
                payload = {"sub": str(existing_user.id)}
                access_token = create_token(payload)

                return {"access_token": access_token, "token_type": "bearer"}
        except SQLAlchemyError:
            abort(500, message="Internal Server Error")
