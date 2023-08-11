from rest_framework import serializers

from task.models import TaskModel, TaskUserMapModel
from task.services import TaskManagerService

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskModel
        fields = ("id", "title", "description", "due_date", "status")

    def create(self, validated_data):
        serviceInstance = TaskManagerService(user=self.context["request"].user)
        return serviceInstance.add_task(validated_data)

class TaskUserMapSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskUserMapModel
        fields = ("__all__")