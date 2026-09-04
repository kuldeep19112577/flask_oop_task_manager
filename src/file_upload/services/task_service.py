from datetime import datetime
from uuid import uuid4
from ..models.task import Task


task_archive = {}


class TaskService:
    def create_task(self, user_id, title, description):
        task = Task(
            id=f"TASK_ID_{str(uuid4())}",
            title=title,
            description=description,
            user_id=user_id,
            created_at=str(datetime.now())
        )
        if user_id in task_archive:
            task_archive[user_id].append(task)
        else:
            task_archive[user_id] = [task]
        return task

    def get_user_tasks(self, user_id):
        return task_archive.get(user_id, [])

    def delete_task(self, task_id, user_id):
        task_list = task_archive.get(user_id, [])
        for task in task_list:
            if task.id == task_id:
                task_list.remove(task)
                return task
        return None
