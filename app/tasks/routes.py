

from flask import request, make_response
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from app.db import SessionLocal
from app.models import Task

from app.crud import add_new_task, delete_task, get_all_tasks, get_task_by_id, update_task
from app.schemas import TaskSchema, TaskCreateSchema, TaskUpdateSchema
from app.util.auth import optional_jwt, required_jwt
from sqlalchemy.exc import SQLAlchemyError

blp = Blueprint('tasks', __name__, url_prefix="/tasks", description="Tasks operations")


@blp.route("")
class TaskList(MethodView):

    @optional_jwt
    @blp.response(200, TaskSchema(many=True))
    def get(self):
        try:
            with SessionLocal() as db:
                tasks = get_all_tasks(db)
                all_tasks = [t.to_dict()  for t in tasks]
                return all_tasks
        except SQLAlchemyError:
            abort(500, message="Internal Server Error")


    @required_jwt
    @blp.doc(security=[{"bearerAuth": []}])
    @blp.arguments(TaskCreateSchema)
    @blp.response(201, TaskSchema)
    def post(self, new_task_data):
        # add to db:
        try:
            with SessionLocal() as db:
                new_task = add_new_task(db, new_task_data)
                if not new_task:
                    abort(500, detail="Internal Server error.")
                return new_task.to_dict()
        except SQLAlchemyError:
            abort(500, message="Internal Server Error")    

@blp.route("/<int:task_id>")
class TaskItem(MethodView):

    @optional_jwt
    @blp.response(200, TaskSchema)
    def get(self, task_id):
        try:
            with SessionLocal() as db:
                task = get_task_by_id(db, task_id)
                if task:
                    return task.to_dict()
                else:
                    abort(404, message=f"Task with ID: {task_id} not found!")
        except SQLAlchemyError:
            abort(500, message="Internal Server Error")

    @required_jwt
    @blp.doc(security=[{"bearerAuth": []}])
    @blp.arguments(TaskUpdateSchema(partial=True))
    @blp.response(200, TaskSchema)
    def put(self, update_data, task_id):
        try:
            with SessionLocal() as db:
                task_to_update = get_task_by_id(db, task_id)
                if not task_to_update:
                    abort(404, message=f"Task with ID: {task_id} not found!")

                updated_task = update_task(db, update_data, task_to_update)
                return updated_task.to_dict()
        except SQLAlchemyError:
            abort(500, message="Internal Server Error")

    @required_jwt
    @blp.doc(security=[{"bearerAuth": []}])
    @blp.response(204)
    def delete(self, task_id):
        try:
            with SessionLocal() as db:
                task_to_delete = get_task_by_id(db, task_id)
                if not task_to_delete:
                    abort(404, message=f"Task with ID: {task_id} not found!")
                delete_task(db, task_to_delete)
                return "", 204
        except SQLAlchemyError:
            abort(500, message="Internal Server Error")

