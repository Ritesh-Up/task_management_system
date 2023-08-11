from rest_framework.exceptions import NotFound
from rest_framework import status, exceptions
from datetime import datetime, timedelta

from task.models import TaskModel, TaskUserMapModel
from user.models import UserModel


class TaskManagerService():
    def __init__(self, user: UserModel = None) -> None:
        self.user = user

    def task_user_mapping(self, tid, uid):
        try:
            return TaskUserMapModel.objects.get(task_id=tid, user_id=uid)
        except:
            return False

    def get_task_list(self, user: UserModel):
        if user.user_role == UserModel.USER_ROLE_CHOICES.admin:
            return TaskModel.objects.all()
        elif user.user_role == UserModel.USER_ROLE_CHOICES.normal:
            return TaskModel.objects.filter(user_id=user.id)
        elif user.user_role == UserModel.USER_ROLE_CHOICES.moderator:
            objects = TaskUserMapModel.objects.filter(user_id=user).select_related("task_id")
            task_list = []
            for o in objects:
                task_list.append(o.task_id)
            return task_list
        
        return None

    def get_task_by_id(self, id):
        try:
            return TaskModel.objects.get(id=id)
        except TaskModel.DoesNotExist:
            raise exceptions.NotFound("Task not found")
        except Exception as e:
            raise Exception(e)
        
    def add_task(self, data = dict()):
        try:
            taskInstance = TaskModel.objects.create(
               title=data.get("title", None),
               description=data.get("description", None),
               due_date=data.get("due_date", None),
               user_id = self.user
            )
            return taskInstance
        except Exception as e:
            raise e
        
    def update_task(self, taskInstance, payload = {}):
        try:
            if taskInstance is None or not isinstance(taskInstance, TaskModel):
                raise exceptions.ValidationError("Invalid Task Instance")
            
            taskInstance.title = payload.get("title", "")
            taskInstance.description = payload.get("description", "")
            taskInstance.due_date = payload.get("due_date", None)
            taskInstance.save()

            return taskInstance
        except Exception as e:
            raise e
        
    def delete_task(self, taskInstace):
        try:
            taskInstace.delete()
        except Exception as e:
            raise e

    def assign_task(self, task_id, user_id):
        try:
            task = self.get_task_by_id(id=task_id)
            user = UserModel.objects.get(id=user_id)

            return TaskUserMapModel.objects.create(
                task_id=task,
                user_id=user
            )
        except Exception as e:
            raise e