from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from .auth import user_service
from ..services.task_service import TaskService


task_bp = Blueprint("tasks",__name__, url_prefix="/tasks")
task_service = TaskService()


@task_bp.get("/")
@jwt_required()
def handle_task():
    email = get_jwt_identity()
    user = user_service.find_by_email(email)
    if not user:
        return "Resource not found", 404
    tasks = task_service.get_user_tasks(user.id)
    list_task = list(map(lambda x:x.get_dictionary(), tasks))
    return list_task


@task_bp.post("/")
@jwt_required()
def add_task():
    body_args=  request.json
    email = get_jwt_identity()
    user = user_service.find_by_email(email)
    if not user:
        return "Resource not found", 404
    task = task_service.create_task(
        user.id,
        body_args.get("title"),
        body_args.get("description")
    )
    return {"message":"Task created", "task_id": task.id}, 201


@task_bp.put("/<task_id>")
@jwt_required()
def handle_update_task(task_id):
    email = get_jwt_identity()
    user = user_service.find_by_email(email)
    if not user:
        return "Resource not found", 404

    body_params = request.json
    task_list = task_service.get_user_tasks(user.id)
    for task in task_list:
        if task.id == task_id:
            task.title = body_params.get("title")
            task.description = body_params.get("description")
            return task.get_dictionary(), 200
    return "Task not found", 404


@task_bp.delete("/<task_id>")
@jwt_required()
def handle_delete_task(task_id):
    email = get_jwt_identity()
    user = user_service.find_by_email(email)
    if not user:
        return "Resource not found", 404

    task = task_service.delete_task(task_id, user.id)
    if not task:
        return "Task not found", 404
    return {"message": "Task deleted"}, 200
