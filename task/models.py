import uuid
from django.db import models
from model_utils import Choices
from django.utils.translation import gettext_lazy as _
from user.models import UserModel

# Create your models here.
class TaskModel(models.Model):
    TASK_STATUS_CHOICES = Choices(
        (1, 'todo', _('todo')),
        (2, 'in_progress', _('in_progress')),
        (3, 'done', _('done')),
        (4, 'discarded', _('discarded'))
    )
    id = models.UUIDField(db_column="id", default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    title = models.CharField(max_length=255, null=False)
    description = models.TextField(blank=True)
    status = models.IntegerField(choices=TASK_STATUS_CHOICES, default=1)
    due_date = models.DateTimeField(null=True)
    user_id = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = "task"

class TaskUserMapModel(models.Model):
    user_id = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    task_id = models.ForeignKey(TaskModel, on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = "task_user_map"
        unique_together = (('user_id', 'task_id'))