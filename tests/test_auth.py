from sqlalchemy import select

from app.models import User


def register_user(client, username="testuser", password="secret"):
    payload = {"username": username, "password": password}
    return client.post("/auth/register", json=payload, content_type="application/json")


def login_user(client, username="testuser", password="secret"):
    payload = {"username": username, "password": password}
    return client.post("/auth/login", json=payload, content_type="application/json")

def test_register_user(client, db_session):
    test_username = "test_user"
    resp = register_user(client=client, username=test_username)
    assert resp.status_code == 201
    assert resp.get_json() == {'username': test_username}

    # check in db
    q = select(User).where(User.username == test_username)
    user_in_db = db_session.execute(q).scalar_one_or_none()
    assert user_in_db is not None

def test_register_duplicate_fails(client, db_session):
    test_username = "test_user01"
    resp = register_user(client=client, username=test_username)
    assert resp.status_code == 201
    test_username2 = "test_user01"
    resp = register_user(client=client, username=test_username2)
    assert resp.status_code == 400
    resp_data = resp.get_json()
    assert resp_data["code"]  == 400
    assert resp_data["message"]  == f"User with {test_username2} already exists!"
    assert resp_data["status"]  == "Bad Request"


def test_login_return_token(client):
    test_username = "test_user03"
    test_password = "test_pass"
    resp = register_user(client=client, username=test_username, password=test_password)
    assert resp.status_code == 201

    # login
    resp2 = login_user(client=client, username=test_username, password=test_password)
    assert resp2.status_code == 200
    resp_data = resp2.get_json()
    assert resp_data['access_token'] is not None
    assert resp_data['token_type'] == "bearer"


def test_login_wrong_password(client):
    test_username = "test_user04"
    test_password = "test_pass"
    resp = register_user(client=client, username=test_username, password=test_password)
    assert resp.status_code == 201

    # login
    resp2 = login_user(client=client, username=test_username, password="WrongPass")
    assert resp2.status_code == 400
    resp_data = resp2.get_json()
    assert resp_data["code"]  == 400
    assert resp_data["message"]  == "Invalid credentials."
    assert resp_data["status"]  == "Bad Request"
    