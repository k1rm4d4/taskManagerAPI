from app.models import Task, User

from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

def get_task_by_id(db: Session, task_id: int)->Task|None:
    query = select(Task).where(Task.id == task_id)
    task = db.execute(query).scalar_one_or_none()

    return task

def get_all_tasks(db: Session)->list[Task]:
    query = select(Task)
    tasks = db.scalars(query).all()
    return tasks

def add_new_task(db: Session, new_task_data):
    try:
        new_task = Task(**new_task_data)
        db.add(new_task)
        db.commit()
        db.refresh(new_task)
        return new_task
    except SQLAlchemyError:
        db.rollback()
        raise

def update_task(db: Session, update_data: dict, task_to_update: Task):
    try:
        for field in update_data.keys():
            setattr(task_to_update, field, update_data[field])
        db.commit()
        return task_to_update
    except SQLAlchemyError:
        db.rollback()
        raise


def delete_task(db: Session, task_to_delete: Task):
    try:
        db.delete(task_to_delete)
        db.commit()
        return
    except SQLAlchemyError:
        db.rollback()
        raise


def get_user_by_username(db: Session, username: str)->User|None:
    query = select(User).where(User.username == username)
    user = db.execute(query).scalar_one_or_none()
    return user

def add_user(db: Session, user_details: dict):
    new_user = User(**user_details)
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception as e:
        db.rollback()
        raise