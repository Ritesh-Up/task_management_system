import uuid
from django.db import models
from model_utils import Choices
from django.utils.translation import gettext_lazy as _

# Create your models here.
class UserModel(models.Model):
    USER_ROLE_CHOICES = Choices(
        (3, 'admin', _('admin')),
        (2, 'moderator', _('moderator')),
        (1, 'normal', _('normal'))
    )

    id = models.UUIDField(db_column="id", default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    name = models.CharField(max_length=100, null=False)
    email = models.CharField(max_length=255, unique=True, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user_role = models.IntegerField(choices=USER_ROLE_CHOICES, default=1)

    class Meta:
        managed = True
        db_table = "user"