
import json
import pytest


from app.models import Task


def test_login_and_use_token(client, auth_headers):
    resp2 = client.post("/tasks", json={"title": "test title"}, headers=auth_headers)
    assert resp2.status_code == 201


# get all tasks
def test_tasks_root_exists(client):
    # no auth token needed
    resp = client.get("/tasks")
    assert resp.status_code == 200
    resp_data = resp.get_json()
    assert isinstance(resp_data, list)


# test get single task route
def test_create_and_get_single_task(client, db_session):
    new_task = Task(title="sample task title", completed=False)
    db_session.add(new_task)
    db_session.commit()
    db_session.refresh(new_task)
    task_id = new_task.id

    # attempt to get the task
    resp = client.get(f"/tasks/{task_id}")
    assert resp.status_code == 200
    resp_data = resp.get_json()
    assert resp_data["title"] == "sample task title"
    assert resp_data["completed"] is False


def test_task_not_found(client):
    task_id = 999
    resp = client.get(f"/tasks/{task_id}")
    assert resp.status_code == 404
    resp_data = resp.get_json()
    assert resp_data['message'] == f"Task with ID: {task_id} not found!"
    assert resp_data['code'] == 404
    assert resp_data['status'] == "Not Found"



# test create task route
def test_create_task_no_token(client):
    new_task = {"title": "test title"}
    resp = client.post("/tasks", json=new_task)
    assert resp.status_code == 401
    resp_data = resp.get_json()
    assert resp_data['message'] == "Missing access token. Access denied"


def test_create_task(client, auth_headers):
    new_task = {"title": "test title"}
    resp2 = client.post("/tasks", json=new_task, headers=auth_headers)
    assert resp2.status_code == 201
    resp_data = resp2.get_json()
    assert resp_data["title"] == "test title"
    assert resp_data["completed"] is False
    assert resp_data["description"] is None

# test update task

def test_update_task_no_auth(client, db_session):
    new_task = Task(title="sample task title", completed=False)
    db_session.add(new_task)
    db_session.commit()
    db_session.refresh(new_task)
    task_id = new_task.id

    # attempt tp update the task
    resp = client.put(f"/tasks/{task_id}", json={"title": "create some notes"})
    assert resp.status_code == 401
    assert resp.get_json() == {"message": "Missing access token. Access denied"}

def test_update_task(client, db_session, auth_headers):
    new_task = Task(title="sample task title", completed=False)
    db_session.add(new_task)
    db_session.commit()
    db_session.refresh(new_task)
    task_id = new_task.id

    # attempt tp update the task
    resp = client.put(f"/tasks/{task_id}", json={"title": "create some notes", "completed": False}, headers=auth_headers)
    assert resp.status_code == 200
    resp_data = resp.get_json()
    assert resp_data["title"] == "create some notes"
    assert resp_data["completed"] is  False

# test delete task

def test_delete_task_no_auth(client, db_session):
    new_task = Task(title="sample task title", completed=False)
    db_session.add(new_task)
    db_session.commit()
    db_session.refresh(new_task)
    task_id = new_task.id

    # attempt tp update the task
    resp = client.delete(f"/tasks/{task_id}")
    assert resp.status_code == 401
    assert resp.get_json() == {"message": "Missing access token. Access denied"}

def test_delete_task(client, db_session, auth_headers):
    new_task = Task(title="sample task title", completed=False)
    db_session.add(new_task)
    db_session.commit()
    db_session.refresh(new_task)
    task_id = new_task.id

    # attempt tp update the task
    resp = client.delete(f"/tasks/{task_id}", headers=auth_headers)
    assert resp.status_code == 204
    # assert resp.get_json() is None