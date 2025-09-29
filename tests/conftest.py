# tests/conftest.py
import os
import tempfile
import pytest
from app import create_app
from app import db as app_db  # this is your app.db module
from app.db import Model  # Declarative base class; Model.metadata has metadata
from app.models import User
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from werkzeug.security import generate_password_hash


@pytest.fixture(scope="session")
def tmp_sqlite_file():
    """Create a temporary sqlite file for the whole test session."""
    fd, path = tempfile.mkstemp(suffix=".sqlite", prefix="test_db")
    os.close(fd)
    yield path
    try:
        os.remove(path)
    except OSError:
        pass


@pytest.fixture(scope="session")
def app(tmp_sqlite_file):
    """Create Flask app configured for testing and initialize DB engine."""
    test_db_url = f"sqlite:///{tmp_sqlite_file}"
    config = {
        "TESTING": True,
        "DATABASE_URL": test_db_url,
        "JWT_SECRET_KEY": "test-secret",  # if using JWT
    }

    # create app (this calls init_engine inside create_app)
    _app = create_app(config=config)

    # Ensure db engine/session objects were initialized
    # app.db.init_engine was called by create_app, but to be safe we can re-init
    # app_db.init_engine(test_db_url, echo=False, future=True)

    # create schema
    with _app.app_context():
        # Model is your DeclarativeBase subclass defining metadata
        Model.metadata.create_all(app_db.engine)

    yield _app

    # teardown session-level DB
    with _app.app_context():
        Model.metadata.drop_all(app_db.engine)


@pytest.fixture()
def client(app):
    """A test client. DB state persists for the whole session file unless you clean per-test."""
    return app.test_client()


@pytest.fixture()
def db_session(app):
    """
    Provide a SQLAlchemy session bound to the test engine. Use inside tests when you want
    to create objects directly (bypassing the API).
    """
    # Create a new Session maker bound to the same engine
    Session = sessionmaker(bind=app_db.engine, autoflush=False, autocommit=False)
    session = Session()
    try:
        yield session
    finally:
        session.rollback()
        session.close()


@pytest.fixture
def test_user(db_session):
    test_username = "test_user01"
    test_password = "test_pass"

    # check and return if existing user
    q = select(User).where(User.username == test_username)
    existing = db_session.execute(q).scalar_one_or_none()
    if existing:
        user = existing.to_dict()
        user["_test_password"] = test_password
        return user

    password_hash = generate_password_hash(test_password)
    user = User(username=test_username, hash_password=password_hash)
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    new_user = user.to_dict()
    new_user["_test_password"] = test_password
    return new_user


@pytest.fixture
def auth_token(client, test_user):
    test_username = test_user["username"]
    test_password = test_user["_test_password"]
    resp = client.post(
        "/auth/login", json={"username": test_username, "password": test_password}
    )
    assert resp.status_code == 200, f"login failed in fixture: {resp.data}"
    data = resp.get_json()
    # adjust key based on your login response
    token = data.get("access_token")
    return token


@pytest.fixture
def auth_headers(auth_token):
    return {"Authorization": f"Bearer {auth_token}"}
